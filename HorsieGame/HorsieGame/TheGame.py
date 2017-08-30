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
        self.worker = RunThread(self._InitConnection,self.SetToMenu)

    def SetToMenu(self):
        # Initialize menu widget and set to central widget
        self.MenuWidget = MenuScreen.Ui_QtMenuScreen()
        self.setCentralWidget(self.MenuWidget.getWidget())

    def _InitConnection(self):
        self.LoadingWidget.ChangeStatus("Establishing connection to server")
        self.conn = Querier(ServerConnection(self.Settings.URL))
        self.LoadingWidget.ChangeStatus("Instantiating new session")
        self.GameName = self.conn.InstantiateNewSession()

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
    finished = pyqtSignal(["QString"], [int])

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
                self.finished.emit(str(result)) # Force it to be a string by default.