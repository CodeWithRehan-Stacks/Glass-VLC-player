
import os
from datetime import datetime

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def save_screenshot(player):
    desktop = get_desktop_path()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"GlassVLC_Shot_{timestamp}.png"
    filepath = os.path.join(desktop, filename)
    
    # VLC's video_take_snapshot(num, path, width, height)
    player.video_take_snapshot(0, filepath, 0, 0)
    return filepath