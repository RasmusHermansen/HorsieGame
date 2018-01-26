from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from GameSettings import GameSettings as Settings

class BasicWidget(object):
    """ A basic widget, implement setupUi to decorate the widget """    


    def __init__(self):
        self.Widget = QWidget()
        # Set resolution
        self.Widget.setFixedHeight(Settings().Height);
        self.Widget.setFixedWidth(Settings().Width);

    def getWidget(self):
        return self.Widget

class DynamicWidget(BasicWidget):

    def __init__(self, widgetName):
        super().__init__();
        self.setupDynamicWindow(self.Widget, widgetName);

    def setupDynamicWindow(self, widget, widgetName):
        widget.setObjectName(widgetName)
        
        # Create mainView
        self.MainView = QtWidgets.QGraphicsView(widget)

        # Create sizeing policy for main view
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainView.sizePolicy().hasHeightForWidth())
        self.MainView.setSizePolicy(sizePolicy)

        # Set scrollbarPolicy
        self.MainView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.MainView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Set update to FullViewport (Removes all artifacts at the cost of lower performance but whatever)
        self.MainView.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        
        # Set name and margins
        self.MainView.setObjectName("MainView")
        self.MainView.setContentsMargins(0,0,0,0)

        # Set horizontal layout and add mainView
        self.horizontalLayout = QtWidgets.QHBoxLayout(widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("Layout")
        self.horizontalLayout.addWidget(self.MainView)

        # Define and set scene
        self.Scene = QtWidgets.QGraphicsScene(widget)
        self.Scene.setSceneRect(0,0,self.Widget.width(), self.Widget.height())
        self.MainView.setScene(self.Scene)
        QtCore.QMetaObject.connectSlotsByName(widget)
        
        # Retranslate ui
        self.retranslateUi(widget)

        # Set Anti aliasing based on settings
        if(Settings().AntiAliasing == 2):
            self.MainView.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        elif(Settings().AntiAliasing == 1):
            self.MainView.setRenderHint(QtGui.QPainter.Antialiasing)