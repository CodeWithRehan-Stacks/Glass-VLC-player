import sys
import os
import json
import qtawesome as qta

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QFrame, QFileDialog, QGraphicsDropShadowEffect,
                             QLabel, QPushButton)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

# ── Path Setup ──────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

# ── Navigation & Views ──────────────────────────────────────────────────────
from navigation.sidebar.sidebar import Sidebar
from navigation.topbar.topbar import TopBar
from navigation.router import AnimatedRouter
from views.dashboard import DashboardView

# ── Screens ─────────────────────────────────────────────────────────────────
from screens.player import PlayerScreen
from mixer.panel import MixerPanel
from radio.stations import RadioPanel
from visualizer.analyzer import VisualizerWidget
from components.title_bar import CustomTitleBar

# ── Placeholder view for pages not yet built ────────────────────────────────
class PlaceholderView(QWidget):
    def __init__(self, icon, label, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(16)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon(icon, color="#2D3748").pixmap(QSize(64, 64)))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text = QLabel(f"{label}\nComing Soon")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setStyleSheet("color: #4A5568; font-size: 18px; font-weight: 600; line-height: 1.6;")

        layout.addWidget(icon_lbl)
        layout.addWidget(text)


class NexusStudio(QMainWindow):
    """
    Nexus Studio — Premium AI Multimedia Platform
    Architecture: MVVM-lite with central AnimatedRouter and modular views.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexus Studio")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)

        # ── Frameless window ─────────────────────────────────────────────────
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ── State ────────────────────────────────────────────────────────────
        self.history_file = os.path.join(BASE, "history.json")
        self.memory_file  = os.path.join(BASE, "memory.json")
        self.recent_files    = []
        self.playback_memory = {}

        # ── Apply theme ──────────────────────────────────────────────────────
        self._apply_theme()

        # ── Media Engine ─────────────────────────────────────────────────────
        self.player       = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.7)

        # ── Auto-save timer ──────────────────────────────────────────────────
        self.save_timer = QTimer(self)
        self.save_timer.setInterval(5000)
        self.save_timer.timeout.connect(self._update_memory)
        self.save_timer.start()

        # ── Build UI ─────────────────────────────────────────────────────────
        self._build_shell()
        self._build_views()
        self._wire_signals()

        # ── Load persisted data ──────────────────────────────────────────────
        self._load_all()

    # ─────────────────────────────────────────────────────────────────────────
    # UI Construction
    # ─────────────────────────────────────────────────────────────────────────

    def _build_shell(self):
        """Outer container with drop-shadow, title bar, sidebar, topbar."""

        # Root container (carries the shadow + rounded border)
        self.root = QFrame()
        self.root.setObjectName("MainContainer")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.root.setGraphicsEffect(shadow)

        self.setCentralWidget(self.root)

        root_layout = QVBoxLayout(self.root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Title bar
        self.title_bar = CustomTitleBar(self)
        root_layout.addWidget(self.title_bar)

        # Body: sidebar + content column
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Sidebar (collapsible)
        self.sidebar = Sidebar()
        body_layout.addWidget(self.sidebar)

        # Right column: topbar + visualizer + router
        right_col = QWidget()
        right_col_layout = QVBoxLayout(right_col)
        right_col_layout.setContentsMargins(0, 0, 0, 0)
        right_col_layout.setSpacing(0)

        self.topbar = TopBar()
        right_col_layout.addWidget(self.topbar)

        # Audio visualizer strip (thin, always-on)
        self.visualizer = VisualizerWidget()
        self.visualizer.setFixedHeight(60)
        right_col_layout.addWidget(self.visualizer)

        # Animated page router
        self.router = AnimatedRouter()
        right_col_layout.addWidget(self.router, stretch=1)

        body_layout.addWidget(right_col, stretch=1)
        root_layout.addWidget(body)

    def _build_views(self):
        """Instantiate all views/screens and register them in the router."""

        # 0 — Dashboard (Home)
        self.dashboard = DashboardView()
        self.router.addWidget(self.dashboard)

        # 1 — Cinema Player
        self.player_screen = PlayerScreen(self)
        self.player.setVideoOutput(self.player_screen.get_video_widget())
        self.router.addWidget(self.player_screen)

        # 2 — Audio Mixer
        self.mixer = MixerPanel()
        self.router.addWidget(self.mixer)

        # 3 — Radio
        self.radio = RadioPanel()
        self.router.addWidget(self.radio)

        # 4 — Library (placeholder)
        self.router.addWidget(PlaceholderView('mdi.playlist-music', 'Library'))

        # 5 — History (placeholder)
        self.router.addWidget(PlaceholderView('mdi.history', 'History'))

        # 6 — Settings (placeholder)
        self.router.addWidget(PlaceholderView('mdi.cog', 'Settings'))

        self.router.setCurrentIndex(0)

    def _wire_signals(self):
        """Connect all cross-component signals."""

        # Sidebar navigation
        self.sidebar.tab_changed.connect(self.router.switch_to)

        # Dashboard navigation shortcuts
        self.dashboard.navigate_to.connect(self._handle_dashboard_navigate)
        self.dashboard.file_play_requested.connect(self._play_file)

        # Topbar search
        self.topbar.search_triggered.connect(self._on_search)

        # Cinema Player controls
        ctrl = self.player_screen.controls
        ctrl.play_pause_clicked.connect(self._toggle_playback)
        ctrl.seek_slider_moved.connect(self._on_seek)
        ctrl.volume_slider_moved.connect(
            lambda v: self.audio_output.setVolume(v / 100.0))
        ctrl.skip_forward_clicked.connect(
            lambda: self.player.setPosition(self.player.position() + 10000))
        ctrl.skip_backward_clicked.connect(
            lambda: self.player.setPosition(max(0, self.player.position() - 10000)))

        self.player.playbackStateChanged.connect(self._on_playback_state_changed)
        self.player.positionChanged.connect(
            lambda p: ctrl.update_position(p, self.player.duration()))
        self.player.durationChanged.connect(
            lambda d: ctrl.update_position(self.player.position(), d))

        # Radio
        self.radio.station_selected.connect(self._play_radio)

    # ─────────────────────────────────────────────────────────────────────────
    # Navigation
    # ─────────────────────────────────────────────────────────────────────────

    def _handle_dashboard_navigate(self, idx):
        """Dashboard tiles emit tab indices; -1 means 'open file dialog'."""
        if idx == -1:
            self._browse_file()
        else:
            self.router.switch_to(idx)
            self.sidebar._on_item_clicked(idx)

    def _on_search(self, query):
        """Basic search: jump to relevant page by keyword."""
        q = query.strip().lower()
        mapping = {
            'cinema': 1, 'video': 1, 'player': 1,
            'mixer': 2, 'audio': 2, 'eq': 2,
            'radio': 3, 'stream': 3,
            'library': 4, 'playlist': 4,
            'history': 5,
            'settings': 6,
        }
        for keyword, idx in mapping.items():
            if keyword in q:
                self.router.switch_to(idx)
                self.sidebar._on_item_clicked(idx)
                return

    # ─────────────────────────────────────────────────────────────────────────
    # Playback
    # ─────────────────────────────────────────────────────────────────────────

    def _browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Media File", "",
            "Video / Audio (*.mp4 *.mkv *.avi *.mov *.mp3 *.wav *.flac *.ogg *.m4a)")
        if path:
            self._play_file(path)

    def _play_file(self, path):
        from PyQt6.QtCore import QUrl
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()
        # Navigate to player and sync sidebar
        self.router.switch_to(1)
        self.sidebar._on_item_clicked(1)
        self._add_to_history(path)
        # Smart resume
        if path in self.playback_memory:
            self.player.setPosition(self.playback_memory[path])

    def _play_radio(self, name, url):
        from PyQt6.QtCore import QUrl
        self.player.setSource(QUrl(url))
        self.player.play()
        self.router.switch_to(1)
        self.sidebar._on_item_clicked(1)
        self.title_bar.title.setText(f"NEXUS STUDIO  •  {name}")

    def _toggle_playback(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def _on_seek(self, value):
        dur = self.player.duration()
        if dur > 0:
            self.player.setPosition(int((value / 1000.0) * dur))

    def _on_playback_state_changed(self, state):
        playing = state == QMediaPlayer.PlaybackState.PlayingState
        self.visualizer.set_active(playing)

    # ─────────────────────────────────────────────────────────────────────────
    # Persistence
    # ─────────────────────────────────────────────────────────────────────────

    def _add_to_history(self, path):
        if path in self.recent_files:
            self.recent_files.remove(path)
        self.recent_files.insert(0, path)
        self.recent_files = self.recent_files[:15]
        self._refresh_dashboard()
        self._save_history()

    def _refresh_dashboard(self):
        self.dashboard.populate_recent(self.recent_files, self.playback_memory)

    def _update_memory(self):
        src = self.player.source().toLocalFile()
        if src and self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playback_memory[src] = self.player.position()
            self._save_memory()

    def _load_all(self):
        # Load memory
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file) as f:
                    self.playback_memory = json.load(f)
            except Exception:
                pass
        # Load history
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file) as f:
                    self.recent_files = json.load(f)
            except Exception:
                pass
        self._refresh_dashboard()

    def _save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.recent_files, f, indent=2)

    def _save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.playback_memory, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────────
    # Theme
    # ─────────────────────────────────────────────────────────────────────────

    def _apply_theme(self):
        qss = os.path.join(BASE, "themes", "cyber.qss")
        if os.path.exists(qss):
            with open(qss, encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    # ─────────────────────────────────────────────────────────────────────────
    # Keyboard Shortcuts
    # ─────────────────────────────────────────────────────────────────────────

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Space:
            self._toggle_playback()
        elif k == Qt.Key.Key_F:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif k == Qt.Key.Key_Left:
            self.player.setPosition(max(0, self.player.position() - 5000))
        elif k == Qt.Key.Key_Right:
            self.player.setPosition(self.player.position() + 5000)
        elif k == Qt.Key.Key_Escape and self.isFullScreen():
            self.showNormal()
        else:
            super().keyPressEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    # QApplication must exist BEFORE any qtawesome icons are created.
    _app = QApplication(sys.argv)
    _font = QFont("Segoe UI", 10)
    _app.setFont(_font)

    # Now safe to instantiate the main window (triggers all icon creation)
    window = NexusStudio()
    window.show()
    sys.exit(_app.exec())

