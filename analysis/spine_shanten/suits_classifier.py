from spine_shanten.resource import Transitions, Lookup

SuitFirstPhase = Transitions("SuitFirstPhase.txt")
SuitSecondPhase0 = Transitions("SuitSecondPhase0.txt")
SuitSecondPhase1 = Transitions("SuitSecondPhase1.txt")
SuitSecondPhase2 = Transitions("SuitSecondPhase2.txt")
SuitSecondPhase3 = Transitions("SuitSecondPhase3.txt")
SuitSecondPhase4 = Transitions("SuitSecondPhase4.txt")
SuitBase5Lookup = Lookup("suitArrangementsBase5NoMelds.dat")
SuitSecondPhases = (
    SuitSecondPhase0,
    SuitSecondPhase1,
    SuitSecondPhase2,
    SuitSecondPhase3,
    SuitSecondPhase4
)

class SuitClassifier():
    def __init__(self):
        self._meldCount = 0
        self._entry = 0
        self._secondPhase = SuitSecondPhase0

    def Clone(self):
        s = SuitClassifier()
        s._entry = self._entry
        s._meldCount = self._meldCount
        s._secondPhase = self._secondPhase
        return s

    def SetMelds(self, melds):
        current = 0
        self._meldCount = 0
        for i in range(5):
            m = melds & 0b111111
            if m != 0:
                current = SuitFirstPhase[current + m]
                melds >>= 6
                self._meldCount += 1
            else: break
        self._entry = SuitFirstPhase[current]
        self._secondPhase = SuitSecondPhases[self._meldCount]

    def GetValue(self, tiles, suit, base5Hashes):
        offset = suit * 9
        if self._meldCount == 0:
            return SuitBase5Lookup[base5Hashes[suit]]

        _secondPhase = self._secondPhase

        if self._meldCount == 1:
            current = self._entry
            current = _secondPhase[current + tiles[offset + 0]]
            current = _secondPhase[current + tiles[offset + 1]]
            current = _secondPhase[current + tiles[offset + 2]]
            current = _secondPhase[current + tiles[offset + 3]] + 11752
            current = _secondPhase[current + tiles[offset + 4]] + 30650
            current = _secondPhase[current + tiles[offset + 5]] + 55952
            current = _secondPhase[current + tiles[offset + 6]] + 80078
            current = _secondPhase[current + tiles[offset + 7]] + 99750
            return _secondPhase[current + tiles[offset + 8]]
        
        if self._meldCount == 2:
            current = self._entry
            current = _secondPhase[current + tiles[offset + 0]]
            current = _secondPhase[current + tiles[offset + 1]]
            current = _secondPhase[current + tiles[offset + 2]] + 22358
            current = _secondPhase[current + tiles[offset + 3]] + 54162
            current = _secondPhase[current + tiles[offset + 4]] + 90481
            current = _secondPhase[current + tiles[offset + 5]] + 120379
            current = _secondPhase[current + tiles[offset + 6]] + 139662
            current = _secondPhase[current + tiles[offset + 7]] + 150573
            return _secondPhase[current + tiles[offset + 8]]
        
        if self._meldCount == 3:
            current = self._entry
            current = _secondPhase[current + tiles[offset + 0]]
            current = _secondPhase[current + tiles[offset + 1]] + 24641
            current = _secondPhase[current + tiles[offset + 2]] + 50680
            current = _secondPhase[current + tiles[offset + 3]] + 76245
            current = _secondPhase[current + tiles[offset + 4]] + 93468
            current = _secondPhase[current + tiles[offset + 5]] + 102953
            current = _secondPhase[current + tiles[offset + 6]] + 107217
            current = _secondPhase[current + tiles[offset + 7]] + 108982
            return _secondPhase[current + tiles[offset + 8]]
        
        if self._meldCount == 4:
            current = self._entry
            current = _secondPhase[current + tiles[offset + 0]]
            current = _secondPhase[current + tiles[offset + 1]]
            current = _secondPhase[current + tiles[offset + 2]]
            current = _secondPhase[current + tiles[offset + 3]]
            current = _secondPhase[current + tiles[offset + 4]]
            current = _secondPhase[current + tiles[offset + 5]]
            current = _secondPhase[current + tiles[offset + 6]]
            current = _secondPhase[current + tiles[offset + 7]]
            return _secondPhase[current + tiles[offset + 8]]

        return 0

