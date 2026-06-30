# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETE README.md - DETAILED DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
 
readme = '''# ⚡ JOKERATC v2.0 - Cyberpunk Terminal Interface

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-orange)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

> **A futuristic, sci-fi inspired terminal interface inspired by eDEX-UI but built with modern Python.**

![JokerATC Screenshot](screenshot.png)

---

## 📖 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Controls](#-controls)
- [Terminal Commands](#-terminal-commands)
- [Themes](#-themes)
- [Sound Effects](#-sound-effects)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🖥️ System Monitoring
- **Real-time CPU** usage with per-core monitoring and frequency display
- **RAM usage** with visual progress bars and swap monitoring
- **Disk usage** for all partitions with percentage indicators
- **Temperature monitoring** (CPU/GPU sensors with critical thresholds)
- **Network speed** with real-time download/upload rates (KB/s)
- **Process viewer** with top CPU/memory consumers and kill functionality

### 🎨 Visual Effects
- **6 Unique Themes**: TRON, MATRIX, CYBERPUNK, AMBER, NEON, OCEAN
- **Matrix Rain** animation with Katakana, Greek, and Hex characters
- **Smooth animations** and transitions at configurable speeds
- **ASCII art banners** and boot sequences
- **Color-coded** system status indicators (green/yellow/red)
- **Responsive layout** that adapts to terminal size

### 🔊 Sound Effects
- **Boot sound** - Futuristic power-up sequence with frequency sweep
- **Typing sounds** - Tech blips on every keystroke
- **Ambient drone** - Background atmosphere (10-second loop)
- **Alert sounds** - Warning beeps for errors
- **Success chimes** - Positive feedback (major chord arpeggio)
- **Hover effects** - UI interaction sounds
- **Volume control** per sound type

### 💻 Terminal
- **Built-in command processor** with 15+ commands
- **Command history** and autocomplete hints
- **Shell command execution** with 5-second safety timeout
- **Colored output** with syntax highlighting
- **Help system** with command documentation
- **Neofetch-style** system info display

### 📁 File Explorer
- **Directory tree** with file icons (emoji based on file type)
- **File size** display (B, KB, MB, GB auto-formatting)
- **File type detection** with 20+ icon mappings
- **Real-time updates** every second
- **Permission handling** with graceful error messages

### 🌐 Network Monitoring
- **Network interfaces** with IP addresses
- **Real-time speed** bars for download/upload
- **Total traffic** statistics (GB received/sent)
- **Ping functionality** from terminal
- **Packet counters** (RX/TX)

---

## 📸 Screenshots

### TRON Theme (Default)
```
╔══════════════════════════════════════════════════════════════════════╗
║  ⚡ JOKERATC v2.0 - Cyberpunk Terminal Interface    joker@kali      ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ System Stats ───────────────────┬─ Terminal ──────────────────────┐
│ ◉ SYSTEM MONITOR                 │ 💻 TERMINAL                    │
│ CPU  23.5% (8C)  ████░░░░░░░░░░ │ ┌──(user@jokeratc)-[~]         │
│ RAM  4.2/16 GB   ███████░░░░░░░ │ └─▶ help                       │
│ DISK 45%         █████████░░░░░ │ Available Commands:            │
│ TEMP 42.0°C      ████████░░░░░░ │   help, sysinfo, theme...      │
│ NET ↓ 15.4 GB    NET ↑ 3.2 GB   │                                │
└──────────────────────────────────┴────────────────────────────────┘

┌─ Time ────────┬─ Matrix ───────┬─ Files ───────┬─ Processes ─────┐
│ 🕐 TIME       │ 🌧️ MATRIX RAIN│ 📂 FILE       │ ⚡ PROCESSES     │
│ 18:06:42      │ ｱｲｳｴｵｶｷｸｹｺ    │ 📁 /home/joker│ PID  NAME  CPU% │
│ Tue, 30 Jun   │ 0123456789    │ 📂 .config    │ 1234 python 12% │
│ Week 26       │ ABCDEF        │ 🐍 main.py    │ 5678 chrome  8% │
└───────────────┴────────────────┴───────────────┴─────────────────┘

Q Quit  R Refresh  T Theme  S Sound  M Matrix
```

---

## 🚀 Installation

### Prerequisites
- **Python 3.8 or higher**
- **pip** package manager
- **Terminal with Unicode support** (for best experience)

### Method 1: Using install.py (Recommended)
```bash
# Clone or download the project
git clone https://github.com/yourusername/jokeratc.git
cd jokeratc

# Run the auto-installer
python install.py
```

### Method 2: Manual Installation
```bash
# Install dependencies manually
pip install textual rich psutil pygame

# Run JokerATC
python main.py
```

### Method 3: Using start scripts
```bash
# Linux/macOS
chmod +x start.sh
./start.sh

# Windows
start.bat
```

---

## 🎮 Quick Start

```bash
# 1. Navigate to project directory
cd jokeratc

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run JokerATC
python main.py

# 4. Enjoy the cyberpunk interface!
```

### First Run
On first run, JokerATC will:
1. Check all dependencies
2. Generate default configuration (`config.json`)
3. Play the boot sound sequence
4. Start the ambient background drone
5. Display the main interface

---

## 🎮 Controls

| Key | Action | Description |
|-----|--------|-------------|
| `Q` | Quit | Exit JokerATC gracefully |
| `R` | Refresh | Manually refresh all widgets |
| `T` | Theme | Cycle through available themes |
| `S` | Sound | Toggle sound effects on/off |
| `M` | Matrix | Toggle matrix rain animation |
| `F5` | Refresh | Alternative refresh key |
| `Ctrl+C` | Force Quit | Emergency exit |

### Terminal Shortcuts
- **Up/Down arrows** - Navigate command history
- **Tab** - Auto-complete commands
- **Enter** - Execute command
- **Ctrl+L** - Clear terminal

---

## 💻 Terminal Commands

### System Commands
| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show all available commands | `help` |
| `clear` | Clear terminal screen | `clear` |
| `sysinfo` | Display system information | `sysinfo` |
| `neofetch` | ASCII art system info | `neofetch` |
| `whoami` | Show current user | `whoami` |
| `uptime` | Show system uptime | `uptime` |

### Theme Commands
| Command | Description | Example |
|---------|-------------|---------|
| `theme` | List all themes | `theme` |
| `theme <name>` | Switch to theme | `theme matrix` |

### Control Commands
| Command | Description | Example |
|---------|-------------|---------|
| `sound` | Toggle sound on/off | `sound` |
| `matrix` | Toggle matrix rain | `matrix` |
| `reboot` | Simulate system reboot | `reboot` |
| `shutdown` | Exit JokerATC | `shutdown` |

### Monitoring Commands
| Command | Description | Example |
|---------|-------------|---------|
| `ps` | List running processes | `ps` |
| `net` | Show network information | `net` |
| `ping <host>` | Ping a host | `ping google.com` |

### Fun Commands
| Command | Description | Example |
|---------|-------------|---------|
| `banner` | Show JokerATC ASCII banner | `banner` |

### Shell Commands
Any standard shell command can be executed:
```
ls -la
cat file.txt
echo "Hello World"
```
*(Commands run with 5-second timeout for safety)*

---

## 🎨 Themes

### TRON (Default)
```
Primary:   #00ff88 (Green)
Secondary: #00ccff (Cyan)
Accent:    #ff0066 (Pink)
Background: #000510
```
Futuristic green and cyan interface inspired by TRON Legacy.

### MATRIX
```
Primary:   #00ff41 (Matrix Green)
Secondary: #008f11 (Dark Green)
Accent:    #003b00 (Very Dark Green)
Background: #000000
```
Classic green Matrix code rain with pure black background.

### CYBERPUNK 2077
```
Primary:   #ff00ff (Neon Pink)
Secondary: #00ffff (Neon Cyan)
Accent:    #ffff00 (Yellow)
Background: #0a0a1a
```
Vibrant neon pink and cyan cyberpunk aesthetic.

### AMBER CRT
```
Primary:   #ffb000 (Amber)
Secondary: #ff8800 (Dark Amber)
Accent:    #ff4400 (Orange)
Background: #1a0a00
```
Retro amber monochrome terminal style like old CRT monitors.

### NEON NIGHTS
```
Primary:   #ff006e (Hot Pink)
Secondary: #8338ec (Purple)
Accent:    #3a86ff (Blue)
Background: #0a0014
```
Vibrant pink, purple, and blue neon colors.

### DEEP OCEAN
```
Primary:   #00b4d8 (Ocean Blue)
Secondary: #90e0ef (Light Blue)
Accent:    #caf0f8 (Very Light Blue)
Background: #001219
```
Calming blue and cyan ocean-inspired theme.

### Switching Themes
```
# In terminal:
theme matrix

# Or press T key
```

---

## 🔊 Sound Effects

### Generated Sounds
All sounds are procedurally generated using numpy (no external files needed):

| Sound | Description | Trigger |
|-------|-------------|---------|
| **Boot** | 3-second frequency sweep (200→800Hz) with harmonics | App startup |
| **Typing** | 50ms blip at 1500Hz | Keystroke in terminal |
| **Ambient** | 10-second low drone (55Hz) with modulation | Background loop |
| **Alert** | 5 alternating beeps (880/1100Hz) | Error/warning |
| **Success** | Major chord arpeggio (C5→E5→G5→C6) | Success action |
| **Hover** | Short 800Hz blip | UI hover (future) |

### Volume Levels
- Ambient: 30%
- Typing: 40%
- Hover: 20%
- Others: 100%

### Disabling Sound
```bash
# Method 1: Press S key
# Method 2: Type 'sound' in terminal
# Method 3: Edit config.json: "sound_enabled": false
```

---

## 📁 Project Structure

```
jokeratc/
│
├── main.py                  # Main application (54.5 KB)
│   ├── Dependency Check     # Auto-check required packages
│   ├── Sound Manager        # Procedural sound generation
│   ├── System Monitor       # CPU/RAM/Disk/Network monitoring
│   ├── Matrix Rain          # Animation engine
│   ├── Widgets              # UI components (7 widgets)
│   └── JokerATCApp          # Main Textual application
│
├── requirements.txt         # Python dependencies
├── README.md               # This documentation
├── config.json             # User configuration (auto-generated)
│
├── install.py              # Auto-installer script
├── start.sh                # Linux/macOS startup
├── start.bat               # Windows startup
│
├── sound_generator.py      # Standalone sound generator
├── utils.py                # Helper functions
├── screenshot_demo.py      # Demo visualization
│
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
│
├── themes/
│   └── default.json        # Custom theme template
│
└── sounds/
    └── generated/          # Generated WAV files (optional)
```

---

## ⚙️ Configuration

Configuration is automatically saved to `config.json`:

```json
{
  "theme": "tron",
  "sound_enabled": true,
  "matrix_enabled": true,
  "animation_speed": 1.0,
  "show_processes": true,
  "show_network": true,
  "show_file_explorer": true,
  "terminal_history_limit": 100,
  "auto_refresh_interval": 1.0,
  "matrix_update_interval": 0.15,
  "first_run": true
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `theme` | string | `"tron"` | Active theme name |
| `sound_enabled` | boolean | `true` | Enable/disable sound |
| `matrix_enabled` | boolean | `true` | Enable/disable matrix rain |
| `animation_speed` | float | `1.0` | Global animation speed multiplier |
| `show_processes` | boolean | `true` | Show process widget |
| `show_network` | boolean | `true` | Show network widget |
| `show_file_explorer` | boolean | `true` | Show file explorer |
| `terminal_history_limit` | int | `100` | Max terminal history lines |
| `auto_refresh_interval` | float | `1.0` | Widget refresh interval (seconds) |
| `matrix_update_interval` | float | `0.15` | Matrix animation speed |

---

## 📚 API Reference

### SystemMonitor Class
```python
from main import sys_monitor

# Get CPU info
cpu = sys_monitor.get_cpu_info()
# Returns: {"percent": 23.5, "cores": 8, "freq": "2400 MHz", "history": [...]}

# Get RAM info
ram = sys_monitor.get_ram_info()
# Returns: {"total": 17179869184, "used": 4509715660, ...}

# Get disk info
disks = sys_monitor.get_disk_info()
# Returns: [{"device": "/dev/sda1", "percent": 45, ...}]

# Get network info
net = sys_monitor.get_network_info()
# Returns: {"bytes_sent": ..., "speed_up": ..., "interfaces": [...]}

# Get temperature
temps = sys_monitor.get_temperature()
# Returns: {"coretemp": {"current": 42.0, "high": 80.0, ...}}

# Get processes
procs = sys_monitor.get_processes(limit=10, sort_by="cpu")
# Returns: [{"pid": 1234, "name": "python3", "cpu_percent": 12.5, ...}]
```

### SoundManager Class
```python
from main import sound_manager

# Play sounds
sound_manager.play("boot")       # Boot sequence
sound_manager.play("typing")     # Typing blip
sound_manager.play("ambient", loops=-1)  # Loop ambient
sound_manager.play("alert")      # Warning
sound_manager.play("success")    # Success chime

# Stop sounds
sound_manager.stop("ambient")    # Stop specific
sound_manager.stop()             # Stop all

# Toggle
is_enabled = sound_manager.toggle()
```

### MatrixRain Class
```python
from main import MatrixRain

# Create custom matrix rain
matrix = MatrixRain(width=80, height=24)

# Update animation
matrix.update()

# Get rendered text
output = matrix.render()
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Sound not working?
```bash
# Install pygame
pip install pygame

# Or disable sound in config.json
# Set "sound_enabled": false

# Check audio system
python -c "import pygame; pygame.mixer.init(); print('OK')"
```

#### 2. Permission errors?
```bash
# Run with sudo for full system access
sudo python main.py

# Or grant permissions to user
sudo usermod -aG adm,systemd-journal $USER
```

#### 3. Display issues / garbled text?
```bash
# Ensure UTF-8 locale
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Use a modern terminal
# Recommended: Alacritty, Kitty, iTerm2, Windows Terminal, GNOME Terminal
```

#### 4. Import errors?
```bash
# Reinstall dependencies
pip install --upgrade textual rich psutil pygame

# Or run the installer
python install.py
```

#### 5. Slow performance?
```bash
# Reduce animation speed in config.json
# "matrix_update_interval": 0.3
# "auto_refresh_interval": 2.0

# Or disable matrix rain
# Press M key or set "matrix_enabled": false
```

#### 6. Windows-specific issues?
```bash
# Install windows-curses for better terminal support
pip install windows-curses

# Use Windows Terminal (not cmd.exe)
# Install from Microsoft Store
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing`)
5. **Open** a Pull Request

### Ideas for Contributions
- [ ] New themes (Solarized, Dracula, Nord, etc.)
- [ ] Custom widget layouts
- [ ] Plugin system
- [ ] SSH connection manager
- [ ] Docker container monitor
- [ ] Git repository viewer
- [ ] Weather widget
- [ ] Calendar/schedule widget

---

## 📝 License

```
MIT License

Copyright (c) 2026 JokerATC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Credits & Acknowledgments

- **Inspired by** [eDEX-UI](https://github.com/GitSquared/edex-ui) by GitSquared
- **Built with** [Textual](https://github.com/Textualize/textual) - Modern Python TUI framework
- **Powered by** [Rich](https://github.com/Textualize/rich) - Rich text and beautiful formatting
- **System monitoring** by [psutil](https://github.com/giampaolo/psutil)
- **Sound effects** powered by [pygame](https://www.pygame.org/)

---

## 🔗 Links & Resources

- **GitHub**: https://github.com/yourusername/jokeratc
- **Issues**: https://github.com/yourusername/jokeratc/issues
- **Wiki**: https://github.com/yourusername/jokeratc/wiki
- **Releases**: https://github.com/yourusername/jokeratc/releases

---

## 💬 Support

Having issues? We're here to help!

- 📧 **Email**: support@jokeratc.dev
- 💬 **Discord**: [Join our server](https://discord.gg/jokeratc)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/jokeratc/issues)

---

## 🎯 Roadmap

### v2.1 (Planned)
- [ ] Custom widget layouts (drag & drop)
- [ ] Plugin system
- [ ] Weather widget
- [ ] Music player widget
- [ ] Custom ASCII art upload

### v3.0 (Future)
- [ ] Web-based remote access
- [ ] Mobile companion app
- [ ] AI assistant integration
- [ ] Voice commands
- [ ] VR/AR interface

---

> **"The future is already here — it's just not evenly distributed."**
> — William Gibson

---

Made with ❤️ by the JokerATC Team

⭐ Star us on GitHub if you like this project!
'''

with open('/mnt/agents/output/jokeratc/README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

readme_size = len(readme)
print(f"✅ README.md updated! ({readme_size:,} characters)")

# Also update the zip file
import zipfile
import os

zip_path = '/mnt/agents/output/jokeratc_v2.0_complete.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('/mnt/agents/output/jokeratc'):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, '/mnt/agents/output')
            zipf.write(file_path, arcname)

zip_size = os.path.getsize(zip_path)
print(f"✅ ZIP file updated! ({zip_size:,} bytes)")

print("\n" + "="*70)
print("📄 README.md CONTENT PREVIEW (First 80 lines):")
print("="*70)
lines = readme.split('\n')
for i, line in enumerate(lines[:80], 1):
    print(f"{i:>3} | {line}")
print("...")
print(f"\n📄 Total lines in README: {len(lines)}")
