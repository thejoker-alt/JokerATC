#!/bin/bash
# JokerATC - Auto Installer
# Works on Kali Linux, Parrot OS, Ubuntu/Debian

echo ""
echo "  🃏 JokerATC Installer"
echo "  ─────────────────────"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Install it first: sudo apt install python3"
    exit 1
fi

echo "[*] Installing system dependencies..."
sudo apt-get install -y portaudio19-dev lm-sensors python3-pip 2>/dev/null

echo "[*] Installing Python packages..."
pip3 install -r requirements.txt

echo ""
echo "[✓] Installation complete!"
echo "[*] Run with: python3 jokeratc.py"
echo "[*] Tip: For CPU temp, run: sudo sensors-detect"
echo ""
