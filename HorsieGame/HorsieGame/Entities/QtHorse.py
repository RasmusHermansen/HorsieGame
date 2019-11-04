from Entities.Horse import Horse
from QtExtensions.QtSprites import QtDynLenSprite
from PyQt5 import QtGui, QtWidgets, QtCore
import random


class QtHorse(Horse):
        
    def __init__(self, name, id, KnotPoints, KnotValues, Scene):
        # Instantiate BaseHorse
        super().__init__(name, id, KnotPoints, KnotValues)

        self.Finished = False
        self.FinishT = 9999

        # Create Horse Object
        self.Obj = QtDynLenSprite()
        # Make label background transparent
        horseData = self._GetHorseAsset(name);
        self.Obj.setSpriteAsset(horseData[0],horseData[1],horseData[2])
        self.Obj.setSpriteSpeed(2)
        # Add to scene
        Scene.addItem(self.Obj)

    def _GetHorseAsset(self, horseName):
        horses = {
            "Basic": ["Assets/Horses/Basic.png",303,222],
            "HeztBollah": ["Assets/Horses/Basic.png",303,222],
            "LeninHest": ["Assets/Horses/Basic.png",303,222],
            "XenoHorse": ["Assets/Horses/Basic.png",303,222]
        }
        return horses[horseName]