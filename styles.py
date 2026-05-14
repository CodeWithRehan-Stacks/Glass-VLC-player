

MAIN_STYLE = """
QMainWindow {
    background-color: rgba(10, 10, 10, 200);
    border-radius: 20px;
}

#TitleBar {
    background-color: rgba(20, 20, 20, 150);
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
    min-height: 50px;
}

#TitleLabel {
    color: #00f2ff;
    font-size: 16px;
    font-weight: 900;
    margin-left: 20px;
    letter-spacing: 1px;
}

#ControlPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(20, 20, 20, 0), stop:1 rgba(10, 10, 10, 230));
    border-bottom-left-radius: 20px;
    border-bottom-right-radius: 20px;
    min-height: 120px;
}

#PlaylistPanel {
    background-color: rgba(15, 15, 15, 180);
    border-left: 1px solid rgba(0, 242, 255, 30);
}

QPushButton {
    background-color: transparent;
    border-radius: 8px;
    color: #e0e0e0;
    padding: 8px;
    font-size: 18px;
    transition: all 0.3s ease;
}

QPushButton:hover {
    background-color: rgba(0, 242, 255, 40);
    color: #00f2ff;
    border: 1px solid rgba(0, 242, 255, 100);
}

QPushButton#PrimaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7000ff, stop:1 #00f2ff);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 12px;
}

QSlider::groove:horizontal {
    border: 1px solid #1a1a1a;
    height: 4px;
    background: rgba(255, 255, 255, 10);
    margin: 2px 0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #00f2ff;
    border: 2px solid #00f2ff;
    width: 12px;
    height: 12px;
    margin: -5px 0;
    border-radius: 6px;
    box-shadow: 0 0 10px #00f2ff;
}

QListWidget {
    background: transparent;
    border: none;
    color: #cccccc;
    font-size: 14px;
    outline: none;
}

QListWidget::item {
    padding: 12px;
    border-radius: 10px;
    margin: 4px 10px;
}

QListWidget::item:hover {
    background: rgba(255, 255, 255, 10);
}

QListWidget::item:selected {
    background: rgba(112, 0, 255, 50);
    border: 1px solid #7000ff;
    color: white;
}

#VideoWidget {
    background-color: #000;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 10);
}

QLabel {
    color: #999;
    font-size: 12px;
}

#TimeLabel {
    color: #00f2ff;
    font-family: 'Consolas', monospace;
    font-size: 14px;
}
"""