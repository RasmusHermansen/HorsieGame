from Screens.BasicWidget import BasicWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

class Ui_QtMenuScreen(BasicWidget):

    def __init__(self, horsesChange, startGame):
        super().__init__()
        self.setupUi(self.Widget);
        self.In_HorsesNumber.valueChanged.connect(horsesChange)
        self.B_StartRun.clicked.connect(startGame)

    def SetPlayers(self, players, header):
        self.__PopulateTable(players, header, self.Tbl_Players)

    def SetHorses(self, horses, header):
        self.__PopulateTable(horses, header, self.Tbl_Horses)

    def __PopulateTable(self, data, header, table):
        table.setRowCount(len(data))
        table.setColumnCount(len(header))
        table.setHorizontalHeaderLabels(header)
        for rowNr, entry in enumerate(data):
            for colNr, value in enumerate(entry):
                table.setItem(rowNr,colNr,QTableWidgetItem(str(value)))

    def SetGameName(self, gameName):
        self.L_GameName.setText("Game name: " + gameName)

    def setupUi(self, QtMenuScreen):
        QtMenuScreen.setObjectName("QtMenuScreen")
        self.gridLayout = QtWidgets.QGridLayout(QtMenuScreen)
        self.gridLayout.setObjectName("gridLayout")
        self.L_Players = QtWidgets.QLabel(QtMenuScreen)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L_Players.sizePolicy().hasHeightForWidth())
        self.L_Players.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.L_Players.setFont(font)
        self.L_Players.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.L_Players.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.L_Players.setObjectName("L_Players")
        self.gridLayout.addWidget(self.L_Players, 0, 0, 1, 1)
        self.L_Bets = QtWidgets.QLabel(QtMenuScreen)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.L_Bets.setFont(font)
        self.L_Bets.setObjectName("L_Bets")
        self.gridLayout.addWidget(self.L_Bets, 0, 2, 1, 1)
        self.Tbl_Horses = QtWidgets.QTableWidget(QtMenuScreen)
        self.Tbl_Horses.setObjectName("Tbl_Horses")
        self.Tbl_Horses.setColumnCount(0)
        self.Tbl_Horses.setRowCount(0)
        self.gridLayout.addWidget(self.Tbl_Horses, 1, 1, 1, 1)
        self.Tbl_Players = QtWidgets.QTableWidget(QtMenuScreen)
        self.Tbl_Players.setObjectName("Tbl_Players")
        self.Tbl_Players.setColumnCount(0)
        self.Tbl_Players.setRowCount(0)
        self.gridLayout.addWidget(self.Tbl_Players, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.L_Horses = QtWidgets.QLabel(QtMenuScreen)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.L_Horses.setFont(font)
        self.L_Horses.setObjectName("L_Horses")
        self.horizontalLayout.addWidget(self.L_Horses)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.In_HorsesNumber = QtWidgets.QSpinBox(QtMenuScreen)
        self.In_HorsesNumber.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.In_HorsesNumber.setMaximum(9)
        self.In_HorsesNumber.setMinimum(2)
        self.In_HorsesNumber.setObjectName("In_HorsesNumber")
        self.horizontalLayout.addWidget(self.In_HorsesNumber)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.B_StartRun = QtWidgets.QPushButton(QtMenuScreen)
        self.B_StartRun.setObjectName("B_StartRun")
        self.gridLayout.addWidget(self.B_StartRun, 2, 2, 1, 1)
        self.L_GameName = QtWidgets.QLabel(QtMenuScreen)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.L_GameName.setFont(font)
        self.L_GameName.setAlignment(QtCore.Qt.AlignCenter)
        self.L_GameName.setObjectName("L_GameName")
        self.gridLayout.addWidget(self.L_GameName, 2, 0, 1, 2)

        self.retranslateUi(QtMenuScreen)
        QtCore.QMetaObject.connectSlotsByName(QtMenuScreen)

    def retranslateUi(self, QtMenuScreen):
        _translate = QtCore.QCoreApplication.translate
        self.L_Players.setText(_translate("QtMenuScreen", "Players"))
        self.L_Bets.setText(_translate("QtMenuScreen", "Bets"))
        self.L_Horses.setText(_translate("QtMenuScreen", "Horses"))
        self.B_StartRun.setText(_translate("QtMenuScreen", "PushButton"))
        self.L_GameName.setText(_translate("QtMenuScreen", "GameName:"))