class ChiitoiClassifier():
    def __init__(self, shanten = 7):
        self.shanten = shanten

    def Clone(self):
        return ChiitoiClassifier(self.shanten)

    def Draw(self, previousTileCount):
        if previousTileCount == 1:
            self.shanten -= 1

    def Discard(self, tileCountAfterDiscard):
        if tileCountAfterDiscard == 1:
            self.shanten += 1