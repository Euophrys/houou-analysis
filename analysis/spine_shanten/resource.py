import numpy

def Transitions(resourceName):
    fullResourceName = "./spine_shanten/data/%s" % resourceName
    with open(fullResourceName, "r", encoding="utf8") as f:
        lines = f.readlines()
        ints = [max(int(line), 0) for line in lines]
        return ints

def Lookup(resourceName):
    fullResourceName = "./spine_shanten/data/%s" % resourceName
    data = numpy.fromfile(fullResourceName, numpy.uint8)
    return data