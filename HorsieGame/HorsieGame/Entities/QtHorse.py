from Entities.Horse import Horse
from PyQt5 import QtGui, QtWidgets, QtCore
import random


class QtHorse(Horse):
        
    def __init__(self, name, KnotPoints, KnotValues, Scene):
        # Instantiate BaseHorse
        super().__init__(name, KnotPoints, KnotValues)

        self.Finished = False
        self.FinishT = 9999

        # Create Horse Object (Gif)
        self.Obj = QtWidgets.QLabel()
        self.Gif = QtGui.QMovie(self._GetHorseAsset())
        # Make label background transparent
        self.Obj.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.Obj.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Instantiate
        self.Obj.setObjectName(self.Name + "_gif")
        self.Obj.setMovie(self.Gif)
        self.Gif.start()            
        self.Widget = QtWidgets.QGraphicsProxyWidget()
        self.Widget.setWidget(self.Obj)
        # Add to scene
        Scene.addItem(self.Widget)

    def _GetHorseAsset(self):
        return random.choice(["Assets/Horses/WhiteHorse.gif", "Assets/Horses/BlackHorse.gif", "Assets/Horses/JihadHorse.gif"])