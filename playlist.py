# playlist.py
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

class PlaylistWidget(QListWidget):
    """Playlist sidebar with drag & drop support."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PlaylistPanel")
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDefaultDropAction(Qt.MoveAction)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                    self.add_item(path)
            event.accept()
        else:
            event.ignore()
    
    def add_item(self, filepath):
        """Add a video file to the playlist."""
        # Extract filename for display
        import os
        name = os.path.basename(filepath)
        item = QListWidgetItem(name)
        item.setData(Qt.UserRole, filepath)  # store full path
        self.addItem(item)
    
    def get_current_file(self):
        """Return the filepath of the currently selected item."""
        item = self.currentItem()
        if item:
            return item.data(Qt.UserRole)
        return None