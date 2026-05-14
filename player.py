# player.py
import os
import sys
import vlc
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence, QShortcut

from playlist import PlaylistWidget
from controls import ControlsPanel
import utils
from styles import DARK_STYLE

class VideoPlayer(QMainWindow):
    """Main video player window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neon Player")
        self.resize(1100, 650)
        self.setStyleSheet(DARK_STYLE)
        
        # VLC instance
        self.instance = vlc.Instance("--no-xlib --quiet")
        self.player = self.instance.media_player_new()
        
        # UI
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_signals()
        
        # Timer to update UI (seek, time)
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start()
        
        # Drag & drop on window
        self.setAcceptDrops(True)
        
        # Recent playlist
        self.recent = utils.load_recent_playlist()
        for path in self.recent:
            if os.path.exists(path):
                self.playlist.add_item(path)
        
        # Flag for fullscreen
        self.is_fullscreen = False
        self.was_maximized = False
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Video widget (VLC embed)
        self.video_widget = QWidget()
        self.video_widget.setStyleSheet("background-color: black;")
        self.video_widget.setMinimumHeight(400)
        main_layout.addWidget(self.video_widget, 1)
        
        # Bottom area: controls + playlist
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(8, 8, 8, 8)
        bottom_layout.setSpacing(8)
        
        # Controls panel
        self.controls = ControlsPanel()
        bottom_layout.addWidget(self.controls, 3)
        
        # Playlist sidebar
        self.playlist = PlaylistWidget()
        self.playlist.setMaximumWidth(260)
        self.playlist.setMinimumWidth(180)
        bottom_layout.addWidget(self.playlist, 1)
        
        main_layout.addLayout(bottom_layout)
        
        # Embed video in widget
        self.player.set_hwnd(int(self.video_widget.winId()))
    
    def setup_shortcuts(self):
        # Space: play/pause
        shortcut = QShortcut(QKeySequence("Space"), self)
        shortcut.activated.connect(self.controls.toggle_play)
        # F: fullscreen
        shortcut = QShortcut(QKeySequence("F"), self)
        shortcut.activated.connect(self.toggle_fullscreen)
        # Left/Right arrows: seek -5/+5 seconds
        shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        shortcut.activated.connect(lambda: self.seek_relative(-5000))
        shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        shortcut.activated.connect(lambda: self.seek_relative(5000))
        # Up/Down: volume
        shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        shortcut.activated.connect(lambda: self.change_volume(5))
        shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        shortcut.activated.connect(lambda: self.change_volume(-5))
    
    def setup_signals(self):
        self.controls.play_toggled.connect(self.toggle_play)
        self.controls.stop_clicked.connect(self.stop_video)
        self.controls.volume_changed.connect(self.set_volume)
        self.controls.seek_requested.connect(self.seek_percentage)
        self.controls.fullscreen_toggled.connect(self.toggle_fullscreen)
        self.controls.forward_clicked.connect(lambda: self.seek_relative(10000))
        self.controls.rewind_clicked.connect(lambda: self.seek_relative(-10000))
        self.controls.speed_changed.connect(self.set_speed)
        self.controls.screenshot_clicked.connect(self.take_screenshot)
        self.controls.pip_toggled.connect(self.toggle_pip)
        self.playlist.itemDoubleClicked.connect(self.play_selected)
    
    # ---------- Player control methods ----------
    def toggle_play(self, play):
        if play:
            self.player.play()
        else:
            self.player.pause()
    
    def stop_video(self):
        self.player.stop()
        self.controls.set_playing(False)
        self.controls.set_current_time(0, 0)
        self.controls.set_duration(0)
    
    def set_volume(self, value):
        self.player.audio_set_volume(value)
    
    def change_volume(self, delta):
        vol = self.player.audio_get_volume()
        new_vol = max(0, min(100, vol + delta))
        self.player.audio_set_volume(new_vol)
        self.controls.volume_slider.setValue(new_vol)
    
    def seek_relative(self, ms):
        """Seek forward/backward by ms milliseconds."""
        curr = self.player.get_time()
        if curr != -1:
            new_time = curr + ms
            self.player.set_time(new_time)
    
    def seek_percentage(self, percent):
        """Seek to percentage (0-1000)."""
        duration = self.player.get_length()
        if duration > 0:
            self.player.set_time(int(percent / 1000 * duration))
    
    def set_speed(self, speed):
        self.player.set_rate(speed)
    
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.was_maximized = self.isMaximized()
            self.showFullScreen()
        else:
            if self.was_maximized:
                self.showMaximized()
            else:
                self.showNormal()
    
    def toggle_pip(self):
        """Picture-in-Picture: hide controls and keep video on top."""
        if not hasattr(self, 'pip_window'):
            # Create a small floating window
            from PyQt5.QtWidgets import QWidget
            self.pip_window = QWidget()
            self.pip_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.pip_window.setStyleSheet("background-color: black;")
            self.pip_window.setFixedSize(320, 180)
            # Move to bottom right corner
            screen = self.screen().geometry()
            self.pip_window.move(screen.width() - 340, screen.height() - 200)
            # Transfer video to pip window
            self.player.set_hwnd(int(self.pip_window.winId()))
            self.pip_window.show()
        else:
            # Restore video to main window
            self.player.set_hwnd(int(self.video_widget.winId()))
            self.pip_window.close()
            self.pip_window = None
    
    def take_screenshot(self):
        """Capture current frame and save to desktop."""
        import datetime
        desktop = os.path.expanduser("~/Desktop")
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(desktop, filename)
        # VLC doesn't have direct screenshot; use QPixmap from video widget
        pixmap = self.video_widget.grab()
        pixmap.save(path)
        # Show notification
        self.statusBar().showMessage(f"Screenshot saved: {path}", 3000)
    
    def play_selected(self, item):
        """Play the video selected in playlist."""
        filepath = item.data(Qt.UserRole)
        if filepath and os.path.exists(filepath):
            self.load_media(filepath)
    
    def load_media(self, filepath):
        """Load a file into VLC and start playing."""
        if not os.path.exists(filepath):
            QMessageBox.warning(self, "File not found", f"Could not find: {filepath}")
            return
        media = self.instance.media_new(filepath)
        # Add subtitle support (auto-load .srt with same name)
        srt_path = os.path.splitext(filepath)[0] + ".srt"
        if os.path.exists(srt_path):
            media.add_option(f"sub-file={srt_path}")
        self.player.set_media(media)
        self.player.play()
        self.controls.set_playing(True)
        # Add to recent playlist
        self.add_to_recent(filepath)
    
    def add_to_recent(self, filepath):
        """Add filepath to recent list and save."""
        if filepath not in self.recent:
            self.recent.insert(0, filepath)
        else:
            self.recent.remove(filepath)
            self.recent.insert(0, filepath)
        utils.save_recent_playlist(self.recent)
    
    def update_ui(self):
        """Update time labels, seek bar, and play state."""
        if self.player.get_state() == vlc.State.Ended:
            self.controls.set_playing(False)
        if self.player.get_length() > 0:
            duration = self.player.get_length()
            current = self.player.get_time()
            if current >= 0:
                self.controls.set_duration(duration)
                self.controls.set_current_time(current, duration)
        # Update play/pause icon if state changed externally
        state = self.player.get_state()
        if state == vlc.State.Playing:
            self.controls.set_playing(True)
        elif state in (vlc.State.Paused, vlc.State.Stopped, vlc.State.Ended):
            self.controls.set_playing(False)
    
    # ---------- Drag & drop ----------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                    self.playlist.add_item(path)
                    # Auto-play first dropped file
                    if self.player.get_state() == vlc.State.Stopped:
                        self.playlist.setCurrentRow(self.playlist.count() - 1)
                        self.play_selected(self.playlist.currentItem())
            event.accept()
        else:
            event.ignore()