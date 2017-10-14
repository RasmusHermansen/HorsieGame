from Entities import VisualObject
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


class Horse(object):
    def __init__(self,KnotPoints,KnotValues,position):
        # Den fucking hest
        self.KnotPoints = KnotPoints
        self.KnotValues = KnotValues
        self.position = position
     
    def Run(self):
        tck = interpolate.splrep(self.KnotPoints,self.KnotValues,s=0)
        self.position += interpolate.splint(0, self.KnotPoints[2], tck)
      

Tarok = Horse([0,0.5,0.67,0.98,1.2], [1,1.2,0.78,0.42,1.1], 0)
Tarok.Run()

print (Tarok.position)