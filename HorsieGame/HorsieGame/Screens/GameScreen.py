from PyQt5 import QtCore, QtGui, QtWidgets
from Screens.BasicWidget import BasicWidget
from Entities.QtHorse import QtHorse
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPen
from GameSettings import GameSettings as Settings
import random

class Ui_QtGameScreen(BasicWidget):
    
    def __init__(self, postGameCB, horses):
        super().__init__()


        self._constructBackground()
        self._constructHorses(horses)
        self._postGameCB = postGameCB
        self.timer = QTimer(self.Widget)
        self.timer.timeout.connect(self._Update)
        self.FinishLineActive = False

    def _constructHorses(self, horses):
        # Resolve Knots
        knotIncrement = 30;
        knotPoints = [0, knotIncrement, knotIncrement*2, knotIncrement*3, knotIncrement*4, knotIncrement*5]
        # Instantiate horses
        self.HorseEntities = []

        for i, horsie in enumerate(horses):
            knotvalues = [horsie['Knot1'],horsie['Knot2'],horsie['Knot3'],horsie['Knot4'],horsie['Knot5'],horsie['Knot1']]
            horse = QtHorse(horsie['Name'],knotPoints,knotvalues, self.Scene)
            self.HorseEntities.append(horse)
            horse.Widget.setPos(0, round(0.6*self.Scene.height()) + i*25)

    def _constructBackground(self):
        self.BackGroundSpeed = -10

        pen = QPen()
        # Earth
        dustColor = QColor(120,72,0)
        self.Scene.addRect(0,round(0.6*self.Scene.height()),self.Scene.width(),round(0.4*self.Scene.height()),pen,dustColor)
        # Sky
        skyColor = QColor(14,171,245)
        self.Scene.addRect(0,0,self.Scene.width(),round(0.6*self.Scene.height()),pen,skyColor)
        # TRect
        self.TLabel = self.Scene.addText("")
        self.TLabel.setPos(100,100)

        self.BackGroundEntities = []
        # Add 7 trees
        for i in range(0,25):
            # Create Horse Object (Gif)
            treeObj = QtWidgets.QLabel()
            # Make label background transparent
            treeObj.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            treeObj.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            # Instantiate
            treeObj.setPixmap(QtGui.QPixmap("Assets/Background/treeOne.png"))
            # Initialize proxy widgets
            widget = QtWidgets.QGraphicsProxyWidget()
            widget.setWidget(treeObj)
            widget.setPreferredHeight(treeObj.height())
            widget.setPreferredWidth(treeObj.width())
            # Add to scene
            self.Scene.addItem(widget)
            # Set starting position
            widget.setPos(random.randint(0,self.Scene.width()+widget.preferredWidth()*2), round(0.6*self.Scene.height())-widget.preferredHeight())
            # Save in background entitites
            self.BackGroundEntities.append(widget)


    def _ProcessBackground(self):
        for item in self.BackGroundEntities:
            if(item.pos().x() < -item.preferredWidth()):
                item.moveBy(self.Scene.width()+item.preferredWidth()*3,0)
            else:
                item.moveBy(self.BackGroundSpeed,0)


    def _Update(self):
        self.T += 1
        self.TLabel.setPlainText(str(self.T))
        self._MoveHorses()
        self._ProcessBackground()
        self._CheckFinish()

    def HandleHorseFinish(self, place, name):
        font = QtGui.QFont()
        font.setBold(True)
        if(place == 1):
            color = QColor(255, 215, 0)
            displacement = 0
            font.setPointSize(72)
        elif(place == 2):
            color = QColor(192, 192, 192)
            displacement = 90
            font.setPointSize(66)
        elif(place == 3):
            color = QColor(205, 127, 50)
            displacement = 180
            font.setPointSize(60)
        else:
            color = QColor(0, 0, 0)
            displacement = 265 + (place - 4)*80
            font.setPointSize(56)

        placementLabel = self.Scene.addText(str(place) + ": " + name, font)
        placementLabel.setDefaultTextColor(color)
        placementLabel.setPos(self.Scene.width()/3, 150 + displacement)

    def _CreateReturnToMenuButton(self):
        returnLabel = QtWidgets.QPushButton()
        returnLabel.setObjectName("B_ReturnToMenu")
        returnLabel.setText("Return to Menu")
        returnLabel.clicked.connect(lambda : self._postGameCB(self.HorsesFinished))
        # Initialize proxy widgets
        widget = QtWidgets.QGraphicsProxyWidget()
        widget.setWidget(returnLabel)
        # Add to scene
        self.Scene.addItem(widget)
        # Set starting position
        widget.setPos(self.Scene.width()/2-returnLabel.width()/2, 0.85*self.Scene.height())

    def _DisplayWinningPhoto(self):
        # Initialise Label
        photoObj = QtWidgets.QLabel()
        photoObj.setPixmap(self.FinishLinePhotos[0])
        photoObj.setStyleSheet("border: 2px solid")
        # Initialize proxy widgets
        widget = QtWidgets.QGraphicsProxyWidget()
        widget.setWidget(photoObj)
        # Add to scene
        self.Scene.addItem(widget)
        # Set starting position
        widget.setPos(50, 0.4*self.Scene.height())
        # Draw text above
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(32)
        textLabel = self.Scene.addText("Slowmo Recap", font)
        textLabel.setPos(50, 0.35*self.Scene.height())

        # Start slowmotion T
        self.timer.timeout.disconnect()
        self.T = 0
        self.timer.timeout.connect(lambda : self._ChangeWinningPhoto(photoObj))
        self.timer.start(500)

    def _ChangeWinningPhoto(self, photoObj):
        photoObj.setPixmap(self.FinishLinePhotos[self.T % len(self.FinishLinePhotos)])
        self.T += 1

    def _CheckFinish(self):
        if(self.FinishLineActive):
            # Compute finishline position
            finishLinexPos = self.FinishLineWidget.rect().x() + self.FinishLineWidget.rect().width() + self.FinishLineWidget.pos().x()

            # Check if horses crossed finishline
            for horse in self.HorseEntities:
                if not horse.Finished and horse.Widget.pos().x() + horse.Widget.preferredWidth() > finishLinexPos:
                    self.HorsesFinished[len(self.HorsesFinished)] = horse
                    horse.Finished = True
                    horse.FinishT = self.T
                    self.BackGroundSpeed = 0
                    self.HandleHorseFinish(len(self.HorsesFinished), horse.Name)

            # Check if all horses crossed finishline
            if len(self.HorsesFinished) == len(self.HorseEntities):
                    self.timer.stop()
                    self._DisplayWinningPhoto()
                    self._CreateReturnToMenuButton()

            # Move finishLine
            self.FinishLineWidget.moveBy(self.BackGroundSpeed,0)
        else:
            for horse in self.HorseEntities:
                if horse.Widget.pos().x() > self.Scene.width()*0.65:
                    pen = QPen()
                    # red
                    redColor = QColor(225,0,0)
                    self.FinishLineWidget = self.Scene.addRect(self.Scene.width(),round(0.6*self.Scene.height()),3,round(0.4*self.Scene.height()),pen,redColor)
                    self.FinishLineActive = True
                    self.HorsesFinished = {}
                    # Start Capture Finish line
                    self.FinishLinePhotos = []
                    self.timer.timeout.connect(self._GrapFinishLinePhoto)

    def _GrapFinishLinePhoto(self):
        # target rect
        targetRect = self.FinishLineWidget.rect().adjusted(-500,-60,-150,-75)
        self.FinishLinePhotos.append(self.GameView.grab(targetRect.toRect()))

        if(len(self.FinishLinePhotos) > 2 and len(self.HorsesFinished) == 0):
            self.FinishLinePhotos.pop(0)
        if(len(self.HorsesFinished) > 2 and self.HorsesFinished[2].FinishT + 2 < self.T):
            self.timer.timeout.disconnect(self._GrapFinishLinePhoto)


    def _MoveHorses(self):
        for horse in self.HorseEntities:
            speed = horse.Run(self.T)
            # Adjust Horse gif speed
            horse.Gif.setSpeed(round(speed*20))
            # Horse.Run(t)
            horse.Widget.moveBy(speed,0)

    def RunGame(self):
        self.GameView.show()
        self.T = 0
        self.timer.start(100)   

    def getWidget(self):
        return super().getWidget()

    def setupUi(self, Game):
        Game.setObjectName("Game")
        Game.showFullScreen()
        self.horizontalLayout = QtWidgets.QHBoxLayout(Game)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("GameLayout")
        self.GameView = QtWidgets.QGraphicsView(Game)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GameView.sizePolicy().hasHeightForWidth())
        self.GameView.setSizePolicy(sizePolicy)
        self.GameView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GameView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GameView.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.GameView.setObjectName("GameView")
        self.GameView.setContentsMargins(0,0,0,0)
        self.horizontalLayout.addWidget(self.GameView)
        self.Scene = QtWidgets.QGraphicsScene(Game)
        self.Scene.setSceneRect(0,0,self.Widget.width(), self.Widget.height())
        self.GameView.setScene(self.Scene)
        self.retranslateUi(Game)
        QtCore.QMetaObject.connectSlotsByName(Game)

        if(Settings().AntiAliasing == 2):
            self.GameView.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        elif(Settings().AntiAliasing == 1):
            self.GameView.setRenderHint(QtGui.QPainter.Antialiasing)

    def retranslateUi(self, Game):
        _translate = QtCore.QCoreApplication.translate
        Game.setWindowTitle(_translate("Game", "Game"))


