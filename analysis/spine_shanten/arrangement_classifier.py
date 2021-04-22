from spine_shanten.resource import Transitions
Arrangement = Transitions("ArrangementTransitions.txt")

def Classify(values):
    current = Arrangement[values[0]]
    current = Arrangement[current + values[1]]
    current = Arrangement[current + values[2]]
    current = Arrangement[current + values[3]]
    return current