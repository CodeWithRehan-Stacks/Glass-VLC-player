import os
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLineEdit, QPushButton, 
                             QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QColor
import qtawesome as qta

class TopBar(QFrame):
    search_triggered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TopBar")
        self.setFixedHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 8, 20, 8)
        layout.setSpacing(12)

        # Global Search
        search_frame = QFrame()
        search_frame.setObjectName("SearchFrame")
        search_frame.setFixedWidth(380)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(12, 0, 12, 0)
        search_layout.setSpacing(8)

        search_icon = QLabel()
        search_icon.setPixmap(qta.icon('mdi.magnify', color="#718096").pixmap(18, 18))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search media, radio, files...")
        self.search_input.setObjectName("SearchInput")
        self.search_input.returnPressed.connect(lambda: self.search_triggered.emit(self.search_input.text()))

        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)

        layout.addWidget(search_frame)
        layout.addStretch()

        # Quick Action Buttons
        self.btn_ai = self._icon_btn('mdi.robot', "AI Assistant", "#8A2BE2")
        self.btn_notify = self._icon_btn('mdi.bell-outline', "Notifications", "#A0AEC0")
        self.btn_theme = self._icon_btn('mdi.brightness-6', "Theme", "#A0AEC0")
        self.btn_profile = self._icon_btn('mdi.account-circle', "Profile", "#00E5FF")

        for btn in [self.btn_ai, self.btn_notify, self.btn_theme, self.btn_profile]:
            layout.addWidget(btn)

    def _icon_btn(self, icon, tooltip, color):
        btn = QPushButton()
        btn.setIcon(qta.icon(icon, color=color))
        btn.setIconSize(QSize(22, 22))
        btn.setObjectName("TopBarBtn")
        btn.setToolTip(tooltip)
        btn.setFixedSize(40, 40)
        return btn
