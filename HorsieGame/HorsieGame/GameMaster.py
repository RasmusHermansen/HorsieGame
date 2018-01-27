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
        self.timer.start(1000)
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

#region WELCOMESCREEN And LOADINGSCREEN

    def SetToWelcome(self):
        self.WelcomeWidget = MenuScreen.Ui_QtMainScreen(MenuScreen.widgetMode.WelcomeScreen);
        # Set as central widget
        self.setCentralWidget(self.WelcomeWidget.getWidget())

    def SetToLoading(self):
        AudioPlayer().PlayEffect('Vrinsk');
        self.LoadingWidget = LoadingScreen.Ui_QtLoadingScreen()
        self.setCentralWidget(self.LoadingWidget.getWidget())

    # Handle for btn pressed on WelcomeScreen
    def InitConnection(self):
        # Set loading widget
        self.SetToLoading()
        self.worker = RunThread(self._InitConnection,self._InitConnectionCB)

    # The callback for _InitConnection
    def _InitConnectionCB(self, _InitConnectionResults):
        self.conn = _InitConnectionResults[0]
        self.GameName = _InitConnectionResults[1]
        self.SetToMenu()

    # Makes the request to Server and establishes a conn
    def _InitConnection(self):
        self.LoadingWidget.ChangeStatus("Establishing connection to server")
        conn = Querier(ServerConnection(Settings().Url))
        self.LoadingWidget.ChangeStatus("Instantiating new session")
        return conn, conn.InstantiateNewSession()
    
#endregion

#region MENUSCREEN

    # Initialize menu widget and set to central widget
    def SetToMenu(self):
        self.MenuWidget = MenuScreen.Ui_QtMenuScreen(self.AddOrRemoveHorses, self.StartGame)
        if(not hasattr(self,"Horses")):
            self.AddOrRemoveHorses(2)
        else:
            self.PopulateHorseTable()
        self.MenuWidget.SetGameName(self.GameName)
        self.setCentralWidget(self.MenuWidget.getWidget())
        self._updateFuncs.append(self.GetPlayers)

    def AddOrRemoveHorses(self, count):
        if(not hasattr(self,"Horses")):
            self.Horses = []

        if (len(self.Horses) == count):
            return
        else:
            self.app.processEvents()
            self.Horses = self.conn.SetHorseCount(count)['Horses']
            self.PopulateHorseTable()
    
    def PopulateHorseTable(self):
        if self.Horses: # <-- True if not empty
            header = list(self.Horses[0].keys())
            data = [list(x.values()) for x in self.Horses]
            self.MenuWidget.SetHorses(data, header)

    def GetPlayers(self):
        if(not hasattr(self,"Players")):
            self.Players = []

        self.app.processEvents()
        self.Players = self.conn.GetPlayers()['Players']
        if self.Players: # <-- True if not empty
            header = list(self.Players[0].keys())
            data = [list(x.values()) for x in self.Players]
            self.MenuWidget.SetPlayers(data, header)

#endregion 

#region GameScreen

    def StartGame(self):
        # Set loading widget
        self.SetToLoading()
        self.LoadingWidget.ChangeStatus("Feeding Horses")
        self.GameWidget = GameScreen.Ui_QtGameScreen(self.PostGame, self.Horses)
        self.setCentralWidget(self.GameWidget.getWidget())
        self.app.processEvents()
        self.showMaximized()
        AudioPlayer().SetBackgroundTrack('LoneRanger');
        self.GameWidget.RunGame()
        
    def PostGame(self, results):
        self.SetToMenu()

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
    finished = pyqtSignal([object], [int])

    def __init__(self, func, on_finish, *args, **kwargs):
        super(RunThread, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.func = func
        self.finished.connect(on_finish)
        self.finished[int].connect(on_finish)
        self.start()

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            print(e)
            result = e
        finally:
            if isinstance(result, int):
                self.finished[int].emit(result)
            else:
                self.finished.emit(result)