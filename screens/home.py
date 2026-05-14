import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class HomeScreen(QWidget):
    file_selected = pyqtSignal(str)
    open_file_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HomeScreen")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        self.header = QLabel("Continue Watching")
        self.header.setObjectName("HeaderLabel")
        
        # Recent List
        self.recent_list = QListWidget()
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_open = QPushButton("Browse Files")
        self.btn_open.setObjectName("PrimaryButton")
        self.btn_open.setFixedWidth(200)
        
        btn_layout.addWidget(self.btn_open)
        btn_layout.addStretch()

        layout.addWidget(self.header)
        layout.addWidget(self.recent_list)
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
