import GameSettings as cfg, sys, GameMaster
from PyQt5.QtWidgets import QApplication


cfg.GameSettings(
            Url = "http://localhost:5555", # "Local",
            # Debug = (1 if __name__ == '__main__' else 0),
            PlayMusic = True,
            PlayEffects = True,
            Height = 1080,
            Width = 1920,
            )


# Init Qt
app = QApplication(sys.argv)

# Start the game
Game = GameMaster.GameMaster(app)

# Cleanup
sys.exit(app.exec_())