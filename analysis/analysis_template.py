from log_hand_analyzer import LogHandAnalyzer
from analysis_utils import convertTile
from collections import defaultdict, Counter

class AnalysisName(LogHandAnalyzer):
    def __init__(self):
        super().__init__()

    def PrintResults(self):
        with open("./results/Counts.csv", "w", encoding="utf8") as f:
            pass