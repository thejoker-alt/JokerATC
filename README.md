# 🃏 JokerATC

> **Hacker Terminal Dashboard for Kali Linux & Parrot OS**  
> A sci-fi inspired, matrix-style TUI (Terminal UI) tool with live system stats, file explorer, interactive terminal, and hacker animations.

```
       ██╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗ ████████╗ ██████╗
       ██║██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
       ██║██║   ██║█████╔╝ █████╗  ██████╔╝███████║   ██║   ██║     
  ██   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║     
  ╚█████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║██║  ██║   ██║   ╚██████╗
   ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝
                          [ A T C ]  v1.0  |  by rc8447327-jpg
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🖥️ **Interactive Terminal** | Run live bash commands inside the dashboard |
| 📁 **File Explorer** | Navigate folders/files like eDEX-UI style |
| 💾 **RAM Monitor** | Live usage bar + MB used |
| ⚡ **CPU Monitor** | Live CPU % with color alerts |
| 🌡️ **Temperature Monitor** | CPU heat tracking (requires lm-sensors) |
| 💿 **Disk Usage** | Disk space bar |
| 🕐 **Live Clock** | Time, Date, Day — always visible |
| 🌧️ **Matrix Rain** | Animated katakana/hex matrix animation |
| 🔊 **Sound Effects** | Boot sound, keypress beeps, alerts |
| 🎨 **Hacker Colors** | Green, Red, Blue, White on Black |

---

## 🚀 Installation

### Requirements
- Python 3.8+
- Kali Linux / Parrot OS / Any Linux distro
- Terminal with 256-color support (min size: 80x24)

### Step 1 — Clone the repo
```bash
git clone https://github.com/rc8447327-jpg/JokerATC.git
cd JokerATC
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

> **For sound support** — install portaudio first:
> ```bash
> sudo apt install portaudio19-dev
> ```

### Step 3 — For CPU temperature (optional)
```bash
sudo apt install lm-sensors
sudo sensors-detect
```

### Step 4 — Run
```bash
python3 jokeratc.py
```

---

## ⌨️ Controls

| Key | Action |
|---|---|
| `TAB` | Switch focus between Terminal ↔ Explorer |
| `↑ ↓` | Navigate file explorer |
| `Enter` | Open folder / Run command |
| `Backspace` | Delete input character |
| `M` | Toggle matrix animation |
| `Q` | Quit (only when terminal input is empty) |

---

## 🎨 Color Scheme

| Color | Usage |
|---|---|
| 🟢 Green | Primary text, CPU/RAM bars (normal) |
| 🔴 Red | Alerts, high usage warnings, header |
| 🔵 Blue | File explorer, disk stats |
| ⚪ White | Normal text, input |
| ⚫ Black | Background |
| 🔵 Cyan | Accents, timestamps |

---

## 📁 Project Structure

```
JokerATC/
├── jokeratc.py         # Main application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚠️ Ethical Use Disclaimer

> This tool is developed for **educational and ethical purposes only**.  
> JokerATC is a system monitoring dashboard and terminal interface.  
> The author is **not responsible** for any misuse of this software.  
> Use only on systems you own or have explicit permission to access.  
> Unauthorized access to computer systems is **illegal**.

---

## 👨‍💻 Author

**rc8447327-jpg**  
GitHub: [github.com/rc8447327-jpg](https://github.com/rc8447327-jpg)

---

## 📜 License

MIT License — Free to use, modify, and distribute with attribution.

---

*"The system is yours — monitor it like a hacker."* 🃏
