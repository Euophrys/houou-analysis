class ChiitoiClassifier():
    def __init__(self, shanten = 7):
        self.shanten = shanten

    def Clone(self):
        return ChiitoiClassifier(self.shanten)

    def Draw(self, previousTileCount):
        # ((x >> 1) ^ 001) & x
        # 1 if x == 1 else 0
        self.shanten -= ((previousTileCount >> 1) ^ 1) & previousTileCount

    def Discard(self, tileCountAfterDiscard):
        # ((x >> 1) ^ 001) & x
        # 1 if x == 1 else 0
        self.shanten += ((tileCountAfterDiscard >> 1) ^ 1) & tileCountAfterDiscard