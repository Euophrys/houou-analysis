from spine_shanten.ihand_calculator import IHandCalculator
from spine_shanten.suits_classifier import SuitClassifier
from spine_shanten.chiitoi_classifier import ChiitoiClassifier
from spine_shanten.kokushi_classifier import KokushiClassifier
from spine_shanten.progressive_honor_classifier import ProgressiveHonorClassifier
from spine_shanten.arrangement_classifier import Classify
from collections import Counter

Base5Table = (
    1,
    5,
    25,
    125,
    625,
    3125,
    15625,
    78125,
    390625
)

class HandCalculator(IHandCalculator):
    def __init__(self):
        self.arrangementValues = [0] * 4
        self.base5Hashes = [0] * 3
        self.concealedTiles = [0] * 34
        self.inHandByType = [0] * 34
        self.melds = [0] * 3
        self.jihaiMeldBit = 0
        self.suitClassifiers = [SuitClassifier(), SuitClassifier(), SuitClassifier()]
        self.chiitoi = ChiitoiClassifier()
        self.kokushi = KokushiClassifier()
        self.honorClassifier = ProgressiveHonorClassifier()
        self.meldCount = 0

    def __str__(self):
        return "later"
      #return Shanten + ": " + GetConcealedString(0, 'm') + GetConcealedString(1, 'p') + GetConcealedString(2, 's') +
       #      GetConcealedString(3, 'z') +
        #     GetMeldString(0, 'M') + GetMeldString(1, 'P') + GetMeldString(2, 'S') + GetHonorMeldString()

    def Shanten(self):
        return self.CalculateShanten(self.arrangementValues) - 1

    def CalculateShanten(self, arrangementValues):
        shanten = Classify(arrangementValues)
        if (self.meldCount > 0):
            return shanten
        
        return min(shanten, self.kokushi.shanten, self.chiitoi.shanten)

    def Init(self, tiles):
        for tile in tiles:
            tileValue = tile % 9
            tileSuit = tile // 9
            self.inHandByType[tile] += 1

            previousTileCount = self.concealedTiles[tile]
            self.concealedTiles[tile] += 1
            self.kokushi.Draw(tile, previousTileCount)
            self.chiitoi.Draw(previousTileCount)

            if tileSuit == 3:
                self.arrangementValues[3] = self.honorClassifier.Draw(previousTileCount, self.jihaiMeldBit >> tileValue & 1)
            else:
                self.base5Hashes[tileSuit] += Base5Table[tileValue]

        self.UpdateValue(0)
        self.UpdateValue(1)
        self.UpdateValue(2)

    def Draw(self, tile):
        tileValue = tile % 9
        tileSuit = tile // 9
        self.inHandByType[tile] += 1

        previousTileCount = self.concealedTiles[tile]
        self.concealedTiles[tile] += 1
        self.kokushi.Draw(tile, previousTileCount)
        self.chiitoi.Draw(previousTileCount)

        if (tileSuit == 3):
            self.arrangementValues[3] = self.honorClassifier.Draw(previousTileCount, self.jihaiMeldBit >> tileValue & 1)
        else:
            self.base5Hashes[tileSuit] += Base5Table[tileValue]
            self.UpdateValue(tileSuit)

    def UpdateValue(self, suit):
        self.arrangementValues[suit] = self.suitClassifiers[suit].GetValue(self.concealedTiles, suit, self.base5Hashes)

    def Discard(self, tile):
        tileValue = tile % 9
        tileSuit = tile // 9
        self.inHandByType[tile] -= 1
        self.concealedTiles[tile] -= 1
        tileCountAfterDiscard = self.concealedTiles[tile]
        self.kokushi.Discard(tile, tileCountAfterDiscard)
        self.chiitoi.Discard(tileCountAfterDiscard)

        if (tileSuit == 3):
            self.arrangementValues[3] = self.honorClassifier.Discard(tileCountAfterDiscard, self.jihaiMeldBit >> tileValue & 1)
        else:
            self.base5Hashes[tileSuit] -= Base5Table[tileValue]
            self.UpdateValue(tileSuit)
      
    def Chii(self, lowestTileType, calledTileType):
        suitId = lowestTileType // 9
        lowestTileTypeIdInSuit = lowestTileType % 9

        self.concealedTiles[lowestTileType] -= 1
        self.concealedTiles[lowestTileType + 1] -= 1
        self.concealedTiles[lowestTileType + 2] -= 1
        self.concealedTiles[calledTileType] += 1

        self.melds[suitId] <<= 6
        self.melds[suitId] += 1 + lowestTileTypeIdInSuit
        self.meldCount += 1
        self.inHandByType[calledTileType] += 1
        self.suitClassifiers[suitId].SetMelds(self.melds[suitId])
        
        self.UpdateValue(suitId)
    
    def Pon(self, tile):
        suitId = tile // 9
        index = tile % 9
        self.inHandByType[tile] += 1
        self.meldCount += 1
        
        previousTiles = self.concealedTiles[tile]
        self.concealedTiles[tile] -= 2
        if suitId < 3:
            self.melds[suitId] <<= 6
            self.melds[suitId] += 1 + 7 + index
            self.suitClassifiers[suitId].SetMelds(self.melds[suitId])
            self.UpdateValue(suitId)
        else:
            self.arrangementValues[3] = self.honorClassifier.Pon(previousTiles)
            self.jihaiMeldBit += 1 << index

    def Shouminkan(self, tile):
        suitId = tile // 9
        self.concealedTiles[tile] -= 1

        if suitId < 3:
            for i in range(4):
                pon = 1 + 7 + tile % 9
                if (self.melds[suitId] >> 6 * i & 0b111111) == pon:
                    self.melds[suitId] += 9 << 6 * i
                break
                
            self.suitClassifiers[suitId].SetMelds(self.melds[suitId])
            self.UpdateValue(suitId)
        else:
            self.arrangementValues[3] = self.honorClassifier.Shouminkan()
      
    def Ankan(self, tile):
        suitId = tile // 9
        index = tile % 9
        self.concealedTiles[tile] -= 4
        self.meldCount += 1

        if suitId < 3:
            self.melds[suitId] <<= 6
            self.melds[suitId] += 1 + 7 + 9 + index
            self.suitClassifiers[suitId].SetMelds(self.melds[suitId])
            self.UpdateValue(suitId)
        else:
            self.arrangementValues[3] = self.honorClassifier.Ankan()
      
    def Daiminkan(self, tile):
        suitId = tile // 9
        index = tile % 9
        self.inHandByType[tile] += 1
        self.concealedTiles[tile] -= 3
        self.meldCount += 1

        if (suitId < 3):
            self.melds[suitId] <<= 6
            self.melds[suitId] += 1 + 7 + 9 + index
            self.suitClassifiers[suitId].SetMelds(self.melds[suitId])
            self.UpdateValue(suitId)
        else:
            self.arrangementValues[3] = self.honorClassifier.Daiminkan()
      
    def GetUkeIreFor13(self):
        currentShanten = self.CalculateShanten(self.arrangementValues)

        ukeIre = Counter()
        tileId = 0
        localArrangements = [self.arrangementValues[0], self.arrangementValues[1], self.arrangementValues[2], self.arrangementValues[3]]
        
        for suit in range(3):
            for index in range(9):
                if (self.inHandByType[tileId] != 4):
                    self.kokushi.Draw(tileId, self.concealedTiles[tileId])
                    self.chiitoi.Draw(self.concealedTiles[tileId])

                    self.concealedTiles[tileId] += 1
                    self.base5Hashes[suit] += Base5Table[index]
                    localArrangements[suit] = self.suitClassifiers[suit].GetValue(self.concealedTiles, suit, self.base5Hashes)

                    newShanten = self.CalculateShanten(localArrangements)
                    a = currentShanten - newShanten
                    
                    if newShanten < currentShanten:
                        ukeIre[tileId] = 4 - self.inHandByType[tileId]

                    self.concealedTiles[tileId] -= 1
                    self.base5Hashes[suit] -= Base5Table[index]
                    self.kokushi.Discard(tileId, self.concealedTiles[tileId])
                    self.chiitoi.Discard(self.concealedTiles[tileId])
                else:
                    ukeIre[tileId] = -1

                tileId += 1
            localArrangements[suit] = self.arrangementValues[suit]
        
        for index in range(7):
            if (self.inHandByType[tileId] != 4):
                previousTileCount = self.concealedTiles[tileId]
                self.kokushi.Draw(tileId, previousTileCount)
                self.chiitoi.Draw(previousTileCount)
                localArrangements[3] = self.honorClassifier.Clone().Draw(self.concealedTiles[tileId], self.jihaiMeldBit >> index & 1)

                newShanten = self.CalculateShanten(localArrangements)
                a = currentShanten - newShanten
                
                # this evaluates to (remaining tiles of that type) or -1 if newShanten is not better than currentShanten
                t = (5 - self.inHandByType[tileId]) * a - 1
                ukeIre[27 + index] = t

                self.chiitoi.Discard(previousTileCount)
                self.kokushi.Discard(tileId, previousTileCount)
            
            else:
                ukeIre[tileId] = -1
            tileId += 1
        return ukeIre
    
    def ShantenAfterDiscard(self, tile):
        Discard(tile)
        shantenAfterDiscard = self.CalculateShanten(self.arrangementValues) - 1
        Draw(tile)
        return shantenAfterDiscard
    
    def ShantenWithTile(self, tile):
        Draw(tile)
        shantenWithTile = self.CalculateShanten(self.arrangementValues) - 1
        Discard(tile)
        return shantenWithTile
    
    def Clone(self):
        hand = HandCalculator()
        hand.concealedTiles = self.concealedTiles.copy()
        hand.melds = self.melds.copy()
        hand.inHandByType = self.inHandByType.copy()
        hand.jihaiMeldBit = self.jihaiMeldBit
        hand.arrangementValues = self.arrangementValues.copy()
        hand.meldCount = self.meldCount

        for i in len(self.suitClassifiers):
            hand.self.suitClassifiers[i] = self.suitClassifiers[i].Clone()

        hand.kokushi = self.kokushi.Clone()
        hand.chiitoi = self.chiitoi.Clone()
        hand.honorClassifier = self.honorClassifier.Clone()
        return hand
    
    def TilesInHand(self):
        return sum(self.concealedTiles) + self.meldCount * 3
    
    def InitializeJihaiMelds(self, meldIds):
        for meldId in meldIds:
            self.meldCount += 1

            if (meldId < 7 + 9):
                index = meldId - 7
                tile = index + 27
                self.honorClassifier.Draw(0, 0)
                self.honorClassifier.Draw(1, 0)
                self.arrangementValues[3] = self.honorClassifier.Pon(2)
                self.jihaiMeldBit += 1 << index
                self.inHandByType[tile] += 3
            
            else:
                index = meldId - 16
                tile = index + 27
                self.honorClassifier.Draw(0, 0)
                self.honorClassifier.Draw(1, 0)
                self.honorClassifier.Draw(2, 0)
                self.arrangementValues[3] = self.honorClassifier.Daiminkan()
                self.inHandByType[tile] += 4
        
    def InitializeSuitMelds(self, meldIds, suitId):
        for meldId in meldIds:
            self.melds[suitId] <<= 6
            self.melds[suitId] += 1 + meldId
            self.meldCount += 1

            if (meldId < 7):
                start = 9 * suitId + meldId
                self.inHandByType[start + 0] += 1
                self.inHandByType[start + 1] += 1
                self.inHandByType[start + 2] += 1
            elif (meldId < 16):
                self.inHandByType[9 * suitId + meldId - 7] += 3
            else:
                self.inHandByType[9 * suitId + meldId - 16] += 4
            
            self.suitClassifiers[suitId].SetMelds(self.melds[suitId])
    
    