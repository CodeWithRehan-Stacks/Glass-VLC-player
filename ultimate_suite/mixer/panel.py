from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt6.QtCore import Qt

class AudioChannel(QWidget):
    def __init__(self, name, default_val=70, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 100)
        self.slider.setValue(default_val)
        self.slider.setMinimumHeight(150)
        
        self.val_label = QLabel(f"{default_val}%")
        self.val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.name_label = QLabel(name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("color: #8A2BE2; font-weight: bold; font-size: 10px;")

        self.layout.addWidget(self.val_label)
        self.layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.name_label)
        
        self.slider.valueChanged.connect(lambda v: self.val_label.setText(f"{v}%"))

class MixerPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MixerPanel")
        self.setProperty("class", "FloatingPanel")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("LIVE AUDIO MIXER")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #00E5FF; letter-spacing: 2px;")
        self.layout.addWidget(title)
        
        self.channels_layout = QHBoxLayout()
        
        self.ch_master = AudioChannel("MASTER", 80)
        self.ch_music = AudioChannel("MUSIC", 100)
        self.ch_video = AudioChannel("VIDEO", 70)
        self.ch_mic = AudioChannel("MIC", 0)
        self.ch_radio = AudioChannel("RADIO", 50)
        
        # Style Master differently if needed
        self.ch_master.name_label.setStyleSheet("color: #FF007F; font-weight: bold; font-size: 12px;")
        
        self.channels_layout.addWidget(self.ch_master)
        self.channels_layout.addWidget(self.ch_music)
        self.channels_layout.addWidget(self.ch_video)
        self.channels_layout.addWidget(self.ch_mic)
        self.channels_layout.addWidget(self.ch_radio)
        
        self.layout.addLayout(self.channels_layout)
