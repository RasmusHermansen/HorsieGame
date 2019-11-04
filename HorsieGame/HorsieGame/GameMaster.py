from Databinding.Connection import ServerConnection
from Databinding.Querier import Querier
import sys, os, threading
from AudioPlayer import AudioPlayer
from GameSettings import GameSettings as Settings
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from Screens import MenuScreen, GameScreen, LoadingScreen

class GameMaster(QMainWindow):

    _updateFuncs = []
    _inPerformUpdateFuncs = False

    def __init__(self, QtApp):
        # Store parent app
        self.app = QtApp
        # Ensure settings are initialized
        if(not Settings.Instantiated()):
            raise EnvironmentError("GameSettings Object not initialized")
        # Init Qt
        super().__init__()
        # Init Assets & MediaPlayer
        self._LoadAssets()
        # Init background worker
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.PerformUpdateFuncs)
        self.timer.start(2500)
        # Initialize main window
        self.__InitMainWindow()
        # Prepare Loading widget
        self.SetToWelcome()
        # Show
        self.show()
    
    def PerformUpdateFuncs(self):
        if self._updateFuncs:
            if not self._inPerformUpdateFuncs:
                self._inPerformUpdateFuncs = True
                self.backgroundWorker = RunThread(self.IterateUpdateFuncs,self.IterateUpdateFuncsCB)

    def IterateUpdateFuncs(self):
        for func in self._updateFuncs:
            func()

    def IterateUpdateFuncsCB(self):
        self._inPerformUpdateFuncs = False

#region WELCOMESCREEN And MENUSCREEN
    def SetToWelcome(self):
        self.MenuWidget = MenuScreen.Ui_QtMainScreen();
        self.MenuWidget.SetMode(MenuScreen.widgetMode.WelcomeScreen)
        self.MenuWidget.startNewSession.connect(self.InitConnection);
        # Set as central widget
        self.setCentralWidget(self.MenuWidget.getWidget())       

    # Handle for btn pressed on WelcomeScreen
    def InitConnection(self):
        self.SetToLoading()
        self.LoadingWidget.ChangeStatus("Connecting to server")
        self.worker = RunThread(self._InitConnection,self._InitConnectionCB)

    # The callback for _InitConnection
    def _InitConnectionCB(self, _InitConnectionResults):
        # Check if valid connection
        try:
            self.conn = _InitConnectionResults[0]
            self.GameName = _InitConnectionResults[1]  
            self.LoadingWidget.ChangeStatus("Setting up session")
            # Add two horses
            if(not hasattr(self,"Horses")):
                self.AddOrRemoveHorses(4)
        except Exception as e: 
            print(e)
            self.SetToWelcome()
            if (_InitConnectionResults):
                print(_InitConnectionResults)
            else:
                print("Failed to connect to server")
        # SetToMenu
        self.SetToMenu()

    # Makes the request to Server and establishes a conn
    def _InitConnection(self):
        conn = Querier(ServerConnection(Settings().Url))
        return conn, conn.InstantiateNewSession()

    def AddOrRemoveHorses(self, count):
        if(not hasattr(self,"Horses")):
            self.Horses = []

        if (len(self.Horses) == count):
            return
        else:
            self.app.processEvents()
            self.worker = RunThread(lambda: self.conn.SetHorseCount(count)['Horses'], self._AddOrRemoveHorsesCB)

    def _AddOrRemoveHorsesCB(self, horses):
        self.Horses = horses
        self.PopulateHorseTable()

    def AddOneHorse(self):
        self.AddOrRemoveHorses(len(self.Horses)+1)

    def RemoveOneHorse(self):
        self.AddOrRemoveHorses(min(len(self.Horses)-1,1))
    
    def PopulateHorseTable(self):
        if self.Horses:
            header = list(self.Horses[0].keys())
            data = [list(x.values()) for x in self.Horses]
            self.MenuWidget.SetHorses(data, header)

    def GetPlayers(self):
        if(not hasattr(self,"Players")):
            self.Players = []

        self.Players = self.conn.GetPlayers()['Players']
        if self.Players: # <-- True if not empty
            header = list(self.Players[0].keys())
            data = [list(x.values()) for x in self.Players]
            self.MenuWidget.SetPlayers(data, header)

    def GetDrinks(self):
        if(not hasattr(self,"Drinks")):
            self.Drinks = []

        self.Drinks = self.conn.GetDrinks()['Drinks']
        if self.Drinks: # <-- True if not empty
            header = list(self.Drinks[0].keys())
            data = [list(x.values()) for x in self.Drinks]
            self.MenuWidget.SetDrinks(data, header, self.ClearDrink)
        else:
            self.MenuWidget.ClearDrinks()

    def ClearDrink(self, drinkId):
        print("Clearing drink:{0}".format(drinkId))
        self.worker = RunThread(lambda: self.conn.DealDrink(drinkId))

    def SetToMenu(self):
        self.MenuWidget = MenuScreen.Ui_QtMainScreen();
        if hasattr(self,"GameName"):
            self.MenuWidget.SetGameName(self.GameName)
        self.MenuWidget.SetMode(MenuScreen.widgetMode.MenuScreen)
        # Connect to menu screen signals
        self.MenuWidget.addAHorse.connect(self.AddOneHorse)
        #self.MenuWidget.refreshHorses.connect(self.RefreshHorses)
        self.MenuWidget.removeAHorse.connect(self.RemoveOneHorse)
        self.MenuWidget.clearADrink.connect(self.ClearDrink)
        self.MenuWidget.startNewGame.connect(self.StartGame)
        # Start refreshing players & Populate horse table
        self._updateFuncs.append(self.app.processEvents)
        self._updateFuncs.append(self.GetPlayers)
        self._updateFuncs.append(self.GetDrinks)
        self.PopulateHorseTable()
        self.setCentralWidget(self.MenuWidget.getWidget())
