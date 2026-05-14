
import qtawesome as qta
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
                             QSlider, QLabel, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QTimer, QPoint, QSize

class HoverSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class FloatingControls(QWidget):
    play_pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    seek_slider_moved = pyqtSignal(int)
    volume_slider_moved = pyqtSignal(int)
    fullscreen_clicked = pyqtSignal()
    speed_clicked = pyqtSignal()
    skip_forward_clicked = pyqtSignal()
    skip_backward_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FloatingControls")
        self.setFixedHeight(100)
        
        # Icon Color
        self.icon_color = "#E2E8F0"
        self.icon_hover_color = "#00E5FF"
        self.icon_size = QSize(24, 24)
        
        # Opacity effect for fade in/out
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        
        # Animation
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(300)
        
        # Auto-hide timer
        self.hide_timer = QTimer(self)
        self.hide_timer.setInterval(3000) # 3 seconds
        self.hide_timer.timeout.connect(self.hide_controls)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 10)
        self.layout.setSpacing(5)

        # --- Top: Timeline / Seekbar ---
        self.timeline_layout = QHBoxLayout()
        self.time_current = QLabel("00:00")
        self.time_current.setObjectName("TimeLabel")
        self.time_total = QLabel("00:00")
        self.time_total.setObjectName("TimeLabel")
        
        self.seek_slider = HoverSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, 1000)
        self.seek_slider.setObjectName("CinematicSeekbar")

        self.timeline_layout.addWidget(self.time_current)
        self.timeline_layout.addWidget(self.seek_slider)
        self.timeline_layout.addWidget(self.time_total)
        
        # --- Bottom: YouTube-Style Buttons ---
        self.btn_layout = QHBoxLayout()
        
        # Left controls
        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(qta.icon('mdi.skip-previous', color=self.icon_color))
        
        self.btn_rewind = QPushButton()
        self.btn_rewind.setIcon(qta.icon('mdi.rewind-10', color=self.icon_color))
        
        self.btn_play = QPushButton()
        self.btn_play.setIcon(qta.icon('mdi.play', color=self.icon_color))
        
        self.btn_forward = QPushButton()
        self.btn_forward.setIcon(qta.icon('mdi.fast-forward-10', color=self.icon_color))
        
        self.btn_next = QPushButton()
        self.btn_next.setIcon(qta.icon('mdi.skip-next', color=self.icon_color))
        
        self.btn_vol_icon = QPushButton()
        self.btn_vol_icon.setIcon(qta.icon('mdi.volume-high', color=self.icon_color))
        
        self.volume_slider = HoverSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.setObjectName("VolumeSlider")

        left_btns = [self.btn_prev, self.btn_rewind, self.btn_play, self.btn_forward, self.btn_next, self.btn_vol_icon]
        for btn in left_btns:
            btn.setObjectName("ControlBtn")
            btn.setIconSize(self.icon_size)
            self.btn_layout.addWidget(btn)
        self.btn_layout.addWidget(self.volume_slider)
        self.btn_layout.addStretch()
        
        # Right controls
        self.btn_cc = QPushButton()
        self.btn_cc.setIcon(qta.icon('mdi.closed-caption', color=self.icon_color))
        
        self.btn_speed = QPushButton("1.0x") # Keep text for speed but styled
        self.btn_speed.setStyleSheet("font-weight: bold; font-size: 13px;")
        
        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(qta.icon('mdi.cog', color=self.icon_color))
        
        self.btn_pip = QPushButton()
        self.btn_pip.setIcon(qta.icon('mdi.picture-in-picture-bottom-right', color=self.icon_color))
        
        self.btn_theater = QPushButton()
        self.btn_theater.setIcon(qta.icon('mdi.rectangle-outline', color=self.icon_color))
        
        self.btn_fullscreen = QPushButton()
        self.btn_fullscreen.setIcon(qta.icon('mdi.fullscreen', color=self.icon_color))

        right_btns = [self.btn_cc, self.btn_speed, self.btn_settings, self.btn_pip, self.btn_theater, self.btn_fullscreen]
        for btn in right_btns:
            btn.setObjectName("ControlBtn")
            if not btn.text():
                btn.setIconSize(self.icon_size)
            self.btn_layout.addWidget(btn)

        self.layout.addLayout(self.timeline_layout)
        self.layout.addLayout(self.btn_layout)

        # Connections
        self.btn_play.clicked.connect(self.play_pause_clicked.emit)
        self.seek_slider.sliderMoved.connect(self.seek_slider_moved.emit)
        self.volume_slider.valueChanged.connect(self.volume_slider_moved.emit)
        self.btn_fullscreen.clicked.connect(self.fullscreen_clicked.emit)
        self.btn_speed.clicked.connect(self.speed_clicked.emit)
        self.btn_rewind.clicked.connect(self.skip_backward_clicked.emit)
        self.btn_forward.clicked.connect(self.skip_forward_clicked.emit)

    def show_controls(self):
        self.fade_anim.stop()
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()
        self.hide_timer.start()

    def hide_controls(self):
        self.fade_anim.stop()
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.start()

    def enterEvent(self, event):
        self.hide_timer.stop()
        self.show_controls()

    def leaveEvent(self, event):
        self.hide_timer.start()

    def set_playing_state(self, is_playing: bool):
        icon_name = 'mdi.pause' if is_playing else 'mdi.play'
        self.btn_play.setIcon(qta.icon(icon_name, color=self.icon_color))

    def update_position(self, current_ms, total_ms):
        if total_ms > 0:
            val = int((current_ms / total_ms) * 1000)
            self.seek_slider.blockSignals(True)
            self.seek_slider.setValue(val)
            self.seek_slider.blockSignals(False)
            
            self.time_current.setText(self.format_time(current_ms))
            self.time_total.setText(self.format_time(total_ms))

    @staticmethod
    def format_time(ms):
        s = ms // 1000
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"

