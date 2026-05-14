# controls.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLabel, QComboBox
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
import utils

class ControlsPanel(QWidget):
    """Custom video controls with seek bar, volume, speed, and fullscreen."""
    
    play_toggled = pyqtSignal(bool)
    stop_clicked = pyqtSignal()
    volume_changed = pyqtSignal(int)
    seek_requested = pyqtSignal(int)
    fullscreen_toggled = pyqtSignal()
    forward_clicked = pyqtSignal()
    rewind_clicked = pyqtSignal()
    speed_changed = pyqtSignal(float)
    screenshot_clicked = pyqtSignal()
    pip_toggled = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ControlsPanel")
        self.setup_ui()
        self.playing = False
        self.dragging_seek = False
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)
        
        # Seek bar row
        seek_layout = QHBoxLayout()
        self.time_current = QLabel("00:00")
        self.time_current.setObjectName("TimeLabel")
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 1000)  # 0-1000 for percentage
        self.seek_slider.sliderPressed.connect(self.on_seek_pressed)
        self.seek_slider.sliderReleased.connect(self.on_seek_released)
        self.seek_slider.sliderMoved.connect(self.on_seek_moved)
        self.time_total = QLabel("00:00")
        self.time_total.setObjectName("TimeLabel")
        seek_layout.addWidget(self.time_current)
        seek_layout.addWidget(self.seek_slider)
        seek_layout.addWidget(self.time_total)
        layout.addLayout(seek_layout)
        
        # Bottom controls row
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        
        # Play/Pause
        self.play_btn = QPushButton("▶")
        self.play_btn.setObjectName("PlayButton")
        self.play_btn.setFixedSize(48, 48)
        self.play_btn.clicked.connect(self.toggle_play)
        controls_layout.addWidget(self.play_btn)
        
        # Stop
        self.stop_btn = QPushButton("⏹")
        self.stop_btn.setFixedSize(36, 36)
        self.stop_btn.clicked.connect(self.stop_clicked.emit)
        controls_layout.addWidget(self.stop_btn)
        
        # Rewind / Forward
        self.rewind_btn = QPushButton("⏪")
        self.rewind_btn.clicked.connect(self.rewind_clicked.emit)
        controls_layout.addWidget(self.rewind_btn)
        
        self.forward_btn = QPushButton("⏩")
        self.forward_btn.clicked.connect(self.forward_clicked.emit)
        controls_layout.addWidget(self.forward_btn)
        
        # Volume
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.valueChanged.connect(self.volume_changed.emit)
        controls_layout.addWidget(QLabel("🔊"))
        controls_layout.addWidget(self.volume_slider)
        
        # Speed control
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.25x", "0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "2.0x"])
        self.speed_combo.setCurrentText("1.0x")
        self.speed_combo.currentTextChanged.connect(self.on_speed_changed)
        controls_layout.addWidget(self.speed_combo)
        
        # Fullscreen
        self.fullscreen_btn = QPushButton("⛶")
        self.fullscreen_btn.clicked.connect(self.fullscreen_toggled.emit)
        controls_layout.addWidget(self.fullscreen_btn)
        
        # Screenshot
        self.screenshot_btn = QPushButton("📷")
        self.screenshot_btn.clicked.connect(self.screenshot_clicked.emit)
        controls_layout.addWidget(self.screenshot_btn)
        
        # Picture-in-Picture
        self.pip_btn = QPushButton("▣")
        self.pip_btn.clicked.connect(self.pip_toggled.emit)
        controls_layout.addWidget(self.pip_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
    
    def toggle_play(self):
        self.playing = not self.playing
        self.play_btn.setText("⏸" if self.playing else "▶")
        self.play_toggled.emit(self.playing)
    
    def set_playing(self, playing):
        self.playing = playing
        self.play_btn.setText("⏸" if playing else "▶")
    
    def on_seek_pressed(self):
        self.dragging_seek = True
    
    def on_seek_released(self):
        self.dragging_seek = False
        val = self.seek_slider.value()
        self.seek_requested.emit(val)
    
    def on_seek_moved(self, value):
        # Update time label while dragging
        if self.dragging_seek:
            pass  # actual seeking happens on release
        # We'll update the time from the player
    
    def set_duration(self, ms):
        self.time_total.setText(utils.format_time(ms))
    
    def set_current_time(self, ms, duration):
        self.time_current.setText(utils.format_time(ms))
        if duration > 0:
            self.seek_slider.setValue(int(ms / duration * 1000))
    
    def on_speed_changed(self, text):
        speed = float(text.replace("x", ""))
        self.speed_changed.emit(speed)