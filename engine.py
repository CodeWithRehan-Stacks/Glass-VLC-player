

import os
import sys

def find_vlc():
    # Common Windows paths for VLC
    search_paths = [
        r"C:\Program Files\VideoLAN\VLC",
        r"C:\Program Files (x86)\VideoLAN\VLC",
        os.environ.get('VLC_PATH', '')
    ]
    
    for path in search_paths:
        print(f"Searching for VLC in: {path}")
        if path and os.path.exists(os.path.join(path, "libvlc.dll")):
            print(f"FOUND VLC: {path}")
            return path
    return None

vlc_path = find_vlc()
if vlc_path:
    if os.name == 'nt' and sys.version_info >= (3, 8):
        os.add_dll_directory(vlc_path)
    else:
        os.environ['PATH'] = vlc_path + os.pathsep + os.environ['PATH']
else:
    print("CRITICAL: VLC Media Player not found!")
    print("Please install VLC (64-bit) from https://www.videolan.org/vlc/")

import vlc


class VLCEngine:
    def __init__(self, window_id):
        # Hardware acceleration flags for VLC
        args = [
            '--video-required',
            '--no-xlib',
            '--hwdec=auto',
        ]
        self.instance = vlc.Instance(args)
        self.player = self.instance.media_player_new()
        
        # Set window handle for rendering
        if os.name == 'nt':
            self.player.set_hwnd(window_id)
        else:
            self.player.set_xwindow(window_id)
            
    def load_media(self, file_path):
        if not os.path.exists(file_path):
            return False
        
        media = self.instance.media_new(file_path)
        self.player.set_media(media)
        
        # Auto-load subtitles if they exist
        base_path = os.path.splitext(file_path)[0]
        srt_path = base_path + ".srt"
        if os.path.exists(srt_path):
            self.player.video_set_subtitle_file(srt_path)
            
        return True
        
    def play(self):
        self.player.play()
        
    def pause(self):
        self.player.pause()
        
    def stop(self):
        self.player.stop()
        
    def set_volume(self, volume):
        self.player.audio_set_volume(volume)
        
    def set_position(self, pos):
        # pos is 0.0 to 1.0
        self.player.set_position(pos)
        
    def get_position(self):
        return self.player.get_position()
        
    def get_time(self):
        return self.player.get_time()
        
    def get_length(self):
        return self.player.get_length()
        
    def is_playing(self):
        return self.player.is_playing()

    def set_rate(self, rate):
        self.player.set_rate(rate)

    def toggle_fullscreen(self, state):
        self.player.set_fullscreen(state)
