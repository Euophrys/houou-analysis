from log_hand_analyzer import LogHandAnalyzer
from analysis_utils import convertHandToTenhouString
from shanten import calculateMinimumShanten

lookup = (
    1,2,3,4,5,6,7,8,9,
    11,12,13,14,15,16,17,18,19,
    21,22,23,24,25,26,27,28,29,
    31,32,33,34,35,36,37
)

class ShantenTest(LogHandAnalyzer):
    def __init__(self):
        super().__init__()

    def RoundStarted(self, init):
        super().RoundStarted(init)
        
        for i in range(4):
            hand = [0] * 38

            for tile in range(34):
                hand[lookup[tile]] = self.calculators[i].inHandByType[tile]

            old_shanten = calculateMinimumShanten(hand)
            spine_shanten = self.calculators[i].Shanten()

            if old_shanten != spine_shanten:
                print("old: %d, spine: %d, %s" % (old_shanten, spine_shanten, self.calculators[i]))

        self.end_round = True

    def PrintResults(self):
        pass