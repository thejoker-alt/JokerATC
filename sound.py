# ═══════════════════════════════════════════════════════════════════════════════
# FILE 11: sound_generator.py (Standalone sound generator utility)
# ═══════════════════════════════════════════════════════════════════════════════

sound_generator = '''#!/usr/bin/env python3
"""
JokerATC Sound Generator
========================
Generate sci-fi sound effects for JokerATC.
Can be used standalone or imported.

Usage:
    python sound_generator.py          # Generate all sounds
    python sound_generator.py --play   # Generate and play boot sound
"""

import sys
import os
import struct
import wave
import math
import random

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  numpy not available. Using fallback method.")

SAMPLE_RATE = 44100
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sounds", "generated")

def ensure_dir():
    """Create output directory if needed"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_wav(filename, data, sample_rate=SAMPLE_RATE):
    """Save audio data as WAV file"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Ensure data is in int16 range
    if NUMPY_AVAILABLE:
        if isinstance(data, np.ndarray):
            data = data.astype(np.int16)
        else:
            data = np.array(data, dtype=np.int16)
        data_bytes = data.tobytes()
    else:
        data = [max(-32768, min(32767, int(x))) for x in data]
        data_bytes = struct.pack('<' + 'h' * len(data), *data)
    
    with wave.open(filepath, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(data_bytes)
    
    print(f"✅ Saved: {filepath}")
    return filepath

def generate_boot_sound():
    """Generate futuristic boot sound"""
    duration = 3.0
    samples = int(SAMPLE_RATE * duration)
    
    if NUMPY_AVAILABLE:
        t = np.linspace(0, duration, samples)
        freq = np.linspace(200, 800, samples)
        wave = np.sin(2 * np.pi * freq * t) * 0.3
        wave += np.sin(2 * np.pi * freq * 2 * t) * 0.15
        envelope = np.ones_like(t)
        envelope[t > 1.5] = np.exp(-(t[t > 1.5] - 1.5) * 3)
        wave *= envelope
        data = (wave * 32767).astype(np.int16)
    else:
        data = []
        for i in range(samples):
            t = i / SAMPLE_RATE
            freq = 200 + (800 - 200) * (t / duration)
            sample = math.sin(2 * math.pi * freq * t) * 0.3
            if t > 1.5:
                sample *= math.exp(-(t - 1.5) * 3)
            data.append(int(sample * 32767))
    
    return save_wav("boot.wav", data)

def generate_typing_sound():
    """Generate typing blip sound"""
    duration = 0.05
    samples = int(SAMPLE_RATE * duration)
    freq = 1500
    
    if NUMPY_AVAILABLE:
        t = np.linspace(0, duration, samples)
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 80) * 0.5
        data = (wave * 32767).astype(np.int16)
    else:
        data = []
        for i in range(samples):
            t = i / SAMPLE_RATE
            sample = math.sin(2 * math.pi * freq * t) * math.exp(-t * 80) * 0.5
            data.append(int(sample * 32767))
    
    return save_wav("typing.wav", data)

def generate_ambient_sound():
    """Generate ambient drone sound"""
    duration = 10.0
    samples = int(SAMPLE_RATE * duration)
    
    if NUMPY_AVAILABLE:
        t = np.linspace(0, duration, samples)
        base = np.sin(2 * np.pi * 55 * t) * 0.08
        mod = np.sin(2 * np.pi * 0.3 * t) * 0.04
        noise = np.random.normal(0, 0.015, len(t))
        wave = base + mod + noise
        
        fade_in = np.minimum(t * 2, 1.0)
        fade_out = np.maximum(1.0 - (t - 8) * 0.5, 0.0)
        wave *= fade_in * np.where(t > 8, fade_out, 1.0)
        data = (wave * 32767).astype(np.int16)
    else:
        data = []
        for i in range(samples):
            t = i / SAMPLE_RATE
            sample = math.sin(2 * math.pi * 55 * t) * 0.08
            sample += math.sin(2 * math.pi * 0.3 * t) * 0.04
            sample += (random.random() - 0.5) * 0.03
            
            fade = min(t * 2, 1.0)
            if t > 8:
                fade *= max(1.0 - (t - 8) * 0.5, 0.0)
            sample *= fade
            data.append(int(sample * 32767))
    
    return save_wav("ambient.wav", data)

def generate_alert_sound():
    """Generate alert/warning sound"""
    duration = 1.0
    samples = int(SAMPLE_RATE * duration)
    
    if NUMPY_AVAILABLE:
        t = np.linspace(0, duration, samples)
        wave = np.zeros(samples)
        for i in range(5):
            start = i * 0.2
            end = start + 0.08
            freq = 880 if i % 2 == 0 else 1100
            mask = (t >= start) & (t < end)
            wave[mask] = np.sin(2 * np.pi * freq * t[mask]) * 0.3
        data = (wave * 32767).astype(np.int16)
    else:
        data = []
        for i in range(samples):
            t = i / SAMPLE_RATE
            sample = 0
            for j in range(5):
                start = j * 0.2
                end = start + 0.08
                if start <= t < end:
                    freq = 880 if j % 2 == 0 else 1100
                    sample = math.sin(2 * math.pi * freq * t) * 0.3
            data.append(int(sample * 32767))
    
    return save_wav("alert.wav", data)

def generate_success_sound():
    """Generate success chime sound"""
    duration = 0.6
    samples = int(SAMPLE_RATE * duration)
    notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
    
    if NUMPY_AVAILABLE:
        t = np.linspace(0, duration, samples)
        wave = np.zeros(samples)
        for i, freq in enumerate(notes):
            start = i * 0.12
            mask = t >= start
            note = np.sin(2 * np.pi * freq * t) * np.exp(-(t - start) * 5) * 0.2
            wave[mask] += note[mask]
        data = (wave * 32767).astype(np.int16)
    else:
        data = []
        for i in range(samples):
            t = i / SAMPLE_RATE
            sample = 0
            for j, freq in enumerate(notes):
                start = j * 0.12
                if t >= start:
                    sample += math.sin(2 * math.pi * freq * t) * math.exp(-(t - start) * 5) * 0.2
            data.append(int(sample * 32767))
    
    return save_wav("success.wav", data)

def generate_all():
    """Generate all sound effects"""
    print("🎵 JokerATC Sound Generator")
    print("=" * 40)
    ensure_dir()
    
    sounds = [
        ("Boot", generate_boot_sound),
        ("Typing", generate_typing_sound),
        ("Ambient", generate_ambient_sound),
        ("Alert", generate_alert_sound),
        ("Success", generate_success_sound),
    ]
    
    for name, generator in sounds:
        print(f"\\n🔊 Generating {name} sound...")
        try:
            generator()
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\\n" + "=" * 40)
    print("✅ All sounds generated successfully!")
    print(f"📁 Location: {OUTPUT_DIR}")

def play_sound(filepath):
    """Play a sound file"""
    try:
        import pygame
        pygame.mixer.init()
        sound = pygame.mixer.Sound(filepath)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        print(f"❌ Cannot play sound: {e}")

if __name__ == "__main__":
    if "--play" in sys.argv:
        generate_all()
        boot_path = os.path.join(OUTPUT_DIR, "boot.wav")
        if os.path.exists(boot_path):
            print("\\n▶️  Playing boot sound...")
            play_sound(boot_path)
    else:
        generate_all()
'''

