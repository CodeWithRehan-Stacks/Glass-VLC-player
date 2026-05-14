import os
import json
import qtawesome as qta
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QScrollArea, QFrame, QPushButton, QGridLayout,
                             QListWidget, QListWidgetItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt6.QtGui import QLinearGradient, QColor, QPainter, QBrush, QPainterPath, QPixmap, QFont


class GlassCard(QFrame):
    """A reusable Glassmorphism card widget."""
    clicked = pyqtSignal()

    def __init__(self, title="", subtitle="", icon_name="mdi.play", parent=None):
        super().__init__(parent)
        self.setObjectName("GlassCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(160, 120)
        self.setMaximumSize(200, 150)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon(icon_name, color="#00E5FF").pixmap(QSize(36, 36)))
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: 700;")
        
        sub_lbl = QLabel(subtitle)
        sub_lbl.setStyleSheet("color: #718096; font-size: 11px;")

        layout.addWidget(icon_lbl)
        layout.addWidget(title_lbl)
        layout.addWidget(sub_lbl)
        layout.addStretch()

    def mousePressEvent(self, event):
        self.clicked.emit()


class SectionHeader(QLabel):
    """Premium section header with a neon left accent."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            color: #FFFFFF; 
            font-size: 18px; 
            font-weight: 800;
            padding-left: 14px;
            border-left: 4px solid #00E5FF;
            margin-bottom: 15px;
        """)


class RecentItem(QWidget):
    """A single card in the 'Continue Watching' row."""
    play_clicked = pyqtSignal(str)

    def __init__(self, file_path, progress=0, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.setFixedSize(220, 145)
        self.setObjectName("RecentItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # Icon + Title
        fname = os.path.basename(file_path)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon('mdi.movie-outline', color="#00E5FF").pixmap(QSize(28, 28)))

        title_lbl = QLabel(fname[:28] + "..." if len(fname) > 28 else fname)
        title_lbl.setStyleSheet("color: #E2E8F0; font-weight: 600; font-size: 12px;")
        title_lbl.setWordWrap(True)

        # Progress Bar
        progress_frame = QFrame()
        progress_frame.setFixedHeight(4)
        progress_frame.setStyleSheet("background: rgba(255,255,255,15); border-radius: 2px;")
        progress_inner = QFrame(progress_frame)
        progress_inner.setGeometry(0, 0, int(progress * 2.2), 4)
        progress_inner.setStyleSheet(f"background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #8A2BE2,stop:1 #00E5FF); border-radius: 2px;")

        layout.addWidget(icon_lbl)
        layout.addWidget(title_lbl)
        layout.addStretch()
        layout.addWidget(progress_frame)

    def mousePressEvent(self, event):
        self.play_clicked.emit(self.file_path)


class QuickTile(QFrame):
    """Netflix-style Quick Action Tile."""
    clicked_signal = pyqtSignal(int)

    def __init__(self, icon, label, gradient_start, gradient_end, tab_index, parent=None):
        super().__init__(parent)
        self.tab_index = tab_index
        self.gradient_start = QColor(gradient_start)
        self.gradient_end = QColor(gradient_end)
        self.setObjectName("QuickTile")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(180, 100)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon(icon, color="white").pixmap(QSize(30, 30)))
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: white; font-size: 13px; font-weight: 700;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon_lbl)
        layout.addWidget(lbl)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 16, 16)
        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0, self.gradient_start)
        grad.setColorAt(1, self.gradient_end)
        painter.fillPath(path, QBrush(grad))
        super().paintEvent(event)

    def mousePressEvent(self, event):
        self.clicked_signal.emit(self.tab_index)


