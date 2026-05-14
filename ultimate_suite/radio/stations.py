from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

class RadioPanel(QWidget):
    station_selected = pyqtSignal(str, str) # name, url

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RadioPanel")
        self.setProperty("class", "FloatingPanel")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("GLOBAL RADIO STATIONS")
        title.setStyleSheet("font-size: 16px; font-weight: 800; color: #00E5FF; letter-spacing: 2px;")
        self.layout.addWidget(title)
        
        self.grid = QGridLayout()
        
        # Mock Stations (In reality these would be streaming URLs like Icecast/Shoutcast)
        stations = [
            ("Lofi Girl", "https://streams.ilovemusic.de/iloveradio17.mp3", "Lo-Fi"),
            ("Jazz 24", "https://live.wostreaming.net/direct/ppm-jazz24aac256-ibc1", "Jazz"),
            ("BBC Radio 1", "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one", "Pop/Hits"),
            ("Classic FM", "http://media-ice.musicradio.com/ClassicFMMP3", "Classical"),
            ("Synthwave", "https://station.synthwave.hu/stream", "EDM/Synth"),
            ("Hip Hop Lounge", "http://icecast.commedia.org.uk:8000/resonance.mp3", "Hip-Hop")
        ]
        
        row = 0
        col = 0
        for name, url, genre in stations:
            btn = QPushButton(f"{name}\n({genre})")
            btn.setMinimumHeight(60)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(30, 30, 45, 180);
                    border: 1px solid rgba(138, 43, 226, 50);
                    border-radius: 8px;
                    color: #E2E8F0;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(0, 229, 255, 30);
                    border: 1px solid #00E5FF;
                }
            """)
            btn.clicked.connect(lambda checked, n=name, u=url: self.station_selected.emit(n, u))
            self.grid.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        self.layout.addLayout(self.grid)
        self.layout.addStretch()
