from spine_shanten.tile_type import FromSuitAndIndex

class Meld():
    def __init__(self, suit, meldId):
        self.suit = suit
        self.meldId = meldId
        
    def __iter__(self):
        if self.meldId < 7:
            return iter([FromSuitAndIndex(self.suit, self.meldId + self.position - x) for x in range(3)])
        elif self.meldId < 16:
            return iter([FromSuitAndIndex(self.suit, self.meldId - 7) for x in range(3)])
        else:
            return iter([FromSuitAndIndex(self.suit, self.meldId - 16) for x in range(4)])