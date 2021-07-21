from PyQt5 import QtCore, QtWidgets, QtGui


class QtSimpleText(QtWidgets.QGraphicsTextItem):
    ''' Enables centered = true '''

    Data = 0;

    def __init__(self, scene, text, font = QtGui.QFont(), centered = True,**kwargs):
        if (scene):
            super().__init__(**kwargs)
            self.setPlainText(text);
            self.setFont(font);
            scene.addItem(self);

    def pos(self):
        real = super().pos()
        real.setX(real.x()+self.boundingRect().width()/2)
        real.setY(real.y()+self.boundingRect().height()/2)
        return real

    def setPos(self, x, y):
        return super().setPos(x-self.boundingRect().width()/2, y-self.boundingRect().height()/2)

class QtLinkText(QtSimpleText):
    ''' Enables mousepress & hover Events '''

    def __init__(self, scene, text, onClick, font = QtGui.QFont(), centered = True,**kwargs):
        super().__init__(scene, text, font, centered, **kwargs)

        self.onClick = onClick;

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        self.onClick()
        return super().mousePressEvent(QGraphicsSceneMouseEvent)

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        self.setDefaultTextColor(QtGui.QColor(134, 188, 37))
        return super().hoverEnterEvent(QGraphicsSceneHoverEvent)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        self.setDefaultTextColor(QtGui.QColor(0, 0, 0))
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)

class QtRemoveableText(QtLinkText):
    ''' Enables mousepress & hover Events '''

    IsCleared = False

    def __init__(self, scene, text, onClick, font = QtGui.QFont(), centered = True,**kwargs):
        super().__init__(scene, text, onClick, font, centered, **kwargs)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        self.scene().removeItem(self)
        self.IsCleared = True
        return super().mousePressEvent(QGraphicsSceneMouseEvent)