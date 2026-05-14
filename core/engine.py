import os
from PyQt6.QtCore import QObject, QUrl, pyqtSignal, pyqtProperty, pyqtSlot
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

class MediaEngine(QObject):
    stateChanged = pyqtSignal(QMediaPlayer.PlaybackState)
    positionChanged = pyqtSignal(int)
    durationChanged = pyqtSignal(int)
    volumeChanged = pyqtSignal(int)
    errorOccurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        
        # Connect signals
        self.player.playbackStateChanged.connect(self.stateChanged.emit)
        self.player.positionChanged.connect(self.positionChanged.emit)
        self.player.durationChanged.connect(self.durationChanged.emit)
        self.player.errorOccurred.connect(self._handle_error)

        # Default volume
        self.audio_output.setVolume(0.7)

    def _handle_error(self, error, error_string):
        self.errorOccurred.emit(error_string)

    def set_video_widget(self, widget: QVideoWidget):
        self.player.setVideoOutput(widget)

    def load_media(self, file_path: str):
        if not os.path.exists(file_path):
            self.errorOccurred.emit(f"File not found: {file_path}")
            return False
        
        url = QUrl.fromLocalFile(file_path)
        self.player.setSource(url)
        return True

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_position(self, ms: int):
        self.player.setPosition(ms)

    def set_volume(self, volume: int):
        # QAudioOutput expects a float from 0.0 to 1.0 linearly, but often UI is 0-100
        # Convert logarithmic if needed, but linear 0-1 is fine for now
        val = max(0, min(100, volume)) / 100.0
        self.audio_output.setVolume(val)

    def get_volume(self) -> int:
        return int(self.audio_output.volume() * 100)

    def set_playback_rate(self, rate: float):
        self.player.setPlaybackRate(rate)

    @property
    def is_playing(self) -> bool:
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    def toggle_play_pause(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()
