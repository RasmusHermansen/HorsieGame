from Databinding.Connection import ServerConnection
from Databinding.Querier import Querier
import GameSettings, sys, os, threading
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from Screens import WelcomeScreen, MenuScreen, GameScreen, LoadingScreen

class Game(QMainWindow):

    def __init__(self, settings, QtApp):
        assert isinstance(settings,GameSettings.GameSettings), "Invalid Settings object passed to Game"
        # Store parent app
        self.app = QtApp
        # Store settings
        self.Settings = settings
        # Init Qt
        super().__init__()
        # Initialize main window
        self.__InitMainWindow(settings)
        # Prepare Loading widget
        self.LoadingWidget = LoadingScreen.Ui_QtLoadingScreen()
        # Initialise Welcome widget
        self.WelcomeWidget = WelcomeScreen.Ui_QtWelcomeScreen(self.InitConnection)
        # Set as central widget
        self.setCentralWidget(self.WelcomeWidget.getWidget())
        # Show
        self.show()
        
        # When btn pressed on WelcomeScreen
    def InitConnection(self):
        # Set loading widget
        self.setCentralWidget(self.LoadingWidget.getWidget())
        self.worker = RunThread(self._InitConnection,self._InitConnectionCB)

    def SetToMenu(self):
        # Initialize menu widget and set to central widget
        self.MenuWidget = MenuScreen.Ui_QtMenuScreen(self.AddOrRemoveHorses)
        self.MenuWidget.SetGameName(self.GameName)
        self.setCentralWidget(self.MenuWidget.getWidget())

    def AddOrRemoveHorses(self, count):
        if(not hasattr(self,"Horses")):
            self.Horses = []

        if (len(self.Horses) == count):
            return
        else:
            self.app.processEvents()
            self.Horses = self.conn.SetHorseCount(count)['Horses']
            header = list(self.Horses[0].keys())
            data = [list(x.values()) for x in self.Horses]
            self.MenuWidget.SetHorses(data, header)

    def _InitConnectionCB(self, _InitConnectionResults):
        self.conn = _InitConnectionResults[0]
        self.GameName = _InitConnectionResults[1]
        self.SetToMenu()

    def _InitConnection(self):
        self.LoadingWidget.ChangeStatus("Establishing connection to server")
        conn = Querier(ServerConnection(self.Settings.URL))
        self.LoadingWidget.ChangeStatus("Instantiating new session")
        return conn, conn.InstantiateNewSession()

    def __InitMainWindow(self, settings):
        # Set size
        if(settings.DEBUG):
            self.resize(1000, 600)
            self.move(300, 300)
        else:
            self.showFullScreen()
        # Set window title
        self.setWindowTitle('HorsieGame')
        # Set Icon
        self.setWindowIcon(QIcon("Assets/Logo/Logo_64.png"))

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