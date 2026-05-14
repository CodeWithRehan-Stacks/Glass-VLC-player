
import os
import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QSize

class HomeScreen(QWidget):
    file_selected = pyqtSignal(str)
    open_file_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HomeScreen")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header_layout = QHBoxLayout()
        self.header_icon = QLabel()
        self.header_icon.setPixmap(qta.icon('mdi.history', color="#00E5FF").pixmap(QSize(32, 32)))
        
        self.header = QLabel("Continue Watching")
        self.header.setObjectName("HeaderLabel")
        
        header_layout.addWidget(self.header_icon)
        header_layout.addWidget(self.header)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Recent List
        self.recent_list = QListWidget()
        layout.addWidget(self.recent_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_open = QPushButton(" Browse Files")
        self.btn_open.setIcon(qta.icon('mdi.folder-open', color="white"))
        self.btn_open.setObjectName("PrimaryButton")
        self.btn_open.setFixedWidth(200)
        self.btn_open.setIconSize(QSize(20, 20))
        
        btn_layout.addWidget(self.btn_open)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # Connections
        self.btn_open.clicked.connect(self.open_file_clicked.emit)
        self.recent_list.itemDoubleClicked.connect(self._on_item_double_clicked)

    def _on_item_double_clicked(self, item):
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.file_selected.emit(file_path)

    def populate_recent(self, files: list):
        self.recent_list.clear()
        for f in files:
            if os.path.exists(f):
                self.recent_list.addItem(os.path.basename(f))
                self.recent_list.item(self.recent_list.count()-1).setData(Qt.ItemDataRole.UserRole, f)
                self.recent_list.item(self.recent_list.count()-1).setIcon(qta.icon('mdi.movie-outline', color="#00E5FF"))
