from Entities import VisualObject
from scipy import interpolate


class Horse(VisualObject):
    def __init__(self, x, y, png, KnotPoints, KnotValues):
        # Den fucking hest
        self.KnotPoints = KnotPoints
        self.KnotValues = KnotValues
        self.t = 0
        self.tck = interpolate.splrep(KnotPoints,KnotValues,s=0)
     
        super().__init__(x,y,png)

    def Run(self, T):
        self.x += interpolate.splint(self.t, T, self.tck)
        self.t = T


      

