import GameSettings as cfg, sys, GameMaster
from PyQt5.QtWidgets import QApplication


cfg.GameSettings(
            Url = "Local",
            Debug = (1 if __name__ == '__main__' else 0),
            PlayMusic = True,
            PlayEffects = True,
            Height = 720,
            Width = 1080,
            )


# Init Qt
app = QApplication(sys.argv)

# Start the game
Game = GameMaster.GameMaster(app)

# Cleanup
sys.exit(app.exec_())