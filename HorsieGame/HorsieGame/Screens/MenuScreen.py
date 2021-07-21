from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QHoverEvent
from Screens.BasicWidget import DynamicWidget
from QtExtensions import QtSprites, QtStaticImg, QtTrajectory, QtLinkText, QtAnimationEngine;
from GameSettings import GameSettings as Settings
from enum import Enum
import random;

class widgetMode(Enum):
    WelcomeScreen = 1;
    MenuScreen = 2;

class Ui_QtMainScreen(DynamicWidget):
    startNewSession = pyqtSignal();
    reconnectLastSession = pyqtSignal();
    startNewGame = pyqtSignal();
    addAHorse = pyqtSignal();
    refreshHorses = pyqtSignal();
    removeAHorse = pyqtSignal();
    clearADrink = pyqtSignal(int);

    def __init__(self):
        super().__init__("Main")

        self.AnimationEngine = QtAnimationEngine.QtAnimationEngine();

        self.__InitializeBackground()

        self.StartTimer(10);

    def _Update(self):
        # Update animation and check if done
        self.AnimationEngine.update();

    def SetMode(self, mode):
        self.mode = mode
        if(mode == widgetMode.WelcomeScreen):
            self._SetAsWelcome()
        if(mode == widgetMode.MenuScreen):
            self._InitializeMenu()

#region VisualAssets

    def CreateSimpleText(self, text, fontsize):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(fontsize)
        label = QtLinkText.QtSimpleText(self.Scene, text, font) 
        label.setPos(-100,-100)
        return label

    def CreateLinkText(self, text, fontsize, fire):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(fontsize)
        label = QtLinkText.QtLinkText(self.Scene, text, fire, font)
        label.setPos(-100,-100) 
        return label

    def CreateRemoveableText(self, text, fontsize, fire):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(fontsize)
        label = QtLinkText.QtRemoveableText(self.Scene, text, fire, font)
        label.setPos(-100,-100) 
        return label

    def __InitializeBackground(self):
        #Set background
        self.backGround = QtStaticImg.QtStaticImage()
        self.backGround.setAsset("Assets/MenuBackgrounds/IdylicBackground.png",self.Scene.width(),self.Scene.height())
        self.backGround.setZValue(-10);
        self.Scene.addItem(self.backGround);

        # Create clouds and loop them
        for i in range(0, 6):
            cloud = QtSprites.QtBaseSprite();
            cloud.setSpriteAsset("Assets/Background/clouds.png", 304, 123);
            size = random.randint(0,2);
            cloud.changeSpriteState(size)
            cloud._UpdateSprite()
            self.Scene.addItem(cloud);
            speed = 10000 + 2000*size + random.randint(0,4)*1000;
            height = random.uniform(-0.1,0.09)*self.Scene.height()
            width = random.uniform(-0.5,0.9);
            # set initial pos
            cloud.setPos(width*self.Scene.width(), height)
            # Initial animation
            initAnim = QtTrajectory.LinearMovement(cloud, (1-width)*self.Scene.width() + 10, 0, int(speed*(1-width)));
            self.AnimationEngine.addAnimationSequence(initAnim)
            # looping animiation
            loopAnim = QtTrajectory.LoopingLinearPath(cloud,-0.5*self.Scene.width(),height,self.Scene.width() + 10,height,speed);
            self.AnimationEngine.addAnimationSequence([initAnim, loopAnim])
#endregion

    def DisplayUrl(self, url):
        if "localhost" in url:
            import socket
            ipv4 = socket.gethostbyname(socket.gethostname())
            hostname = ipv4 + ":" + url[-4:]
        else:
            hostname = url
        self.connectToLabel = self.CreateSimpleText("Connect to:", 26)
        self.connectToLabel.setPos(self.Scene.width() - 200,50);
        self.addressLabel = self.CreateSimpleText(hostname, 22)
        self.addressLabel.setPos(self.Scene.width() - 200,90);


