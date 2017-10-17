from PyQt5 import QtCore, QtWidgets, QtGui


class QtLinkLabel(QtWidgets.QLabel):

    def __init__(self, parent, baseColor = 'rgb(0,0,0)', hoverColor = 'rgb(255,255,0)'):
        QtWidgets.QLabel.__init__(self,parent)
        self.setMouseTracking(True)        
        self.baseColor = baseColor
        self.hoverColor = hoverColor
        self.setAlignment(QtCore.Qt.AlignCenter)

    def enterEvent(self, event):
        self.setStyleSheet("color:" + self.hoverColor)

    def leaveEvent(self, event):
        self.setStyleSheet("color:" + self.baseColor)
    
    def connectClick(self, event):
        self._clickable(self).connect(event);

    def _clickable(self,widget):

        class Filter(QtCore.QObject):
    
            clicked = QtCore.pyqtSignal()
        
            def eventFilter(self, obj, event):
        
                if obj == widget:
                    if event.type() == QtCore.QEvent.MouseButtonRelease:
                        if obj.rect().contains(event.pos()):
                            self.clicked.emit()
                            # The developer can opt for .emit(obj) to get the object within the slot.
                            return True
            
                return False
    
        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked