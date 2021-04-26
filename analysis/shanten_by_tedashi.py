from log_hand_analyzer import LogHandAnalyzer
from analysis_utils import convertTile
from collections import defaultdict, Counter

tile_types = [
    "1/9", "2/8", "3/7", "4/6", "5", "4/6", "3/7", "2/8", "1/9",
    "1/9", "2/8", "3/7", "4/6", "5", "4/6", "3/7", "2/8", "1/9",
    "1/9", "2/8", "3/7", "4/6", "5", "4/6", "3/7", "2/8", "1/9",
    "Z","Z","Z","Z","Z","Z","Z"
]

class ShantenByTedashi(LogHandAnalyzer):
    def __init__(self):
        super().__init__()
        self.counts = defaultdict(Counter)
        self.tenpais = defaultdict(Counter)
        self.shanten = defaultdict(Counter)

        self.counts_tedashi = defaultdict(Counter)
        self.tenpais_tedashi = defaultdict(Counter)
        self.tedashi = defaultdict(Counter)

        self.counts_type = defaultdict(Counter)
        self.tenpais_type = defaultdict(Counter)
        self.tedashi_type = defaultdict(Counter)

        self.tedashi_count = [0,0,0,0]

    def RoundStarted(self, init):
        super().RoundStarted(init)
        self.tedashi_count = [0,0,0,0]

    def TileDiscarded(self, who, tile, tsumogiri, element):
        super().TileDiscarded(who, tile, tsumogiri, element)

        shanten = self.calculators[who].Shanten()
        discards = len(self.discards[who])

        self.counts[discards][self.calculators[who].meldCount] += 1
        self.shanten[discards][self.calculators[who].meldCount] += shanten
        if shanten == 0:
            self.tenpais[discards][self.calculators[who].meldCount] += 1

        if tsumogiri or self.calculators[who].meldCount > 0: return
        
        self.tedashi_count[who] += 1
        self.counts_tedashi[discards][self.tedashi_count[who]] += 1
        self.tedashi[discards][self.tedashi_count[who]] += shanten

        tile_type = tile_types[tile]
        self.counts_type[discards][tile_type] += 1
        self.tedashi_type[discards][tile_type] += shanten

        if shanten == 0:
            self.tenpais_tedashi[discards][self.tedashi_count[who]] += 1
            self.tenpais_type[discards][tile_type] += 1

    def RiichiCalled(self, who, step, element):
        super().RiichiCalled(who, step, element)
        self.end_round = True
            
    def PrintResults(self):
        with open("./results/ShantenCounts.csv", "w") as c:
            with open("./results/ShantenShantens.csv", "w") as s:
                with open("./results/ShantenTenpais.csv", "w") as t:
                    c.write("Discard,Closed,1 Call,2 Calls,3 Calls\n")
                    s.write("Discard,Closed,1 Call,2 Calls,3 Calls\n")
                    t.write("Discard,Closed,1 Call,2 Calls,3 Calls\n")

                    for turn in range(1,19):
                        c.write("%d," % turn)
                        s.write("%d," % turn)
                        t.write("%d," % turn)
                        for melds in range(4):
                            c.write("%d," % self.counts[turn][melds])
                            s.write("%d," % self.shanten[turn][melds])
                            t.write("%d," % self.tenpais[turn][melds])
                        c.write("\n")
                        s.write("\n")
                        t.write("\n")
                            
        with open("./results/TedashiCounts.csv", "w") as c:
            with open("./results/TedashiShantens.csv", "w") as s:
                with open("./results/TedashiTenpais.csv", "w") as t:
                    c.write("Discard,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18\n")
                    s.write("Discard,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18\n")
                    t.write("Discard,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18\n")

                    for turn in range(1,19):
                        c.write("%d," % turn)
                        s.write("%d," % turn)
                        t.write("%d," % turn)
                        for tedashi in range(18):
                            c.write("%d," % self.counts_tedashi[turn][tedashi])
                            s.write("%d," % self.tedashi[turn][tedashi])
                            t.write("%d," % self.tenpais_tedashi[turn][tedashi])
                        c.write("\n")
                        s.write("\n")
                        t.write("\n")

        with open("./results/TedashiTypeCounts.csv", "w") as c:
            with open("./results/TedashiTypeShantens.csv", "w") as s:
                with open("./results/TedashiTypeTenpais.csv", "w") as t:
                    c.write("Discard,1/9,2/8,3/7,4/6,5,Honor\n")
                    s.write("Discard,1/9,2/8,3/7,4/6,5,Honor\n")
                    t.write("Discard,1/9,2/8,3/7,4/6,5,Honor\n")

                    for turn in range(1,19):
                        c.write("%d," % turn)
                        s.write("%d," % turn)
                        t.write("%d," % turn)
                        for tile_type in ("1/9","2/8","3/7","4/6","5","Z"):
                            c.write("%d," % self.counts_type[turn][tile_type])
                            s.write("%d," % self.tedashi_type[turn][tile_type])
                            t.write("%d," % self.tenpais_type[turn][tile_type])
                        c.write("\n")
                        s.write("\n")
                        t.write("\n")