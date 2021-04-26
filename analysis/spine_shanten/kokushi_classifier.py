class KokushiClassifier():
    def __init__(self, shanten = 14, pairs = 1):
        self.shanten = 14
        self.__pairs = 1

    def Clone(self):
        KokushiClassifier(self.shanten, self.pairs)

    def Draw(self, tileTypeId, previousTileCount):
        if previousTileCount == 0:
            self.shanten -= 1
        elif previousTileCount == 1:
            if self.__pairs == 0:
                self.shanten -= 1
            self.__pairs += 1

    def Discard(self, tileTypeId, tileCountAfterDiscard):
        if tileCountAfterDiscard == 0:
            self.shanten += 1
        elif tileCountAfterDiscard == 1:
            self.__pairs -= 1
            if self.__pairs == 0:
                self.shanten += 1