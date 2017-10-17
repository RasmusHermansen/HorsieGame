from PyQt5 import QtCore, QtGui, QtWidgets
from Screens.BasicWidget import BasicWidget
from Entities.Horse import Horse
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPen
import random

class Ui_QtGameScreen(BasicWidget):
    
    def __init__(self, postGameCB, horses):
        super().__init__()

        self.HorseGifs = ["Assets/Horses/Base.gif", "Assets/Horses/BlackHorse.gif"]

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
        for horsie in horses:
            knotvalues = [horsie['Knot1'],horsie['Knot2'],horsie['Knot3'],horsie['Knot4'],horsie['Knot5'],horsie['Knot1']]
            self.HorseEntities.append(Horse(horsie['Name'],knotPoints,knotvalues))

        horsieNumber = 0;
        for horsie in self.HorseEntities:
            horsie.Finished = False
            horsieNumber += 1;
            # Create Horse Object (Gif)
            horsie.Obj = QtWidgets.QLabel()
            horsie.Gif = QtGui.QMovie(random.choice(self.HorseGifs))
            # Make label background transparent
            horsie.Obj.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            horsie.Obj.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            # Instantiate
            horsie.Obj.setObjectName(horsie.Name + "_gif")
            horsie.Obj.setMovie(horsie.Gif)
            horsie.Gif.start()
            # Initialize proxy widgets
            horsie.Widget = QtWidgets.QGraphicsProxyWidget()
            horsie.Widget.setWidget(horsie.Obj)
            # Add to scene
            self.Scene.addItem(horsie.Widget)
            # Set starting position
            horsie.Widget.setPos(0, round(0.6*self.Scene.height()) + horsieNumber*25)

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

    def _WriteHorseFinished(self, place, name):
        font = QtGui.QFont()
        font.setBold(True)
        if(place == 1):
            color = QColor(255, 215, 0)
            font.setPointSize(150)
        elif(place == 2):
            color = QColor(192, 192, 192)
            font.setPointSize(120)
        elif(place == 3):
            color = QColor(205, 127, 50)
            font.setPointSize(90)
        else:
            color = QColor(0, 0, 0)
            font.setPointSize(72)

        placementLabel = self.Scene.addText(str(place) + ": " + name, font)
        placementLabel.setDefaultTextColor(color)
        placementLabel.setPos(self.Scene.width()/2-placementLabel.textWidth(), 200 + 60*place)

    def _CreateReturnToMenuButton(self):
        returnLabel = self.Scene.addText("Return to Menu")
        returnLabel.setPos(self.Scene.width()/2-returnLabel.textWidth(), self.Scene.height()*0.75)

    def _CheckFinish(self):
        if(self.FinishLineActive):
            # Compute finishline position
            finishLinexPos = self.FinishLineWidget.rect().x() + self.FinishLineWidget.rect().width() + self.FinishLineWidget.pos().x()

            # Check if horses crossed finishline
            for horse in self.HorseEntities:
                if not horse.Finished and horse.Widget.pos().x() + horse.Widget.preferredWidth() > finishLinexPos:
                    self.HorsesFinished[len(self.HorsesFinished)] = horse.Name
                    horse.Finished = True
                    self.BackGroundSpeed = 0
                    self._WriteHorseFinished(len(self.HorsesFinished), horse.Name)

            # Check if all horses crossed finishline
            if len(self.HorsesFinished) == len(self.HorseEntities):
                    self.timer.stop()
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
        #self.GameView.setInteractive(False)
        self.GameView.setObjectName("GameView")
        self.GameView.setContentsMargins(0,0,0,0)
        self.horizontalLayout.addWidget(self.GameView)
        self.Scene = QtWidgets.QGraphicsScene(Game)
        self.Scene.setSceneRect(0,0,self.Widget.width(), self.Widget.height())
        self.GameView.setScene(self.Scene)

        self.retranslateUi(Game)
        QtCore.QMetaObject.connectSlotsByName(Game)

    def retranslateUi(self, Game):
        _translate = QtCore.QCoreApplication.translate
        Game.setWindowTitle(_translate("Game", "Game"))


