from log_hand_analyzer import LogHandAnalyzer
from analysis_utils import convertHandToTenhouString
from shanten import calculateMinimumShanten
from collections import defaultdict, Counter

class Dama(LogHandAnalyzer):
    def __init__(self):
        super().__init__()
        self.counts = defaultdict(Counter)
        self.damas = defaultdict(Counter)
        self.ignore = [False, False, False, False]
        self.has_riichi = [False, False, False, False]
        self.visible_tiles = [0] * 34

    def RoundStarted(self, init):
        super().RoundStarted(init)
        self.ignore = [False, False, False, False]
        self.has_riichi = [False, False, False, False]
        self.visible_tiles = [0] * 34

    def TileDiscarded(self, who, tile, tsumogiri, element):
        super().TileDiscarded(who, tile, tsumogiri, element)

        self.visible_tiles[tile] += 1

        if self.calculators[who].meldCount > 0 or self.ignore[who]: return

        shanten = self.calculators[who].Shanten()

        if shanten == 0:
            self.ignore[who] = True
            ukeire = self.calculators[who].GetUkeIreFor13()
            
            total_ukeire = 0
            for tile in ukeire:
                total_ukeire += ukeire[tile] - self.visible_tiles[tile]
                
            total_ukeire = min(total_ukeire, 13)

            self.counts[len(self.discards[who])][total_ukeire] += 1
            if not self.has_riichi[who]:
                self.damas[len(self.discards[who])][total_ukeire] += 1

    def TileCalled(self, who, tiles, element):
        super().TileCalled(who, tiles, element)
        for i in range(1, len(tiles)):
            self.visible_tiles[tiles[i]] += 1

    def RiichiCalled(self, who, step, element):
        super().RiichiCalled(who, step, element)
        self.has_riichi[who] = True
        if step == 2:
            self.end_round = True

    def PrintResults(self):
        with open("./results/DamaCounts.csv", "w", encoding="utf8") as f:
            f.write("Turn,0,1,2,3,4,5,6,7,8,9,10,11,12,13+\n")

            for i in range(1,21):
                f.write("%d," % i)
                for j in range(14):
                    f.write("%d," % self.counts[i][j])
                f.write("\n")

        with open("./results/DamaDamas.csv", "w", encoding="utf8") as f:
            f.write("Turn,0,1,2,3,4,5,6,7,8,9,10,11,12,13+\n")

            for i in range(21):
                f.write("%d," % i)
                for j in range(14):
                    f.write("%d," % self.damas[i][j])
                f.write("\n")