# Ultimate Media Suite (Nexus Studio)

A futuristic, AI-powered, cinematic multimedia platform combining the capabilities of VLC, Spotify, Netflix, Adobe Audition, and OBS Studio into a single, breathtaking desktop experience.

## 🚀 Features (Architectural Foundation)

### 🎬 Cinematic Player
- High-performance video rendering using `QtMultimedia` (hardware accelerated, zero DLL issues).
- Supports MP4, MKV, AVI, MOV, and high-res audio formats (FLAC, AAC, WAV).

### 🎚️ Live Audio Mixer
- Floating Adobe Audition-style mixing panel.
- Individual volume control channels for Master, Music, Video, Mic, and Radio.

### 📻 Global Radio
- Built-in internet radio streaming (Icecast/Shoutcast compatible).
- Browse and listen to global stations (Lofi, Jazz, Synthwave, Classical) with one click.

### 🎨 Audio Visualizer
- Real-time animated frequency spectrum analyzer.
- Reacts instantly to playback state with a beautiful Cyberpunk gradient (`#00E5FF` -> `#FF007F`).

### 💎 UI/UX Design
- **Futuristic Glassmorphism**: Built on a highly customized QSS theme (`themes/cyber.qss`).
- **Apple-Level Smoothness**: Liquid layout transitions and hover effects.

## 📂 Enterprise Project Structure
```text
/ultimate-media-suite
├── audio/          # Advanced audio engine wrappers
├── mixer/          # Adobe Audition-style panel (panel.py)
├── radio/          # Internet radio streaming (stations.py)
├── player/         # Video player logic
├── visualizer/     # Spectrum analyzer (analyzer.py)
├── themes/         # QSS Global Themes (cyber.qss)
├── main.py         # Nexus Studio Orchestrator
└── requirements.txt
```

## 🛠 Installation & Usage
1. **Requirements**: Python 3.12+
2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Run Nexus Studio**:
   ```powershell
   python main.py
   ```

## 🧠 Future AI Integrations (Planned Architecture)
The suite's modular structure (`ai/`, `recording/`, `effects/`) is designed to support:
- OpenAI Whisper for auto-subtitles.
- Librosa/PyAudio for real-time noise cancellation and smart EQ.
- OpenCV for dynamic background ambient lighting.
