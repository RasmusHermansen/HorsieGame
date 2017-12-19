from PyQt5 import QtCore, QtGui, QtWidgets
import math, numpy as np

class QtBaseSprite(QtWidgets.QGraphicsPixmapItem):
    _spriteAsset = None
    _spriteIdxNumber = 0
    _spriteState = 0
    _spriteSpeed = 1
    _spriteCurrentDisplays = 0
    _terminalSprite = False
    _spriteActivelyManaged = True

    def _init_(self, **kwargs):
        return super()._init_(**kwargs)

    def setSpriteSpeed(self, speed):
        if(speed < 1):
            speed = 1
        else:
            speed = round(speed)
        self._spriteSpeed = speed

    def changeSpriteState(self, newState, isTerminal = False):
        self._spriteState = newState
        self._spriteActivelyManaged = True
        self._terminalSprite = isTerminal

    def setSpriteAsset(self, path, itemWidth = 64, itemHeight = 64):
        # Load entire sprite
        self._spriteAsset = QtGui.QPixmap(path)
        self._InitSprite(itemWidth, itemHeight)

    def _InitSprite(self, itemWidth, itemHeight):
        # Set initial values
        self._spriteItemWidth = itemWidth
        self._spriteItemHeight = itemHeight
        # Resolve maximum possible Idx and State
        self._maxSpriteIdxNumber = math.floor(self._spriteAsset.width()/self._spriteItemWidth)
        self._maxSpriteState = math.floor(self._spriteAsset.height()/self._spriteItemHeight)

    def _UpdateSprite(self):
        # Copy new SpriteItem
        self.setPixmap(self._spriteAsset.copy(
            self._spriteIdxNumber*self._spriteItemWidth,self._spriteState*self._spriteItemHeight,self._spriteItemWidth,self._spriteItemHeight))
        # Increment Idx
        self._spriteIdxNumber += 1
        if(self._spriteIdxNumber == self._maxSpriteIdxNumber):
            if(self._terminalSprite):
                self._spriteActivelyManaged = False
            else:
                self._spriteIdxNumber = 0

    def paint(self, QPainter, QStyleOptionGraphicsItem, QWidget):
        if(self._spriteAsset != None and self._spriteActivelyManaged):
            self._spriteCurrentDisplays += 1
            if (self._spriteCurrentDisplays >= self._spriteSpeed):
                self._UpdateSprite()
                self._spriteCurrentDisplays = 0
        return super().paint(QPainter, QStyleOptionGraphicsItem, QWidget)


class QtDynLenSprite(QtBaseSprite):
    _maxSpriteIdxNumberByState = []

    def _EmptySpriteItem(self, img, yPos, xPos, width, height):
        #top left to bot right
        for offset in np.arange(1,width,2):
            if(QtGui.qAlpha(img.pixel(xPos + offset,yPos + offset)) != 0):
                return False
        #bottom left to top right
        for offset in np.arange(1,width,2):
            if(QtGui.qAlpha(img.pixel(xPos + offset,yPos + height - offset)) != 0):
                return False
        return True

    def changeSpriteState(self, newState, isTerminal = False):
        self._maxSpriteIdxNumber = self._maxSpriteIdxNumberByState[newState]
        return super().changeSpriteState(newState, isTerminal)

    def _InitSprite(self, itemWidth, itemHeight):
        # Determine 
        self._spriteItemWidth = itemWidth
        self._spriteItemHeight = itemHeight
        # Resolve maximum possible Idx and State
        self._maxSpriteIdxNumber = math.floor(self._spriteAsset.width()/self._spriteItemWidth)
        self._maxSpriteState = math.floor(self._spriteAsset.height()/self._spriteItemHeight)

        # Transform QPixMap to QImage to process
        img = self._spriteAsset.toImage()
        # Check if any states has less animations
        for state in range(0,self._maxSpriteState):
            for spriteIdx in range(0,self._maxSpriteIdxNumber):
                if(self._EmptySpriteItem(img, state*itemHeight, spriteIdx*itemWidth, itemWidth, itemHeight)):
                    self._maxSpriteIdxNumberByState.append(spriteIdx)
                    break;
            if(len(self._maxSpriteIdxNumberByState) < state + 1):
                self._maxSpriteIdxNumberByState.append(self._maxSpriteIdxNumber)

    def _UpdateSprite(self):
        # Copy new SpriteItem
        self.setPixmap(self._spriteAsset.copy(
            self._spriteIdxNumber*self._spriteItemWidth,self._spriteState*self._spriteItemHeight,self._spriteItemWidth,self._spriteItemHeight))
        # Increment Idx
        self._spriteIdxNumber += 1
        if(self._spriteIdxNumber == self._maxSpriteIdxNumber):
            if(self._terminalSprite):
                self._spriteActivelyManaged = False
            else:
                self._spriteIdxNumber = 0
