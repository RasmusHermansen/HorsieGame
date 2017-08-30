import GameSettings as cfg, sys, TheGame
from PyQt5.QtWidgets import QApplication


settings = cfg.GameSettings(
            URL = "Local",
            DEBUG = (1 if __name__ == '__main__' else 0)
            )

# Init Qt
app = QApplication(sys.argv)

# Start the game
Game = TheGame.Game(settings, app)

# Cleanup
sys.exit(app.exec_())