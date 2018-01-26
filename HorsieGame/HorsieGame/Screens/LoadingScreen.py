from PyQt5 import QtCore, QtGui
from Screens.BasicWidget import BasicWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QPushButton, QWidget

class Ui_QtLoadingScreen(BasicWidget):


    def __init__(self):
        super().__init__()
        self.setupUi(self.Widget);

    def getWidget(self):
        self.L_LoadingMsg.setText("Loading")
        return super().getWidget()

    def ChangeStatus(self, msg):
        self.L_LoadingMsg.setText(msg)

    # SETUP UI CODE

    def setupUi(self, QtWelcomeScreen):
        QtWelcomeScreen.setObjectName("QtWelcomeScreen")
        self.horizontalLayout = QHBoxLayout(QtWelcomeScreen)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        
        # Loading gif
        self.L_Loading = QLabel(QtWelcomeScreen)
        gif = QtGui.QMovie("Assets/General/Loading.gif")
        self.L_Loading.setObjectName("L_Loading")
        self.L_Loading.setMovie(gif)
        gif.start()

        self.verticalLayout.addWidget(self.L_Loading)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)

        # Status label
        font = QtGui.QFont()
        font.setBold(True)
        self.L_LoadingMsg = QLabel(QtWelcomeScreen)
        self.L_LoadingMsg.setObjectName("L_LoadingMsg")
        self.L_LoadingMsg.setFont(font)
        self.L_LoadingMsg.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.L_LoadingMsg)
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)

        QtCore.QMetaObject.connectSlotsByName(QtWelcomeScreen)


    # SETUP UI CODE OVER