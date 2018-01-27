from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QHoverEvent
from Screens.BasicWidget import DynamicWidget
from QtExtensions import QtSprites, QtStaticImg, QtTrajectory, QtLinkText, QtAnimationEngine;
from GameSettings import GameSettings as Settings
from enum import Enum

class widgetMode(Enum):
    WelcomeScreen = 1;
    MenuScreen = 2;

class Ui_QtMainScreen(DynamicWidget):

    def __init__(self, mode):
        super().__init__("Main")

        self.AnimationEngine = QtAnimationEngine.QtAnimationEngine();

        self.mode = mode;
        self._InitializeScene();

        self.StartTimer(10);

    def _Update(self):
        # Update animation and check if done
        self.AnimationEngine.update();

    def _InitializeScene(self):
        if(self.mode == widgetMode.WelcomeScreen):
            self._InitializeWelcome()

#region WelcomeScreen
    def _InitializeWelcome(self):
        #Set background
        self.backGround = QtStaticImg.QtStaticImage()
        self.backGround.setAsset("Assets/MenuBackgrounds/Welcome.jpg",self.Scene.width(),self.Scene.height())
        self.Scene.addItem(self.backGround);

        # Create clickable text
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(32)
        linkText = QtLinkText.QtLinkText(self.Scene, "Start a Game", self.StartNewGame, font) 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(linkText,self.Scene.width()/2,-10,self.Scene.width()/2,self.Scene.height()/3,250))

        # Create 'Headline' text
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(48)
        headline = QtLinkText.QtSimpleText(self.Scene, "Welcome", font) 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(headline,self.Scene.width()/2,-50,self.Scene.width()/2,self.Scene.height()/3-50,250))

#endregion


#region TransitionToMenu
    def StartNewGame(self):
        pass


#endregion

#region MenuScreen

#endregion