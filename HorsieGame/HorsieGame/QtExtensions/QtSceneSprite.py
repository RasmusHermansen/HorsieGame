from PyQt5 import QtCore, QtGui, QtWidgets
import math

class QtSceneSprite(QtWidgets.QGraphicsPixmapItem):
    __spriteAsset = None
    __spriteIdxNumber = 0
    __spriteState = 0
    __spriteSpeed = 1
    __spriteCurrentDisplays = 0
    __terminalSprite = False
    __spriteActivelyManaged = True

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def setSpriteSpeed(self, speed):
        if(speed < 1):
            speed = 1
        else:
            speed = round(speed)
        self.__spriteSpeed = speed

    def changeSpriteState(self, newState, isTerminal = False):
        if(self.__spriteAsset == None):  
            raise BaseException("No SpriteAsset set (setSpriteAsset), cannot change SpriteState")
        if(self.__maxSpriteState < newState):
            raise Exception("New SpriteState is impossible with the given sizeing and spriteAsset (out of bounds)")
        self.__spriteState = newState
        self.__terminalSprite = isTerminal

    def setSpriteAsset(self, path, itemWidth = 64, itemHeight = 64):
        # Load entire sprite
        self.__spriteAsset = QtGui.QPixmap(path)
        # Set initial values
        self.__spriteItemWidth = itemWidth
        self.__spriteItemHeight = itemHeight
        # Resolve maximum possible Idx and State
        self.__maxSpriteIdxNumber = math.floor(self.__spriteAsset.width()/self.__spriteItemWidth)
        self.__maxSpriteState = math.floor(self.__spriteAsset.height()/self.__spriteItemHeight)

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget):
        if(self.__spriteAsset != None and self.__spriteActivelyManaged):
            self.__spriteCurrentDisplays += 1
            if (self.__spriteCurrentDisplays == self.__spriteSpeed):
                # Copy new SpriteItem
                self.setPixmap(self.__spriteAsset.copy(
                    self.__spriteIdxNumber*self.__spriteItemWidth,self.__spriteState*self.__spriteItemHeight,self.__spriteItemWidth,self.__spriteItemHeight))
                # Reset Display (Speed counter)
                self.__spriteCurrentDisplays = 0
                # Increment Idx
                self.__spriteIdxNumber += 1
                if(self.__spriteIdxNumber == self.__maxSpriteIdxNumber):
                    if(not self.__terminalSprite):
                        self.__spriteIdxNumber = 0
                    else:
                        self.__spriteActivelyManaged = False
        return super().paint(QPainter, QStyleOptionGraphicsItem, QWidget)