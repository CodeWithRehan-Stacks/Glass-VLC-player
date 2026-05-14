import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget

from core.engine import MediaEngine
from components.controls import ControlsPanel
from screens.home import HomeScreen

class AIVideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Video Player - Premium")
        self.resize(1280, 720)
        
        # Core Engine
        self.engine = MediaEngine(self)
        
        # UI Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Stacked Widget for Screens
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # 1. Home Screen
        self.home_screen = HomeScreen()
        self.stack.addWidget(self.home_screen)

        # 2. Player Screen
        self.player_container = QWidget()
        self.player_layout = QVBoxLayout(self.player_container)
        self.player_layout.setContentsMargins(0, 0, 0, 0)
        self.player_layout.setSpacing(0)

        self.video_widget = QVideoWidget()
        self.player_layout.addWidget(self.video_widget, stretch=1)
        self.engine.set_video_widget(self.video_widget)

        self.controls = ControlsPanel()
        self.player_layout.addWidget(self.controls)
        
        self.stack.addWidget(self.player_container)

        # State
        self.history_file = os.path.join(os.path.dirname(__file__), "history.json")
        self.recent_files = []
        self.current_speed_idx = 1
        self.speeds = [0.5, 1.0, 1.5, 2.0]

        self._setup_connections()
        self._load_history()
        self._apply_theme()

    def _setup_connections(self):
        # Home Screen
        self.home_screen.open_file_clicked.connect(self._browse_file)
        self.home_screen.file_selected.connect(self._play_file)

        # Controls
        self.controls.play_pause_clicked.connect(self.engine.toggle_play_pause)
        self.controls.stop_clicked.connect(self._stop_and_return)
        self.controls.seek_slider_moved.connect(self._on_seek_slider_moved)
        self.controls.volume_slider_moved.connect(self.engine.set_volume)
        self.controls.fullscreen_clicked.connect(self._toggle_fullscreen)
        self.controls.speed_clicked.connect(self._cycle_speed)

        # Engine Signals
        self.engine.stateChanged.connect(self._on_state_changed)
        self.engine.positionChanged.connect(self._on_position_changed)
        self.engine.durationChanged.connect(self._on_duration_changed)

    def _apply_theme(self):
        theme_path = os.path.join(os.path.dirname(__file__), "styles", "theme.qss")
        if os.path.exists(theme_path):
            with open(theme_path, "r") as f:
                self.setStyleSheet(f.read())

    def _browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mkv *.mov)")
        if file_name:
            self._play_file(file_name)

    def _play_file(self, file_path):
        if self.engine.load_media(file_path):
            self.engine.play()
            self.stack.setCurrentWidget(self.player_container)
            self._add_to_history(file_path)

    def _stop_and_return(self):
        self.engine.stop()
        self.stack.setCurrentWidget(self.home_screen)

    def _on_state_changed(self, state):
        is_playing = state == QMediaPlayer.PlaybackState.PlayingState
        self.controls.set_playing_state(is_playing)

    def _on_position_changed(self, position):
        duration = self.engine.player.duration()
        self.controls.update_position(position, duration)

    def _on_duration_changed(self, duration):
        self.controls.update_position(self.engine.player.position(), duration)

    def _on_seek_slider_moved(self, value):
        duration = self.engine.player.duration()
        if duration > 0:
            ms = int((value / 1000.0) * duration)
            self.engine.set_position(ms)

    def _toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _cycle_speed(self):
        self.current_speed_idx = (self.current_speed_idx + 1) % len(self.speeds)
        speed = self.speeds[self.current_speed_idx]
        self.engine.set_playback_rate(speed)
        self.controls.btn_speed.setText(f"{speed}x")

    def _add_to_history(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:10]
        self.home_screen.populate_recent(self.recent_files)
        self._save_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    self.recent_files = json.load(f)
                    self.home_screen.populate_recent(self.recent_files)
            except Exception:
                pass

    def _save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.recent_files, f)

    def keyPressEvent(self, event):
        if self.stack.currentWidget() == self.player_container:
            if event.key() == Qt.Key.Key_Space:
                self.engine.toggle_play_pause()
            elif event.key() == Qt.Key.Key_F:
                self._toggle_fullscreen()
            elif event.key() == Qt.Key.Key_Left:
                self.engine.set_position(max(0, self.engine.player.position() - 5000))
            elif event.key() == Qt.Key.Key_Right:
                self.engine.set_position(min(self.engine.player.duration(), self.engine.player.position() + 5000))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set application-wide font
    font = app.font()
    font.setFamily("Segoe UI")
    app.setFont(font)
    
    player = AIVideoPlayer()
    player.show()
    sys.exit(app.exec())