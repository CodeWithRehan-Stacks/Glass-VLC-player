
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor
from PyQt6.QtMultimediaWidgets import QVideoWidget
from components.overlay_controls import FloatingControls

class PlayerScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PlayerScreen")
        self.setMouseTracking(True)
        
        # Outer Glow Frame
        self.glow_frame = QFrame(self)
        self.glow_frame.setObjectName("GlowFrame")
        self.glow_frame.setStyleSheet("#GlowFrame { border-radius: 15px; background: black; }")
        
        self.glow_effect = QGraphicsDropShadowEffect(self)
        self.glow_effect.setBlurRadius(50)
        self.glow_effect.setXOffset(0)
        self.glow_effect.setYOffset(0)
        self.glow_effect.setColor(QColor("#00E5FF"))
        self.glow_frame.setGraphicsEffect(self.glow_effect)
        
        # Layout for video inside glow frame
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15) # Spacing for glow
        self.layout.addWidget(self.glow_frame)
        
        self.inner_layout = QVBoxLayout(self.glow_frame)
        self.inner_layout.setContentsMargins(0, 0, 0, 0)
        
        self.video_widget = QVideoWidget(self.glow_frame)
        self.inner_layout.addWidget(self.video_widget)
        
        # Floating Controls Overlay
        self.controls = FloatingControls(self)
        
        # Install event filter
        self.video_widget.setMouseTracking(True)
        self.video_widget.installEventFilter(self)
        
        # Glow Animation (Pulse)
        self.pulse_anim = QPropertyAnimation(self.glow_effect, b"blurRadius")
        self.pulse_anim.setDuration(2000)
        self.pulse_anim.setStartValue(20)
        self.pulse_anim.setEndValue(60)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Position controls relative to the glow frame
        c_height = self.controls.height()
        self.controls.setGeometry(15, self.height() - c_height - 15, self.width() - 30, c_height)

    def eventFilter(self, obj, event):
        if obj == self.video_widget and event.type() == QEvent.Type.MouseMove:
            self.controls.show_controls()
        return super().eventFilter(obj, event)

    def get_video_widget(self):
        return self.video_widget

