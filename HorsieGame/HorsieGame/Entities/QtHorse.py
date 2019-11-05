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
            "Horse Team Six": ["Assets/Horses/Horse Team Six.png",310,230],
            "HimlerHorse": ["Assets/Horses/HimlerHorse.png",307,227],
            "Ленин лошадь": ["Assets/Horses/LeninHorse.png",304,250],
            "Klov Klux Klan": ["Assets/Horses/Klov Klux Klan.png",300,265],
            "XenoHorse": ["Assets/Horses/XenoHorse.png",336,177],
            "Donald Trav": ["Assets/Horses/Donald Trav.png",304,244]
        }
        return horses[horseName]