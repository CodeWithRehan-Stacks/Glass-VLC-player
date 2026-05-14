import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap
import qtawesome as qta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.setFixedHeight(45)
        self.setObjectName("TitleBar")

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(15, 0, 8, 0)
        self._layout.setSpacing(8)

        # Logo
        self.icon_lbl = QLabel()
        logo_path = os.path.join(BASE, "resources", "logo.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(
                24, 24,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            self.icon_lbl.setPixmap(pix)
        else:
            self.icon_lbl.setPixmap(
                qta.icon('mdi.television-play', color="#00E5FF").pixmap(20, 20))
        self._layout.addWidget(self.icon_lbl)

        # Title (publicly accessible so main.py can update it)
        self.title = QLabel("NEXUS STUDIO")
        self.title.setStyleSheet(
            "color: #E2E8F0; font-weight: 900; letter-spacing: 2px; font-size: 11px;")
        self._layout.addWidget(self.title)
        self._layout.addStretch()

        # Window control buttons
        self.btn_min   = self._win_btn('mdi.minus',           "#A0AEC0")
        self.btn_max   = self._win_btn('mdi.window-maximize', "#A0AEC0")
        self.btn_close = self._win_btn('mdi.close',           "#A0AEC0")

        for btn in [self.btn_min, self.btn_max, self.btn_close]:
            btn.setFixedSize(45, 45)
            btn.setObjectName("TitleBtn")
            self._layout.addWidget(btn)

        self.btn_close.setStyleSheet(
            "QPushButton#TitleBtn:hover { background-color: #E81123; }")

        self.btn_min.clicked.connect(self._parent.showMinimized)
        self.btn_max.clicked.connect(self._toggle_maximize)
        self.btn_close.clicked.connect(self._parent.close)

        self._drag_pos = None

    # ── helpers ──────────────────────────────────────────────────────────────

    def _win_btn(self, icon_name, color):
        btn = QPushButton()
        btn.setIcon(qta.icon(icon_name, color=color))
        btn.setIconSize(QSize(16, 16))
        return btn

    def _toggle_maximize(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
            self.btn_max.setIcon(qta.icon('mdi.window-maximize', color="#A0AEC0"))
        else:
            self._parent.showMaximized()
            self.btn_max.setIcon(qta.icon('mdi.window-restore', color="#A0AEC0"))

    # ── drag to move ─────────────────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_pos:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self._parent.move(self._parent.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def mouseDoubleClickEvent(self, event):
        self._toggle_maximize()
