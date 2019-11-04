from scipy import interpolate
import random


class Horse(object):

    def __init__(self,name, id, KnotPoints, KnotValues):
        # Den fucking hest
        self.KnotPoints = KnotPoints
        self.KnotValues = [knot + random.normalvariate(0,2) for knot in KnotValues]
        self.MaxT = max(KnotPoints)
        self.MaxTSpeed = KnotValues[len(KnotValues)-1]
        self.t = 0
        self.Id = id
        self.Name = name
        self.tck = interpolate.splrep(KnotPoints,KnotValues,s=0) 

        super().__init__()

    def Run(self, T):
        distance = interpolate.splint(self.t, T, self.tck) if (T < self.MaxT) else self.MaxTSpeed*(T - self.t)
        self.t = T
        return distance

      

