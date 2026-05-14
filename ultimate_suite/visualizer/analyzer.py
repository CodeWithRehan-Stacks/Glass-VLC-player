import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QBrush

class VisualizerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Visualizer")
        self.bars = 32
        self.values = [random.randint(10, 100) for _ in range(self.bars)]
        self.target_values = [random.randint(10, 100) for _ in range(self.bars)]
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_visuals)
        self.timer.start(50)  # 20 FPS

        self.is_active = False

    def set_active(self, active: bool):
        self.is_active = active
        if not active:
            self.target_values = [5 for _ in range(self.bars)]

    def update_visuals(self):
        if self.is_active:
            # Generate new targets randomly for simulation
            # In a real app, this data comes from Librosa/PyAudio FFT analysis
            if random.random() < 0.3:
                self.target_values = [random.randint(10, 100) for _ in range(self.bars)]
        
        # Smooth interpolation
        for i in range(self.bars):
            diff = self.target_values[i] - self.values[i]
            self.values[i] += diff * 0.2

        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        bar_width = w / self.bars
        spacing = 4
        
        # Cyberpunk Gradient
        gradient = QLinearGradient(0, h, 0, 0)
        gradient.setColorAt(0.0, QColor("#00E5FF")) # Neon Blue
        gradient.setColorAt(0.5, QColor("#8A2BE2")) # Purple
        gradient.setColorAt(1.0, QColor("#FF007F")) # Pink peak
        
        painter.setPen(Qt.PenStyle.NoPen)
        
        for i in range(self.bars):
            val = self.values[i] / 100.0
            bar_h = (h * 0.7) * val  # Leave room for peak highlight
            
            # Main Bar
            painter.setBrush(QBrush(gradient))
            rect = QRectF(i * bar_width + spacing/2, h/2 - bar_h/2, bar_width - spacing, bar_h)
            painter.drawRoundedRect(rect, 4, 4)
            
            # Peak Highlight (White Neon)
            if val > 0.1:
                painter.setBrush(QBrush(QColor("#FFFFFF")))
                peak_rect = QRectF(i * bar_width + spacing/2, h/2 - bar_h/2, bar_width - spacing, 2)
                painter.drawRect(peak_rect)
                
                # Mirror Peak
                mirror_peak = QRectF(i * bar_width + spacing/2, h/2 + bar_h/2 - 2, bar_width - spacing, 2)
                painter.drawRect(mirror_peak)