#region WelcomeScreen
    def _SetAsWelcome(self):
        # Loop welcome assets in
        self.restartLink = self.CreateLinkText("Reconnect to last game", 26, self.ReconnectLastSession)
        self.restartLink.setPos(self.Scene.width()/2,self.Scene.height() + 25);
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.restartLink,0,-self.Scene.height()/2.75,250))
        self.welcomeLink = self.CreateLinkText("Start a Game", 32, self.EstablishNewSession)
        self.welcomeLink.setPos(self.Scene.width()/2,-10);
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.welcomeLink,0,self.Scene.height()/2.75,250))
        self.welcomeHeadline = self.CreateSimpleText("Welcome", 48)
        self.welcomeHeadline.setPos(self.Scene.width()/2,-75);
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.welcomeHeadline,0,self.Scene.height()/2.75,250))


    def _ClearWelcomeAssets(self):
        if self.welcomeLink and self.welcomeLink.pos().x() > 0:
            self.AnimationEngine.addAnimation(QtTrajectory.LinearMovement(self.welcomeLink,-self.Scene.width(),0,125));
        if self.welcomeHeadline and self.welcomeHeadline.pos().x() > 0:
            self.AnimationEngine.addAnimation(QtTrajectory.LinearMovement(self.welcomeHeadline,-self.Scene.width(),0,125));
#endregion

#region TransitionToMenu
    def EstablishNewSession(self):
        self.ConnectTransition()
        # notify that it needs to start new session
        self.startNewSession.emit();

    def ReconnectLastSession(self):
        self.ConnectTransition()
        # notify that it needs to start new session
        self.reconnectLastSession.emit();

    def ConnectTransition(self):
        self._ClearWelcomeAssets()
        self.LoadingHeadline = self.CreateSimpleText("Loading", 48)
        self.LoadingStatus = self.CreateSimpleText("Establishing connection to the server", 26)
        # Loop welcome assets in
        self.LoadingHeadline.setPos(self.Scene.width()*1.5,self.Scene.height()/2.75-75);
        self.LoadingStatus.setPos(self.Scene.width()*1.5,self.Scene.height()/2.75-10);
        self.AnimationEngine.addAnimation(QtTrajectory.LinearMovement(self.LoadingStatus,-self.Scene.width(),0,125));
        self.AnimationEngine.addAnimation(QtTrajectory.LinearMovement(self.LoadingHeadline,-self.Scene.width(),0,125));

    def _ClearTransitionAssets(self):
        if self.LoadingHeadline and self.LoadingHeadline.pos().x() > 0:
            self.AnimationEngine.addAnimation(QtTrajectory.LinearMovement(self.LoadingHeadline,-self.Scene.width(),0,125));
        if self.LoadingStatus and self.LoadingStatus.pos().x() > 0:
            self.AnimationEngine.addAnimation(QtTrajectory.LinearMovement(self.LoadingStatus,-self.Scene.width(),0,125));
#endregion

