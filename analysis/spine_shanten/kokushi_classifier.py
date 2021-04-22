class KokushiClassifier():
    def __init__(self, shanten = 14, pairs = 1):
        self.shanten = 14
        self.__pairs = 1

    def Clone(self):
        KokushiClassifier(self.shanten, self.pairs)

    def Draw(self, tileTypeId, previousTileCount):
        # (1 << x & 0b100000001100000001100000001) >> x | (x + 5) >> 5
        # 1 if the tileType is a terminal or honor, else 0
        r = (1 << tileTypeId & 0b100000001100000001100000001) >> tileTypeId | (tileTypeId + 5) >> 5

        # TODO I suspect this can be simplified

        # 1 if previousTileCount < 2, else 0
        s = (previousTileCount ^ 2) >> 1 & r
        # 1 if previousTileCount == 1, else 0
        p = previousTileCount & s
        # 1 if no pair was added or there were no pairs before, else 0
        t = (self.__pairs | ~p) & s
        self.__pairs <<= p
        self.shanten -= t

    def Discard(self, tileTypeId, tileCountAfterDiscard):
        # (1 << x & 0b100000001100000001100000001) >> x | (x + 5) >> 5
        # 1 if the tileType is a terminal or honor, else 0
        r = (1 << tileTypeId & 0b100000001100000001100000001) >> tileTypeId | (tileTypeId + 5) >> 5

        # TODO I suspect this can be simplified

        # 1 if tileCountAfterDiscard < 2, else 0
        s = (tileCountAfterDiscard ^ 2) >> 1 & r
        # 1 if tileCountAfterDiscard == 1, else 0
        p = tileCountAfterDiscard & s
        self.__pairs >>= p
        # 1 if no pair was removed or there were at least two pairs before, else 0
        t = (self.__pairs | ~p) & s
        self.shanten += t