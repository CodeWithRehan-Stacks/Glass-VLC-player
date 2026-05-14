import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QScrollArea
from PyQt6.QtCore import Qt, QPropertyAnimation, QSize, pyqtSignal
from PyQt6.QtGui import QPixmap
import qtawesome as qta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SidebarItem(QPushButton):
    """A single sidebar navigation button — icon + label, collapsible."""

    def __init__(self, icon_name, label, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setObjectName("SidebarItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(label)
        self.setFixedHeight(48)

        self.icon_name  = icon_name
        self.label_text = label

        self.setIcon(qta.icon(icon_name, color="#718096"))
        self.setIconSize(QSize(22, 22))
        self.setText("  " + label)

    def set_active(self, active: bool):
        self.setChecked(active)
        self.setIcon(qta.icon(self.icon_name,
                              color="#00E5FF" if active else "#718096"))

    def show_label(self, visible: bool):
        self.setText(("  " + self.label_text) if visible else "")


class Sidebar(QFrame):
    """
    Collapsible sidebar — icon-only when collapsed, icon + label when hovered.
    Emits tab_changed(int) when a nav item is clicked.
    """
    tab_changed = pyqtSignal(int)

    COLLAPSED_W = 68
    EXPANDED_W  = 220

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(self.COLLAPSED_W)
        self._expanded = False

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Logo area ────────────────────────────────────────────────────────
        logo_frame = QFrame()
        logo_frame.setFixedHeight(64)
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(0, 10, 0, 10)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_lbl = QLabel()
        logo_path = os.path.join(BASE, "resources", "logo.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(
                32, 32,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            self.logo_lbl.setPixmap(pix)
        else:
            self.logo_lbl.setPixmap(
                qta.icon('mdi.television-play', color="#00E5FF").pixmap(32, 32))
        self.logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.app_name_lbl = QLabel("NEXUS")
        self.app_name_lbl.setStyleSheet(
            "color: #FFFFFF; font-size: 13px; font-weight: 900; letter-spacing: 3px;")
        self.app_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_name_lbl.setVisible(False)

        logo_layout.addWidget(self.logo_lbl)
        logo_layout.addWidget(self.app_name_lbl)
        outer.addWidget(logo_frame)

        # Thin divider
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet("background: rgba(255,255,255,10);")
        outer.addWidget(div)

        # ── Scrollable nav items ─────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self._items_layout = QVBoxLayout(scroll_content)
        self._items_layout.setContentsMargins(8, 12, 8, 12)
        self._items_layout.setSpacing(4)

        nav_defs = [
            ('mdi.view-dashboard-outline', "Dashboard", 0),
            ('mdi.movie-play-outline',     "Cinema",    1),
            ('mdi.tune-vertical',          "Mixer",     2),
            ('mdi.radio',                  "Radio",     3),
            ('mdi.playlist-music-outline', "Library",   4),
            ('mdi.history',                "History",   5),
        ]
        self._items: list[SidebarItem] = []
        for icon, label, idx in nav_defs:
            self._add_item(icon, label, idx)

        self._items_layout.addStretch()

        # Settings pinned at bottom
        self._add_item('mdi.cog-outline', "Settings", 6)

        scroll.setWidget(scroll_content)
        outer.addWidget(scroll, stretch=1)

        # ── Width animation ──────────────────────────────────────────────────
        self._w_anim = QPropertyAnimation(self, b"minimumWidth")
        self._w_anim.setDuration(220)
        self._w_anim2 = QPropertyAnimation(self, b"maximumWidth")
        self._w_anim2.setDuration(220)

        # Initialise first item active
        if self._items:
            self._items[0].set_active(True)

    # ── internal helpers ──────────────────────────────────────────────────────

    def _add_item(self, icon, label, idx):
        item = SidebarItem(icon, label)
        item.show_label(False)   # start collapsed
        item.clicked.connect(lambda _, i=idx: self._on_clicked(i))
        self._items.append(item)
        self._items_layout.addWidget(item)

    def _on_clicked(self, index):
        for i, item in enumerate(self._items):
            item.set_active(i == index)
        self.tab_changed.emit(index)

    # ── public API ────────────────────────────────────────────────────────────

    def _on_item_clicked(self, index):
        """Called by main.py to sync active state without emitting tab_changed."""
        for i, item in enumerate(self._items):
            item.set_active(i == index)

    # ── hover expand / collapse ───────────────────────────────────────────────

    def _set_width(self, w):
        self._w_anim.stop(); self._w_anim2.stop()
        self._w_anim.setEndValue(w); self._w_anim2.setEndValue(w)
        self._w_anim.start();  self._w_anim2.start()

    def enterEvent(self, event):
        self._expanded = True
        self._set_width(self.EXPANDED_W)
        self.app_name_lbl.setVisible(True)
        for item in self._items:
            item.show_label(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._expanded = False
        self._set_width(self.COLLAPSED_W)
        self.app_name_lbl.setVisible(False)
        for item in self._items:
            item.show_label(False)
        super().leaveEvent(event)
