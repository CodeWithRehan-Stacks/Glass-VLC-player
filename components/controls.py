from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

class ControlsPanel(QWidget):
    play_pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    seek_slider_moved = pyqtSignal(int)
    volume_slider_moved = pyqtSignal(int)
    fullscreen_clicked = pyqtSignal()
    speed_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ControlsPanel")
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 10, 15, 10)

        # Buttons
        self.btn_play = QPushButton("▶")
        self.btn_stop = QPushButton("⏹")
        
        # Sliders
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, 1000)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(100)

        # Labels
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("TimeLabel")

        # Extras
        self.btn_speed = QPushButton("1.0x")
        self.btn_fullscreen = QPushButton("⛶")

        # Layout Assembly
        self.layout.addWidget(self.btn_play)
        self.layout.addWidget(self.btn_stop)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.time_label)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.seek_slider)
        self.layout.addSpacing(15)
        self.layout.addWidget(QLabel("Vol:"))
        self.layout.addWidget(self.volume_slider)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.btn_speed)
        self.layout.addWidget(self.btn_fullscreen)

        # Connections
        self.btn_play.clicked.connect(self.play_pause_clicked.emit)
        self.btn_stop.clicked.connect(self.stop_clicked.emit)
        self.seek_slider.sliderMoved.connect(self.seek_slider_moved.emit)
        self.volume_slider.valueChanged.connect(self.volume_slider_moved.emit)
        self.btn_fullscreen.clicked.connect(self.fullscreen_clicked.emit)
        self.btn_speed.clicked.connect(self.speed_clicked.emit)

    def set_playing_state(self, is_playing: bool):
        self.btn_play.setText("⏸" if is_playing else "▶")

    def update_time(self, current_ms, total_ms):
        self.time_label.setText(f"{self.format_time(current_ms)} / {self.format_time(total_ms)}")

    def update_position(self, current_ms, total_ms):
        if total_ms > 0:
            val = int((current_ms / total_ms) * 1000)
            self.seek_slider.blockSignals(True)
            self.seek_slider.setValue(val)
            self.seek_slider.blockSignals(False)
            self.update_time(current_ms, total_ms)

    @staticmethod
    def format_time(ms):
        s = ms // 1000
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"