#region MenuScreen
    def _InitializeMenu(self):
        try:
            self._ClearTransitionAssets()
        except:
            pass

        # prep horse and players dict
        self.horses = {}
        self.players = {}
        self.drinks = {}

        self.outerColumns = self.Scene.width()/4

        ### Left Column
        # Horses label
        self.HorsesLabel = self.CreateSimpleText("Horses", 24)
        self.HorsesLabel.setPos(-50,self.Scene.height()/5); 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.HorsesLabel,self.outerColumns,0,125))
        # AddHorse
        self.AddHorsesLink = self.CreateLinkText("Add a horse", 16, self.addAHorse.emit)
        self.AddHorsesLink.setPos(-50,4*self.Scene.height()/5); 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.AddHorsesLink,self.outerColumns,0,125))
        # RefreshHorses
        self.RefreshHorsesLink = self.CreateLinkText("New Horses", 16, self.refreshHorses.emit)
        self.RefreshHorsesLink.setPos(-50,4*self.Scene.height()/5+50); 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.RefreshHorsesLink,self.outerColumns,0,125))
        # RemoveHorse
        self.RemoveHorsesLink = self.CreateLinkText("Remove a horse", 16, self.removeAHorse.emit)
        self.RemoveHorsesLink.setPos(-50,4*self.Scene.height()/5+100); 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.RemoveHorsesLink,self.outerColumns,0,125))

        ### Center
        # Gamename label
        self.gameNameLabel = self.CreateSimpleText("Session name:", 26)
        self.gameNameLabel.setPos(self.Scene.width()/2,-75); 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.gameNameLabel,0,self.Scene.height()/4,125))
        # Gamename
        if hasattr(self,"CurrentGameName"):
            self.gameName = self.CreateSimpleText(self.CurrentGameName, 26)
        else:
            self.gameName = self.CreateSimpleText("<Err:UNKNOWN>", 26)
        self.gameName.setPos(self.Scene.width()/2,-10); 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.gameName,0,self.Scene.height()/4,125))
        # Bets
        self.gameNameLabel = self.CreateSimpleText("Paid drinks", 24)
        self.gameNameLabel.setPos(self.Scene.width()/2,self.Scene.height() + 75); 
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.gameNameLabel,0, -3*self.Scene.height()/5-75,125))

        ## Right Column
        # Racelink
        self.RaceLink = self.CreateLinkText("Race!", 32, self.startNewGame.emit)
        self.RaceLink.setPos(self.Scene.width() + 30,4*self.Scene.height()/5 + 50);
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.RaceLink,-self.outerColumns,0,125))
        # Players
        self.PlayersLabel = self.CreateSimpleText("Players", 24)
        self.PlayersLabel.setPos(self.Scene.width()+50,self.Scene.height()/5); # Players
        self.AnimationEngine.addAnimation(QtTrajectory.SlowingLinearPath(self.PlayersLabel,-self.outerColumns,0,125))




    def _GetPlayerAlias(self, id):
        for k, v in self.players.items():
            if (v.id == id):
                return k
        return "<Unknown>"

    def _DisplayHorses(self, horses):
        for horse in horses:
            if not horse in self.horses.keys():
                horseLabel = self.CreateSimpleText(horse, 18)
                horseLabel.setPos(self.outerColumns, self.Scene.height()/5+45*(len(self.horses)+1))
                self.horses[horse] = horseLabel

    def SetHorses(self, horses, header):
        nameIdx = header.index("Name")
        self._DisplayHorses([horse[nameIdx] for horse in horses])


    def _DisplayPlayers(self, players):
        # TODO: Click to kick
        for player, standing, id in players:
            if not player in self.players.keys():
                # Create Label
                playerLabel = self.CreateSimpleText("{0} ({1})".format(player,standing), 18)
                playerLabel.id = id
                playerLabel.setPos(self.Scene.width() - self.outerColumns, self.Scene.height()/5+45*(len(self.players)+1))
                self.players[player] = playerLabel

    def SetPlayers(self, players, header):
        nameIdx = header.index("Alias")
        standingIdx = header.index("Standing")
        idIdx = header.index("id")
        self._DisplayPlayers([(player[nameIdx], player[standingIdx], player[idIdx]) for player in players])

    def _DisplayDrinks(self, drinks):
        occupiedPositions = [drink.Data for id, drink in self.drinks.items() if not drink.IsCleared]

        for fromUserId, toUserId, drink, id in drinks:
            if not id in self.drinks.keys():
                fromUser = self._GetPlayerAlias(fromUserId)
                toUser = self._GetPlayerAlias(toUserId)
                DrinkLabel = self.CreateRemoveableText("{2} gifted to {1} by {0}".format(fromUser, toUser, self.GetDrinkLabel(drink)), 18, lambda id=id: self.clearADrink.emit(id))
                # Find insertion point
                p = 0
                while p in occupiedPositions:
                    p += 1
                DrinkLabel.setPos(self.Scene.width()/2, 2*self.Scene.height()/5+45*(p+1))
                DrinkLabel.Data = p
                occupiedPositions.append(p)
                self.drinks[id] = DrinkLabel
    
    def GetDrinkLabel(self, drink):
        if drink == 1:
            return "sip"
        if drink == 3:
            return "shot"
        return "beer"

    def SetDrinks(self, drinks, header):
        fromUserIdx = header.index("FromUserId");
        toUserIdx = header.index("ToUserId");
        drinkIdx = header.index("Drink")
        idIdx = header.index("id")
        self._DisplayDrinks([(drink[fromUserIdx], drink[toUserIdx], drink[drinkIdx], drink[idIdx]) for drink in drinks])

    def SetGameName(self, name):
        self.CurrentGameName = name
        if hasattr(self,'gameName'):
            self.gameName.setPlainText(self.CurrentGameName)
#endregion