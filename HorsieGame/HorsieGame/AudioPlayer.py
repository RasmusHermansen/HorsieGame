import Singleton, os
from GameSettings import GameSettings
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent, QSound
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget


class AudioPlayer(object, metaclass=Singleton.Singleton):
    PathToTracks = "AudioAssets/Tracks/";
    ValidTrackSuffixes = ['wav'];
    PathToEffects = "AudioAssets/Effects/";
    ValidEffectSuffixes = ['wav'];
    CurrentTrack = "";
    TrackLibrary = {};
    EffectsLibrary = {};

    def __init__(self, startSong = None):
        # Load resource
        self._PreloadResources();
        # Choose first song
        self.SetBackgroundTrack(startSong);

    def SetBackgroundTrack(self, song):
        if(self.CurrentTrack != "" and self.CurrentTrack != song):
            self.TrackLibrary[self.CurrentTrack].stop()
        if(GameSettings().PlayMusic and song in self.TrackLibrary.keys()):
            self.TrackLibrary[song].play();
            self.CurrentTrack = song;


    def PlayEffect(self, effect):
        if(GameSettings().PlayEffects and effect in self.EffectsLibrary.keys()):
            self.EffectsLibrary[effect].play();

    def _PreloadResources(self):
        for file in self._IterateAssetsInFolder(self.PathToTracks,self.ValidTrackSuffixes):
            self.TrackLibrary[os.path.splitext(file)[0]] = QSound(self.PathToTracks + file);
            self.TrackLibrary[os.path.splitext(file)[0]].setLoops(-1);

        for file in self._IterateAssetsInFolder(self.PathToEffects,self.ValidEffectSuffixes):
            self.EffectsLibrary[os.path.splitext(file)[0]] = QSound(self.PathToEffects + file);
       
    def _IterateAssetsInFolder(self, FolderPath,suffixes):
        for filename in os.listdir(FolderPath):
            if any([filename.endswith(suffix) for suffix in suffixes]):
                yield os.path.basename(filename)