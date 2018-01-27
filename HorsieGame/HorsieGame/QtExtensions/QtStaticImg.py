from PyQt5 import QtCore, QtGui, QtWidgets
import math, numpy as np

class QtStaticImage(QtWidgets.QGraphicsPixmapItem):
    _Asset = None

    def _init_(self, **kwargs):
        return super()._init_(**kwargs)

    def setAsset(self, path, width, height):
        self._Asset = QtGui.QPixmap(path).scaled(width, height);
        self.setPixmap(self._Asset);