with open('/mnt/agents/output/jokeratc/sound_generator.py', 'w') as f:
    f.write(sound_generator)

print("✅ sound_generator.py saved!")

# ═══════════════════════════════════════════════════════════════════════════════
# FILE 12: utils.py (Utility functions)
# ═══════════════════════════════════════════════════════════════════════════════

utils = '''#!/usr/bin/env python3
"""
JokerATC Utilities
==================
Helper functions and utilities for JokerATC.
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def get_system_info() -> Dict:
    """Get comprehensive system information"""
    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
        "node": platform.node(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
    }

def check_internet(host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> bool:
    """Check if internet connection is available"""
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def get_ip_address() -> str:
    """Get primary IP address"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def format_duration(seconds: int) -> str:
    """Format seconds to human readable duration"""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)

def run_command(cmd: str, timeout: int = 5) -> Tuple[int, str, str]:
    """Run a shell command safely"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def load_json(filepath: str) -> Optional[Dict]:
    """Load JSON file safely"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json(filepath: str, data: Dict):
    """Save data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def ensure_dir(path: str):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_terminal_size() -> Tuple[int, int]:
    """Get terminal size"""
    import shutil
    return shutil.get_terminal_size()

def is_running_in_container() -> bool:
    """Check if running in a container"""
    return (
        os.path.exists('/.dockerenv') or
        os.path.exists('/run/.containerenv') or
        'container' in open('/proc/1/cgroup', 'r').read()
    )

def get_cpu_model() -> str:
    """Get CPU model name"""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    return line.split(':')[1].strip()
    except:
        pass
    return platform.processor()

# Color utilities for terminal output
class Colors:
    """ANSI color codes"""
    BLACK = '\\033[30m'
    RED = '\\033[31m'
    GREEN = '\\033[32m'
    YELLOW = '\\033[33m'
    BLUE = '\\033[34m'
    MAGENTA = '\\033[35m'
    CYAN = '\\033[36m'
    WHITE = '\\033[37m'
    BRIGHT_BLACK = '\\033[90m'
    BRIGHT_RED = '\\033[91m'
    BRIGHT_GREEN = '\\033[92m'
    BRIGHT_YELLOW = '\\033[93m'
    BRIGHT_BLUE = '\\033[94m'
    BRIGHT_MAGENTA = '\\033[95m'
    BRIGHT_CYAN = '\\033[96m'
    BRIGHT_WHITE = '\\033[97m'
    BOLD = '\\033[1m'
    DIM = '\\033[2m'
    UNDERLINE = '\\033[4m'
    BLINK = '\\033[5m'
    REVERSE = '\\033[7m'
    HIDDEN = '\\033[8m'
    RESET = '\\033[0m'

def colorize(text: str, color: str) -> str:
    """Apply color to text"""
    color_map = {
        'red': Colors.RED,
        'green': Colors.GREEN,
        'yellow': Colors.YELLOW,
        'blue': Colors.BLUE,
        'magenta': Colors.MAGENTA,
        'cyan': Colors.CYAN,
        'white': Colors.WHITE,
        'bright_red': Colors.BRIGHT_RED,
        'bright_green': Colors.BRIGHT_GREEN,
        'bright_yellow': Colors.BRIGHT_YELLOW,
        'bright_blue': Colors.BRIGHT_BLUE,
        'bright_magenta': Colors.BRIGHT_MAGENTA,
        'bright_cyan': Colors.BRIGHT_CYAN,
        'bright_white': Colors.BRIGHT_WHITE,
    }
    return f"{color_map.get(color, '')}{text}{Colors.RESET}"

if __name__ == "__main__":
    print("JokerATC Utilities")
    print("=" * 40)
    print(f"System: {get_system_info()['platform']}")
    print(f"Internet: {'✅' if check_internet() else '❌'}")
    print(f"IP: {get_ip_address()}")
    print(f"Terminal: {get_terminal_size()}")
'''

with open('/mnt/agents/output/jokeratc/utils.py', 'w') as f:
    f.write(utils)

print("✅ utils.py saved!")

print("\n" + "="*60)
print("📦 ALL JOKERATC FILES COMPLETE!")
print("="*60)

# Final file listing
print("\n📁 Complete Project Structure:")
for root, dirs, files in os.walk('/mnt/agents/output/jokeratc'):
    level = root.replace('/mnt/agents/output/jokeratc', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in sorted(files):
        filepath = os.path.join(root, file)
        size = os.path.getsize(filepath)
        print(f'{subindent}{file} ({size:,} bytes)')

# Calculate total size
total_size = sum(
    os.path.getsize(os.path.join(dirpath, filename))
    for dirpath, dirnames, filenames in os.walk('/mnt/agents/output/jokeratc')
    for filename in filenames
)
print(f"\n📊 Total Project Size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
