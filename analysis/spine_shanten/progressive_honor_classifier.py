from spine_shanten.resource import Transitions
Transitions = Transitions("ProgressiveHonorStateMachine.txt")

class ProgressiveHonorClassifier():
    def __init__(self, current = 0):
        self.current = current

    def Clone(self):
        return ProgressiveHonorClassifier(self._current)

    def Draw(self, previousTiles, meldBit):
        action = previousTiles + (meldBit << 2) + 1
        self.current = Transitions[self.current + action]
        return Transitions[self.current]

    def Discard(self, tilesAfterDiscard, meldBit):
        action = tilesAfterDiscard + (meldBit << 2) + 6
        self.current = Transitions[self.current + action]
        return Transitions[self.current]

    def Pon(self, previousTiles):
        self.current = Transitions[self.current + previousTiles + 9]
        return Transitions[self.current]

    def Daiminkan(self):
        self.current = Transitions[self.current + 13]
        return Transitions[self.current]

    def Shouminkan(self):
        self.current = Transitions[self.current + 14]
        return Transitions[self.current]

    def Ankan(self):
        self.current = Transitions[self.current + 15]
        return Transitions[self.current]