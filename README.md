# Ultra Premium AI Video Player

A commercial-grade, Netflix-inspired desktop media player built with Python and PySide6 / PyQt6.

## 🌟 Key Features
- **Cinematic UI**: Dark mode, glassmorphism, neon accents (`#00E5FF`, `#8A2BE2`).
- **Native Rendering**: Powered by `QtMultimedia` (zero external DLL dependencies like VLC!).
- **Smart Netflix Home**: Auto-saves your watch history and presents a "Continue Watching" dashboard.
- **Advanced Controls**: Precision seeking, playback speed control (0.5x to 2.0x), volume, fullscreen.
- **Modular Architecture**: Professional folder structure separating core logic, components, screens, and styles.

## 📂 Project Structure
```text
/video-player
 ├── assets/          # Images, logos
 ├── icons/           # App icons
 ├── styles/          # QSS Themes (theme.qss)
 ├── components/      # Reusable UI (controls.py)
 ├── core/            # Engine logic (engine.py)
 ├── screens/         # Layouts (home.py)
 ├── main.py          # Application entry point
 └── requirements.txt # Python dependencies
```

## 🚀 Installation & Usage
1. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
2. **Launch Application**:
   ```powershell
   python main.py
   ```

## 💡 Why QtMultimedia?
We transitioned the core engine from `python-vlc` to `PyQt6.QtMultimedia`. This eliminates the notorious `FileNotFoundError: libvlc.dll` issue, ensuring the application runs smoothly out-of-the-box on Windows, Mac, and Linux using native OS codecs and GPU acceleration.
