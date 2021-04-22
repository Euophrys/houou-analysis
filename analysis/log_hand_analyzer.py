from log_analyzer import LogAnalyzer
from analysis_utils import convertHai, convertTile, discards, draws, GetNextRealTag, GetStartingHands, getTilesFromCall
from abc import abstractmethod
from spine_shanten.hand_calculator import HandCalculator

class LogHandAnalyzer(LogAnalyzer):
    def __init__(self):
        self.hands = [[], [], [], []]
        self.calculators = [HandCalculator(), HandCalculator(), HandCalculator(), HandCalculator()]
        self.calls = [[], [], [], []]
        self.discards = [[], [], [], []]
        self.last_draw = [50,50,50,50]
        self.end_round = False
        self.current_log_id = ""
        self.ignore_calls = False

    def ParseLog(self, log, log_id):
        self.current_log_id = log_id

        for round_ in log.iter("INIT"):
            self.RoundStarted(round_)

            for element in round_.itersiblings():
                if self.end_round: break

                if element.tag == "DORA":
                    self.DoraRevealed(element.attrib["hai"], element)

                elif element.tag[0] in discards:
                    who = ord(element.tag[0]) - 68
                    tile = convertTile(element.tag[1:])
                    self.TileDiscarded(who, tile, tile == self.last_draw[who], element)

                elif element.tag == "UN":
                    self.Reconnection(element)
                    
                elif element.tag[0] in draws:
                    who = ord(element.tag[0]) - 84
                    tile = convertTile(element.tag[1:])
                    self.last_draw[who] = tile
                    self.TileDrawn(who, tile, element)

                elif element.tag == "N":
                    if not self.ignore_calls:
                        self.TileCalled(int(element.attrib["who"]), getTilesFromCall(element.attrib["m"]), element)
                
                elif element.tag == "REACH":
                    self.RiichiCalled(int(element.attrib["who"]), int(element.attrib["step"]), element)
                
                elif element.tag == "INIT":
                    break

                elif element.tag == "AGARI":
                    self.Win(element)
                    break
                
                elif element.tag == "RYUUKYOKU":
                    if "type" in element.attrib:
                        self.AbortiveDraw(element)
                    else:
                        self.ExhaustiveDraw(element)
                    break

                elif element.tag == "BYE":
                    self.Disconnection(element)

            self.RoundEnded(round_)
        self.ReplayComplete()
    
    def RoundStarted(self, init):
        self.hands = GetStartingHands(init)
        self.calculators = [HandCalculator(), HandCalculator(), HandCalculator(), HandCalculator()]

        for i in range(4):
            tiles = []
            for tile in self.hands[i]:
                for j in range(self.hands[i][tile]):
                    tiles.append(tile)
            self.calculators[i].Init(tiles)

        self.calls = [[], [], [], []]
        self.discards = [[], [], [], []]
        self.end_round = False
    
    def DoraRevealed(self, hai, element):
        pass

    def TileDiscarded(self, who, tile, tsumogiri, element):
        self.hands[who][tile] -= 1
        self.discards[who].append(tile)
        self.calculators[who].Discard(tile)

    def TileDrawn(self, who, tile, element):
        self.hands[who][tile] += 1
        self.calculators[who].Draw(tile)

    def TileCalled(self, who, tiles, element):
        length = len(tiles)
        if length == 1:
            self.hands[who][tiles[0]] -= 1
            self.calculators[who].Shouminkan(tiles[0])
        elif length == 4:
            if self.hands[who][tiles[0]] == 4:
                self.calculators[who].Ankan(tiles[0])
            else:
                self.calculators[who].Daiminkan(tiles[0])
            self.hands[who][tiles[0]] = 0
        else:
            if tiles[1] == tiles[2]:
                self.calculators[who].Pon(tiles[0])
            else:
                self.calculators[who].Chii(min(tiles), tiles[0])
            self.hands[who][tiles[1]] -= 1
            self.hands[who][tiles[2]] -= 1
        self.calls[who].append(tiles)

    def RiichiCalled(self, who, step, element):
        pass

    def RoundEnded(self, init):
        pass

    def Win(self, element):
        pass

    def ExhaustiveDraw(self, element):
        pass

    def AbortiveDraw(self, element):
        pass

    def ReplayComplete(self):
        pass

    def Disconnection(self, element):
        pass

    def Reconnection(self, element):
        pass
    
    @abstractmethod
    def PrintResults(self):
        pass