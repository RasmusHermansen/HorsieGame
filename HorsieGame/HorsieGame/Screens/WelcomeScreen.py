from PyQt5 import QtCore, QtGui
from Screens.BasicWidget import BasicWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QPushButton, QWidget
from QtExtensions.QtLinkLabel import QtLinkLabel

class Ui_QtWelcomeScreen(BasicWidget):


    def __init__(self, OnBtnPress):
        super().__init__()

        self.B_InitNewGame.connectClick(OnBtnPress)

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
        self.L_Welcome = QLabel(QtWelcomeScreen)
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.L_Welcome.setFont(font)
        self.L_Welcome.setObjectName("L_Welcome")
        self.L_Welcome.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.L_Welcome.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.verticalLayout.addWidget(self.L_Welcome)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.B_InitNewGame = QtLinkLabel(QtWelcomeScreen)
        self.B_InitNewGame.setObjectName("B_InitNewGame")
        self.B_InitNewGame.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.B_InitNewGame.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.verticalLayout.addWidget(self.B_InitNewGame)
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        spacerItem4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)

        self.Widget.setStyleSheet("border-image: url(Assets/MenuBackgrounds/Welcome.jpg)")

        self.retranslateUi(QtWelcomeScreen)
        QtCore.QMetaObject.connectSlotsByName(QtWelcomeScreen)

    def retranslateUi(self, QtWelcomeScreen):
        _translate = QtCore.QCoreApplication.translate
        QtWelcomeScreen.setWindowTitle(_translate("QtWelcomeScreen", "HorsieGame"))
        self.L_Welcome.setText(_translate("QtWelcomeScreen", "Welcome"))
        self.B_InitNewGame.setText(_translate("QtWelcomeScreen", "Start a game"))

    # SETUP UI CODE OVER