#endregion 

#region GameScreen
    def StartGame(self):
        # Set loading widget
        #self.SetToLoading()
        #self.LoadingWidget.ChangeStatus("Feeding Horses (Doing Nothing)")
        self.app.processEvents()
        self.GameWidget = GameScreen.Ui_QtGameScreen(self.PostGame, self.Horses, self.DisableBetting)
        self.setCentralWidget(self.GameWidget.getWidget())
        self.app.processEvents()
        AudioPlayer().SetBackgroundTrack('LoneRanger');
        self.timer.stop()
        self.GameWidget.RunGame()
        
    def PostGame(self, results):
        self.timer.start(2500)
        self.ReportResults(results)
        self.SetToMenu()

    def ReportResults(self, results):
        self.conn.ReportResults([results[place].Id for place in sorted(results)])

    def DisableBetting(self):
        self.worker = RunThread(self.conn.DisableBetting)
#endregion

#region Loading screen
    def SetToLoading(self):
        AudioPlayer().PlayEffect("Vrinsk")
        self.LoadingWidget = LoadingScreen.Ui_QtLoadingScreen()
        self.setCentralWidget(self.LoadingWidget.getWidget())
#endregion

    def __InitMainWindow(self):
        # Set size
        if(Settings().Debug):
            self.resize(1000, 600)
            self.move(300, 300)
            self.setFixedSize(Settings().Width, Settings().Height)
            self.move(300,300);
        else:
            self.showFullScreen()
        # Set window title
        self.setWindowTitle('HorsieGame')
        # Set Icon
        self.setWindowIcon(QIcon("Assets/Logo/Logo_64.png"))

    def _LoadAssets(self):
        # Load Font
        fontId = QFontDatabase().addApplicationFont("Assets/Font/south park.ttf")
        family = QFontDatabase().applicationFontFamilies(fontId)[0]
        MainFont = QFont(family)
        self.app.setFont(MainFont)
        
        # Initialize media player
        self.Audio = AudioPlayer('WindBlowing');

    def closeEvent(self, event):
        if(hasattr(self,"conn") and (self.conn != None)):
            self.conn.CloseSession()
        event.accept()

class RunThread(QThread):
    """ Runs a function in a thread, and alerts the parent when done. 

    Uses a pyqtSignal to alert the main thread of completion.

    """
    finished = pyqtSignal([object])

    def __init__(self, func, on_finish = None, *args, **kwargs):
        super(RunThread, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.func = func
        if on_finish:
            self.finished.connect(on_finish)
        self.start()

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            print(e)
            result = e
        finally:
            if self.finished:
                self.finished.emit(result)