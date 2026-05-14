🎬 GlassVLC Player
A high‑end, dark glassmorphism video player built with PyQt5 and VLC backend.
Inspired by VLC, Netflix, and Apple UI — minimal, premium, and responsive.

https://img.shields.io/badge/python-3.8+-blue?logo=python
https://img.shields.io/badge/PyQt5-5.15.9-green?logo=qt
https://img.shields.io/badge/VLC-3.0+-orange?logo=videolan
https://img.shields.io/badge/license-MIT-lightgrey

https://via.placeholder.com/800x450/121212/64c8ff?text=GlassVLC+Player+Screenshot

✨ Features
🚀 Dark Glassmorphism UI – Semi‑transparent panels, blur effects, neon cyan accents.

🎬 Full VLC Backend – Hardware‑accelerated playback for MP4, MKV, AVI, MOV.

📺 Picture‑in‑Picture (PiP) – Float the player on top of other windows.

📂 Playlist Sidebar – Drag‑and‑drop support, double‑click to play, recent files.

📸 Screenshot Capture – Save high‑quality frames directly to your Desktop.

🌓 Theme Switcher – (Planned) Toggle between Dark and Light glass modes.

🗗 Mini Player – Collapse the UI to a minimal floating window (via PiP mode).

⌨️ Keyboard Shortcuts:

Space – Play / Pause

F – Fullscreen / Normal

Left / Right Arrow – Seek ±5 seconds

Up / Down Arrow – Volume ±5%

⏯️ Speed Control – 0.25x to 2.0x playback speed.

🧩 Subtitle Support – Auto‑loads .srt files with same name as video.

📦 Installation
Prerequisites
VLC Media Player – MUST be installed on your system.
Download from videolan.org/vlc.
Default installation paths:

Windows: C:\Program Files\VideoLAN\VLC

Linux: /usr/lib/vlc (or via package manager)

macOS: /Applications/VLC.app

Python 3.8+

Install Python dependencies
bash
pip install -r requirements.txt
Or manually:

bash
pip install PyQt5 python-vlc
Clone the repository
bash
git clone https://github.com/yourusername/GlassVLC-Player.git
cd GlassVLC-Player
🚀 Usage
Run the app from the terminal:

bash
python main.py
First launch
The app will show a splash screen (animated loading).

Recent videos are automatically loaded from recent.json.

Drag & drop video files onto the main window or the playlist sidebar.

Playlist management
Add files – Drag & drop onto the playlist area.

Play – Double‑click any item in the playlist.

Recent files – Automatically saved; up to 20 entries.

Controls overview
Control Action
▶ / ⏸ Play / Pause
⏹ Stop
⏪ / ⏩ Rewind 10s / Forward 10s
🔊 slider Volume (0–100)
Speed dropdown 0.25x – 2.0x
⛶ Toggle fullscreen
📷 Capture screenshot to Desktop
▣ Enable Picture‑in‑Picture
🧰 Project Structure
text
GlassVLC-Player/
│
├── main.py # Entry point, splash screen, app init
├── player.py # Main window (QMainWindow) with VLC integration
├── controls.py # Custom controls panel (play, seek, volume, speed)
├── playlist.py # Playlist sidebar with drag & drop
├── styles.py # QSS glassmorphism / dark theme
├── utils.py # Time formatting, recent file management
├── requirements.txt # Python dependencies
├── resources/ # Icons, splash screen image (place PNGs here)
│ ├── icon.png
│ └── splash.png
└── README.md
🖼️ Custom Icons & Splash
Place your own icon.png and splash.png inside the resources/ folder.
If no images are found, the app falls back to a plain black splash screen and a default window icon.

⚙️ Configuration
The app stores recently played videos in recent.json (created automatically in the same directory as main.py). You can edit this file manually to clear or reorder the playlist.

🐞 Troubleshooting
FileNotFoundError: Could not find module 'libvlc.dll'
Solution: Make sure VLC is installed in its default location.

If you installed VLC elsewhere, add the path to vlc_paths in engine.py (if you have such a file) or set the environment variable PYTHON_VLC_LIB_PATH.

ImportError: No module named 'PyQt5'
Run pip install PyQt5.

Video plays but no audio
Check your system volume and the app’s volume slider.

Ensure VLC’s audio output is correctly configured (usually automatic).

Subtitle not loading
Place an .srt file with the exact same name as the video file in the same folder.

Example: movie.mp4 and movie.srt.

🌐 Cross‑Platform Support
Platform Status
Windows 10/11 ✅ Fully tested
Linux (Ubuntu 22.04+) ✅ Works with libvlc-dev
macOS (Monterey+) ✅ Requires VLC in /Applications
On Linux, you may need to install VLC development headers:

bash
sudo apt install vlc libvlc-dev
📄 License
This project is released under the MIT License.
Feel free to use, modify, and distribute it as you like.

🙏 Acknowledgements
python‑vlc – Python bindings for VLC

PyQt5 – Qt bindings for Python

VLC Media Player – The powerful media engine behind this player