class DashboardView(QWidget):
    """The main Netflix/Apple TV style Home Dashboard."""
    navigate_to = pyqtSignal(int)
    file_play_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardView")
        self.recent_files = []

        # Outer scrollable layout
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.layout = QVBoxLayout(content)
        self.layout.setContentsMargins(30, 20, 30, 40)
        self.layout.setSpacing(30)

        # --- Hero Section ---
        hero = QFrame()
        hero.setObjectName("HeroSection")
        hero.setFixedHeight(200)
        hero.setStyleSheet("""
            #HeroSection {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 rgba(138,43,226,120),
                    stop:0.5 rgba(0,100,180,80),
                    stop:1 rgba(0,229,255,50));
                border-radius: 20px;
                border: 1px solid rgba(0,229,255,40);
            }
        """)
        hero_layout = QVBoxLayout(hero)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        hero_layout.setContentsMargins(35, 25, 35, 25)

        greeting = QLabel("Welcome to Nexus Studio")
        greeting.setStyleSheet("color: #FFFFFF; font-size: 28px; font-weight: 900; letter-spacing: 1px;")
        sub_greeting = QLabel("Your AI-powered cinematic multimedia platform is ready.")
        sub_greeting.setStyleSheet("color: rgba(255,255,255,180); font-size: 14px;")

        btn_open = QPushButton("  Open Media File")
        btn_open.setIcon(qta.icon('mdi.folder-open', color="white"))
        btn_open.setIconSize(QSize(18, 18))
        btn_open.setObjectName("HeroButton")
        btn_open.setFixedWidth(200)
        btn_open.clicked.connect(lambda: self.navigate_to.emit(-1))  # -1 = open file

        hero_layout.addWidget(greeting)
        hero_layout.addWidget(sub_greeting)
        hero_layout.addSpacing(10)
        hero_layout.addWidget(btn_open)
        self.layout.addWidget(hero)

        # --- Quick Access Tiles ---
        tiles_header = SectionHeader("Quick Access")
        self.layout.addWidget(tiles_header)

        tiles_row = QHBoxLayout()
        tiles_row.setSpacing(15)

        tiles_data = [
            ('mdi.movie-play', 'Cinema Player', '#1a1a4e', '#8A2BE2', 1),
            ('mdi.tune', 'Audio Mixer', '#0d2b1a', '#00C853', 2),
            ('mdi.radio', 'Live Radio', '#2b1a1a', '#FF4444', 3),
            ('mdi.playlist-music', 'Library', '#1a2b2b', '#00E5FF', 4),
        ]

        for icon, label, c1, c2, idx in tiles_data:
            tile = QuickTile(icon, label, c1, c2, idx)
            tile.clicked_signal.connect(self.navigate_to.emit)
            tiles_row.addWidget(tile)

        tiles_row.addStretch()
        self.layout.addLayout(tiles_row)

        # --- Continue Watching ---
        self.continue_header = SectionHeader("Continue Watching")
        self.layout.addWidget(self.continue_header)

        self.continue_scroll = QScrollArea()
        self.continue_scroll.setFixedHeight(160)
        self.continue_scroll.setWidgetResizable(True)
        self.continue_scroll.setStyleSheet("background: transparent; border: none;")
        self.continue_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.continue_content = QWidget()
        self.continue_content.setStyleSheet("background: transparent;")
        self.continue_row = QHBoxLayout(self.continue_content)
        self.continue_row.setContentsMargins(0, 0, 0, 0)
        self.continue_row.setSpacing(15)
        self.continue_row.addStretch()
        self.continue_scroll.setWidget(self.continue_content)
        self.layout.addWidget(self.continue_scroll)

        # --- Status Panel ---
        status_header = SectionHeader("System Status")
        self.layout.addWidget(status_header)

        status_grid = QGridLayout()
        status_grid.setSpacing(15)

        status_items = [
            ('mdi.memory', '#00E5FF', 'Engine', 'QtMultimedia  •  Active'),
            ('mdi.shield-check', '#00C853', 'Status', 'All Systems Operational'),
            ('mdi.radio-tower', '#FF9800', 'Radio', '6 Stations Available'),
            ('mdi.clock-fast', '#8A2BE2', 'Performance', '60 FPS  •  GPU Accelerated'),
        ]

        for i, (icon, color, title, val) in enumerate(status_items):
            card = QFrame()
            card.setObjectName("StatusCard")
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(15, 12, 15, 12)
            card_layout.setSpacing(12)

            icon_lbl = QLabel()
            icon_lbl.setPixmap(qta.icon(icon, color=color).pixmap(QSize(24, 24)))
            icon_lbl.setFixedSize(32, 32)

            text_col = QVBoxLayout()
            t = QLabel(title)
            t.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
            v = QLabel(val)
            v.setStyleSheet("color: #E2E8F0; font-size: 12px; font-weight: 600;")
            text_col.addWidget(t)
            text_col.addWidget(v)

            card_layout.addWidget(icon_lbl)
            card_layout.addLayout(text_col)
            card_layout.addStretch()

            status_grid.addWidget(card, i // 2, i % 2)

        self.layout.addLayout(status_grid)
        self.layout.addStretch()

        scroll.setWidget(content)
        self.outer_layout.addWidget(scroll)

    def populate_recent(self, files, memory=None):
        # Clear old
        while self.continue_row.count() > 1:
            item = self.continue_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for f in files:
            progress = 0
            if memory and f in memory:
                pos = memory.get(f, 0)
                progress = min(100, int(pos / 1000))
            card = RecentItem(f, progress)
            card.play_clicked.connect(self.file_play_requested.emit)
            self.continue_row.insertWidget(self.continue_row.count() - 1, card)

        if not files:
            empty = QLabel("No recent files yet. Open a media file to get started.")
            empty.setStyleSheet("color: #4A5568; font-size: 13px; padding: 20px;")
            self.continue_row.insertWidget(0, empty)
