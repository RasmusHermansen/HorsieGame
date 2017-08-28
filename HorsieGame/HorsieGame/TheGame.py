from Databinding.Connection import ServerConnection
from Databinding.Querier import Querier
import GameSettings
import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel

class Game(QMainWindow):

    def __init__(self, settings):
        assert isinstance(settings,GameSettings.GameSettings), "Invalid Settings object passed to Game"
       
        # Init Qt
        super().__init__()

        # Temp PyQt
        if(settings.DEBUG):
            self.resize(500, 300)
            self.move(300, 300)
        else:
            self.showFullScreen()
        self.setWindowTitle('HorsieGame')

        # Show
        self.show()
        # Temp over 

        # Initialize connection
        self.conn = Querier(ServerConnection(settings.URL))

        # Instantiate a new game connection
        self.gameName = self.conn.InstantiateNewSession()

        # Display GameName
        L_GameName = QLabel(self)
        L_GameName.setText(self.gameName)

    def closeEvent(self, event):
        self.conn.CloseSession()
        event.accept()
