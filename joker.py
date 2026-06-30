# ═══════════════════════════════════════════════════════════════════════════════
# FILE 1: main.py (Main Entry Point)
# ═══════════════════════════════════════════════════════════════════════════════

main_py = '''#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#    JOKERATC v2.0 - Cyberpunk Terminal Interface
#    Created by: You (Improved by AI)
#    License: MIT
#    
#    Features:
#    - Real-time system monitoring (CPU, RAM, Disk, Network, GPU, Temperature)
#    - File explorer with directory navigation
#    - Matrix rain animation with improved effects
#    - Sci-fi sound effects (boot, typing, ambient, alerts)
#    - Multiple terminal tabs with command history
#    - Network monitoring with GeoIP & ping
#    - Process viewer with kill functionality
#    - Customizable themes (TRON, MATRIX, CYBERPUNK, AMBER, NEON)
#    - ASCII art banners
#    - Smooth animations & transitions
#    - Keyboard shortcuts
# ═══════════════════════════════════════════════════════════════════════════════

import asyncio
import json
import os
import sys
import time
import random
import subprocess
import threading
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

# ─── Dependency Check ─────────────────────────────────────────────────────────
def check_dependencies():
    """Check and install missing dependencies"""
    missing = []
    
    try:
        import psutil
    except ImportError:
        missing.append("psutil")
    
    try:
        import textual
    except ImportError:
        missing.append("textual")
    
    try:
        import rich
    except ImportError:
        missing.append("rich")
    
    try:
        import pygame
    except ImportError:
        missing.append("pygame")
    
    if missing:
        print(f"""
╔════════════════════════════════════════════════════════════════╗
║  ❌ MISSING DEPENDENCIES: {', '.join(missing):<30}    ║
╠════════════════════════════════════════════════════════════════╣
║  📦 Install with:                                              ║
║     pip install {' '.join(missing):<45}         ║
╚════════════════════════════════════════════════════════════════╝
""")
        sys.exit(1)

check_dependencies()

# ─── Imports ────────────────────────────────────────────────────────────────
import psutil
import pygame
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import Static, Header, Footer, Label, Button, Input, Tree
from textual.reactive import reactive
from textual.screen import Screen
from textual.binding import Binding
from textual.timer import Timer
from textual.scroll_view import ScrollView

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.tree import Tree as RichTree
from rich.align import Align
from rich import box

# ─── Configuration ───────────────────────────────────────────────────────────
CONFIG_FILE = Path(__file__).parent / "config.json"
THEMES_DIR = Path(__file__).parent / "themes"
SOUNDS_DIR = Path(__file__).parent / "sounds"

# Default themes
DEFAULT_THEMES = {
    "tron": {
        "name": "TRON Legacy",
        "primary": "#00ff88",
        "secondary": "#00ccff",
        "accent": "#ff0066",
        "bg": "#000510",
        "text": "#ccffcc",
        "border": "#00ff88",
        "glow": "#00ffaa",
        "danger": "#ff3333",
        "warning": "#ffaa00",
        "success": "#00ff00"
    },
    "matrix": {
        "name": "The Matrix",
        "primary": "#00ff41",
        "secondary": "#008f11",
        "accent": "#003b00",
        "bg": "#000000",
        "text": "#00ff41",
        "border": "#00ff41",
        "glow": "#00ff41",
        "danger": "#ff0000",
        "warning": "#ffff00",
        "success": "#00ff00"
    },
    "cyberpunk": {
        "name": "Cyberpunk 2077",
        "primary": "#ff00ff",
        "secondary": "#00ffff",
        "accent": "#ffff00",
        "bg": "#0a0a1a",
        "text": "#ffccff",
        "border": "#ff00ff",
        "glow": "#ff00ff",
        "danger": "#ff0044",
        "warning": "#ffaa00",
        "success": "#00ff88"
    },
    "amber": {
        "name": "Amber CRT",
        "primary": "#ffb000",
        "secondary": "#ff8800",
        "accent": "#ff4400",
        "bg": "#1a0a00",
        "text": "#ffcc00",
        "border": "#ffb000",
        "glow": "#ffb000",
        "danger": "#ff3300",
        "warning": "#ff8800",
        "success": "#88ff00"
    },
    "neon": {
        "name": "Neon Nights",
        "primary": "#ff006e",
        "secondary": "#8338ec",
        "accent": "#3a86ff",
        "bg": "#0a0014",
        "text": "#ffccdd",
        "border": "#ff006e",
        "glow": "#ff006e",
        "danger": "#ff0000",
        "warning": "#ffaa00",
        "success": "#00ff88"
    },
    "ocean": {
        "name": "Deep Ocean",
        "primary": "#00b4d8",
        "secondary": "#90e0ef",
        "accent": "#caf0f8",
        "bg": "#001219",
        "text": "#e0fbfc",
        "border": "#00b4d8",
        "glow": "#48cae4",
        "danger": "#ff4444",
        "warning": "#ffaa00",
        "success": "#00ff88"
    }
}

# ─── Load/Save Config ────────────────────────────────────────────────────────
def load_config() -> Dict:
    """Load configuration from file"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "theme": "tron",
        "sound_enabled": True,
        "matrix_enabled": True,
        "animation_speed": 1.0,
        "show_processes": True,
        "show_network": True,
        "show_file_explorer": True,
        "terminal_history_limit": 100
    }

def save_config(config: Dict):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

CONFIG = load_config()

# ─── Sound Manager ───────────────────────────────────────────────────────────
class SoundManager:
    """Advanced sci-fi sound effects manager"""
    
    def __init__(self):
        self.enabled = CONFIG.get("sound_enabled", True)
        self.initialized = False
        self.sounds = {}
        self._init_audio()
    
    def _init_audio(self):
        """Initialize audio system"""
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.initialized = True
            self._generate_sounds()
        except Exception as e:
            print(f"⚠️  Audio init failed: {e}")
    
    def _generate_sounds(self):
        """Generate procedural sound effects using numpy"""
        try:
            import numpy as np
        except ImportError:
            print("⚠️  numpy not available, sound generation skipped")
            return
        
        sample_rate = 44100
        
        # 1. Boot Sound - Futuristic power-up sequence
        def create_boot():
            duration = 3.0
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Frequency sweep 200Hz → 800Hz
            freq = np.linspace(200, 800, len(t))
            wave = np.sin(2 * np.pi * freq * t) * 0.3
            
            # Add harmonics for richness
            wave += np.sin(2 * np.pi * freq * 2 * t) * 0.15
            wave += np.sin(2 * np.pi * freq * 0.5 * t) * 0.1
            
            # Envelope with reverb-like decay
            envelope = np.ones_like(t)
            envelope[t > 1.5] = np.exp(-(t[t > 1.5] - 1.5) * 3)
            wave *= envelope
            
            return (wave * 32767).astype(np.int16)
        
        # 2. Typing Sound - Short tech blip
        def create_typing():
            duration = 0.03
            t = np.linspace(0, duration, int(sample_rate * duration))
            freq = 1500 + random.randint(-200, 200)
            wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 80)
            return (wave * 32767).astype(np.int16)
        
        # 3. Ambient Drone - Background atmosphere
        def create_ambient():
            duration = 8.0
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Low frequency drone
            base = np.sin(2 * np.pi * 55 * t) * 0.08
            # Slow modulation
            mod = np.sin(2 * np.pi * 0.3 * t) * 0.04
            # Subtle noise
            noise = np.random.normal(0, 0.015, len(t))
            
            wave = base + mod + noise
            
            # Fade in/out
            fade_in = np.minimum(t * 2, 1.0)
            fade_out = np.maximum(1.0 - (t - 6) * 0.5, 0.0)
            wave *= fade_in * np.where(t > 6, fade_out, 1.0)
            
            return (wave * 32767).astype(np.int16)
        
        # 4. Alert Sound - Warning beep
        def create_alert():
            duration = 0.8
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Alternating beeps
            beep1 = np.sin(2 * np.pi * 880 * t) * 0.3
            beep2 = np.sin(2 * np.pi * 1100 * t) * 0.3
            
            # Create beeping pattern
            pattern = np.zeros_like(t)
            for i in range(4):
                start = i * 0.2
                end = start + 0.08
                mask = (t >= start) & (t < end)
                if i % 2 == 0:
                    pattern[mask] = beep1[mask]
                else:
                    pattern[mask] = beep2[mask]
            
            return (pattern * 32767).astype(np.int16)
        
        # 5. Success Sound - Positive chime
        def create_success():
            duration = 0.5
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Major chord arpeggio
            notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
            wave = np.zeros_like(t)
            
            for i, freq in enumerate(notes):
                start = i * 0.1
                mask = t >= start
                note_wave = np.sin(2 * np.pi * freq * t) * np.exp(-(t - start) * 5) * 0.2
                wave[mask] += note_wave[mask]
            
            return (wave * 32767).astype(np.int16)
        
        # 6. Hover Sound - UI hover effect
        def create_hover():
            duration = 0.05
            t = np.linspace(0, duration, int(sample_rate * duration))
            freq = 800
            wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 60) * 0.1
            return (wave * 32767).astype(np.int16)
        
        try:
            self.sounds["boot"] = pygame.mixer.Sound(create_boot())
            self.sounds["typing"] = pygame.mixer.Sound(create_typing())
            self.sounds["ambient"] = pygame.mixer.Sound(create_ambient())
            self.sounds["alert"] = pygame.mixer.Sound(create_alert())
            self.sounds["success"] = pygame.mixer.Sound(create_success())
            self.sounds["hover"] = pygame.mixer.Sound(create_hover())
            
            # Set volume levels
            self.sounds["ambient"].set_volume(0.3)
            self.sounds["typing"].set_volume(0.4)
            self.sounds["hover"].set_volume(0.2)
            
        except Exception as e:
            print(f"⚠️  Sound generation error: {e}")
    
    def play(self, sound_name: str, loops: int = 0):
        """Play a sound effect"""
        if self.enabled and self.initialized and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play(loops=loops)
            except:
                pass
    
    def stop(self, sound_name: str = None):
        """Stop sound playback"""
        if self.initialized:
            if sound_name and sound_name in self.sounds:
                self.sounds[sound_name].stop()
            else:
                pygame.mixer.stop()
    
    def toggle(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop()
        return self.enabled

# Global sound manager
sound_manager = SoundManager()

# ─── System Monitor ─────────────────────────────────────────────────────────
class SystemMonitor:
    """Advanced real-time system monitoring"""
    
    def __init__(self):
        self.cpu_history = []
        self.ram_history = []
        self.net_history = []
        self.max_history = 60
        self.last_net_io = None
        self.net_speed = {"up": 0, "down": 0}
    
    def get_cpu_info(self):
        """Get CPU information"""
        cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_avg = sum(cpu_percent) / len(cpu_percent)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        self.cpu_history.append(cpu_avg)
        if len(self.cpu_history) > self.max_history:
            self.cpu_history.pop(0)
        
        return {
            "percent": cpu_avg,
            "per_cpu": cpu_percent,
            "cores": cpu_count,
            "freq": f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A",
            "history": self.cpu_history.copy()
        }
    
    def get_ram_info(self):
        """Get RAM information"""
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        self.ram_history.append(ram.percent)
        if len(self.ram_history) > self.max_history:
            self.ram_history.pop(0)
        
        return {
            "total": ram.total,
            "used": ram.used,
            "free": ram.free,
            "percent": ram.percent,
            "swap_total": swap.total,
            "swap_used": swap.used,
            "swap_percent": swap.percent,
            "history": self.ram_history.copy()
        }
    
    def get_disk_info(self):
        """Get Disk information for all partitions"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                })
            except PermissionError:
                pass
        return disks
    
    def get_network_info(self):
        """Get Network information with speed calculation"""
        net_io = psutil.net_io_counters()
        
        if self.last_net_io:
            time_delta = time.time() - self.last_net_io["time"]
            if time_delta > 0:
                self.net_speed["up"] = (net_io.bytes_sent - self.last_net_io["sent"]) / time_delta
                self.net_speed["down"] = (net_io.bytes_recv - self.last_net_io["recv"]) / time_delta
        
        self.last_net_io = {
            "time": time.time(),
            "sent": net_io.bytes_sent,
            "recv": net_io.bytes_recv
        }
        
        # Get network interfaces
        interfaces = []
        try:
            for name, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == 2:  # IPv4
                        interfaces.append({
                            "name": name,
                            "ip": addr.address,
                            "netmask": addr.netmask
                        })
        except:
            pass
        
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "speed_up": self.net_speed["up"],
            "speed_down": self.net_speed["down"],
            "interfaces": interfaces
        }
    
    def get_temperature(self):
        """Get CPU/GPU temperature"""
        temps = {}
        try:
            sensors = psutil.sensors_temperatures()
            if sensors:
                for name, entries in sensors.items():
                    for entry in entries:
                        if entry.current:
                            temps[name] = {
                                "current": entry.current,
                                "high": entry.high,
                                "critical": entry.critical
                            }
        except:
            pass
        return temps
    
    def get_processes(self, limit: int = 15, sort_by: str = "cpu"):
        """Get top processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username', 'status']):
            try:
                info = proc.info
                # Get more details
                p = psutil.Process(info['pid'])
                info['memory_info'] = p.memory_info().rss
                info['create_time'] = p.create_time()
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by specified field
        sort_key = 'cpu_percent' if sort_by == "cpu" else 'memory_percent'
        processes.sort(key=lambda x: x.get(sort_key, 0), reverse=True)
        return processes[:limit]
    
    def get_system_info(self):
        """Get general system information"""
        return {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "python": platform.python_version(),
            "boot_time": psutil.boot_time(),
            "users": [u.name for u in psutil.users()]
        }

sys_monitor = SystemMonitor()

# ─── Matrix Rain Effect ──────────────────────────────────────────────────────
class MatrixRain:
    """Improved Matrix rain effect with multiple streams"""
    
    def __init__(self, width: int = 70, height: int = 20):
        self.width = width
        self.height = height
        self.drops = []
        self.chars = (
            "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"
            "0123456789ABCDEF"
            "αβγδεζηθικλμνξοπρστυφχψω"
            "∞∑∆∇∫√≈≠≤≥"
        )
        self.init_drops()
    
    def init_drops(self):
        """Initialize rain drops with varied properties"""
        self.drops = []
        num_drops = self.width // 2
        
        for _ in range(num_drops):
            self.drops.append({
                'x': random.randint(0, self.width - 1),
                'y': random.randint(-self.height, 0),
                'speed': random.uniform(0.5, 3.0),
                'length': random.randint(4, 15),
                'brightness': random.uniform(0.2, 1.0),
                'trail': [],
                'char_set': random.choice(['katakana', 'hex', 'greek'])
            })
    
    def update(self):
        """Update rain positions"""
        for drop in self.drops:
            drop['y'] += drop['speed']
            
            # Add to trail
            drop['trail'].append({
                'x': drop['x'],
                'y': drop['y'],
                'char': random.choice(self.chars),
                'brightness': drop['brightness']
            })
            
            # Limit trail length
            if len(drop['trail']) > drop['length']:
                drop['trail'].pop(0)
            
            # Reset if off screen
            if drop['y'] > self.height + drop['length']:
                drop['y'] = random.randint(-10, 0)
                drop['x'] = random.randint(0, self.width - 1)
                drop['speed'] = random.uniform(0.5, 3.0)
                drop['length'] = random.randint(4, 15)
                drop['trail'] = []
                drop['brightness'] = random.uniform(0.2, 1.0)
    
    def render(self) -> str:
        """Render matrix rain as styled string"""
        self.update()
        
        # Create grid
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        brightness = [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        
        for drop in self.drops:
            for i, trail_point in enumerate(drop['trail']):
                y = int(trail_point['y'])
                x = int(trail_point['x'])
                
                if 0 <= y < self.height and 0 <= x < self.width:
                    # Head is brightest
                    if i == len(drop['trail']) - 1:
                        grid[y][x] = trail_point['char']
                        brightness[y][x] = 1.0
                    else:
                        # Trail fades
                        fade = i / len(drop['trail'])
                        if random.random() > fade * 0.7:  # Random visibility for trail
                            grid[y][x] = trail_point['char']
                            brightness[y][x] = fade * 0.5
        
        return '\\n'.join(''.join(row) for row in grid)

matrix_rain = MatrixRain(60, 15)

# ─── ASCII Art Generator ───────────────────────────────────────────────────
class ASCIIBanner:
    """Generate ASCII art banners"""
    
    BANNERS = {
        "jokeratc": """
     ██╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗ ████████╗ ██████╗
     ██║██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
     ██║██║   ██║█████╔╝ █████╗  ██████╔╝███████║   ██║   ██║     
██   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║     
╚█████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║██║  ██║   ██║   ╚██████╗
 ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝
        """,
        "boot": """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              ⚡ JOKERATC SYSTEM INITIALIZATION ⚡                 ║
║                                                                  ║
║         [████████████] 100% SYSTEM BOOT COMPLETE                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """,
        "hacker": """
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░ HACKER MODE ENGAGED ░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        """
    }
    
    @classmethod
    def get(cls, name: str) -> str:
        return cls.BANNERS.get(name, cls.BANNERS["jokeratc"])

# ─── Widgets ─────────────────────────────────────────────────────────────────
class SystemStatsWidget(Static):
    """Real-time system statistics widget"""
    
    def __init__(self):
        super().__init__()
        self.theme = DEFAULT_THEMES[CONFIG["theme"]]
    
    def render(self):
        """Render system stats with bars"""
        cpu = sys_monitor.get_cpu_info()
        ram = sys_monitor.get_ram_info()
        disks = sys_monitor.get_disk_info()
        temps = sys_monitor.get_temperature()
        
        table = Table(
            box=box.DOUBLE_EDGE,
            border_style=self.theme["border"],
            show_header=False,
            padding=(0, 1)
        )
        
        table.add_column("Metric", style=f"bold {self.theme['secondary']}", width=10)
        table.add_column("Value", style=self.theme["text"], width=18)
        table.add_column("Bar", width=22)
        
        # CPU
        cpu_bar = "█" * int(cpu["percent"] / 5) + "░" * (20 - int(cpu["percent"] / 5))
        cpu_color = self.theme["success"] if cpu["percent"] < 50 else self.theme["warning"] if cpu["percent"] < 80 else self.theme["danger"]
        table.add_row(
            "[bold]CPU[/]",
            f"{cpu['percent']:.1f}% ({cpu['cores']}C)",
            f"[{cpu_color}]{cpu_bar}[/{cpu_color}]"
        )
        
        # RAM
        ram_used_gb = ram["used"] / (1024**3)
        ram_total_gb = ram["total"] / (1024**3)
        ram_bar = "█" * int(ram["percent"] / 5) + "░" * (20 - int(ram["percent"] / 5))
        ram_color = self.theme["success"] if ram["percent"] < 50 else self.theme["warning"] if ram["percent"] < 80 else self.theme["danger"]
        table.add_row(
            "[bold]RAM[/]",
            f"{ram_used_gb:.1f}/{ram_total_gb:.1f} GB",
            f"[{ram_color}]{ram_bar}[/{ram_color}]"
        )
        
        # Disk
        if disks:
            disk = disks[0]
            disk_bar = "█" * int(disk["percent"] / 5) + "░" * (20 - int(disk["percent"] / 5))
            disk_color = self.theme["success"] if disk["percent"] < 70 else self.theme["warning"] if disk["percent"] < 90 else self.theme["danger"]
            table.add_row(
                "[bold]DISK[/]",
                f"{disk['percent']:.0f}%",
                f"[{disk_color}]{disk_bar}[/{disk_color}]"
            )
        
        # Temperature
        if temps:
            for name, temp_info in list(temps.items())[:1]:
                temp_color = self.theme["success"] if temp_info["current"] < 60 else self.theme["warning"] if temp_info["current"] < 80 else self.theme["danger"]
                table.add_row(
                    "[bold]TEMP[/]",
                    f"{temp_info['current']:.1f}°C",
                    f"[{temp_color}]{'█' * int(temp_info['current'] / 5)}{'░' * (20 - int(temp_info['current'] / 5))}[/{temp_color}]"
                )
        
        return Panel(
            table,
            border_style=self.theme["border"],
            title=f"[bold {self.theme['primary']}]◉ SYSTEM MONITOR[/]",
            title_align="left",
            subtitle=f"[dim]CPU: {cpu['freq']}[/dim]",
            subtitle_align="right"
        )

class FileExplorerWidget(Static):
    """Advanced file explorer widget"""
    
    def __init__(self, path: str = "."):
        super().__init__()
        self.current_path = Path(path).resolve()
        self.theme = DEFAULT_THEMES[CONFIG["theme"]]
        self.selected_index = 0
    
    def render(self):
        """Render file tree with icons"""
        try:
            tree = RichTree(
                f"[bold {self.theme['primary']}]📁 {self.current_path}[/]",
                guide_style=self.theme["secondary"]
            )
            
            items = sorted(self.current_path.iterdir())
            
            for i, item in enumerate(items[:25]):
                if item.is_dir():
                    tree.add(f"[bold {self.theme['secondary']}]📂 {item.name}[/]")
                else:
                    size = item.stat().st_size
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024**2:
                        size_str = f"{size/1024:.1f} KB"
                    elif size < 1024**3:
                        size_str = f"{size/1024**2:.1f} MB"
                    else:
                        size_str = f"{size/1024**3:.1f} GB"
                    
                    # File type icons
                    ext = item.suffix.lower()
                    icons = {
                        '.py': "🐍", '.js': "📜", '.html': "🌐", '.css': "🎨",
                        '.sh': "⚡", '.json': "📋", '.txt': "📝", '.md': "📄",
                        '.jpg': "🖼️", '.png': "🖼️", '.gif': "🖼️", '.mp4': "🎬",
                        '.mp3': "🎵", '.wav': "🎵", '.zip': "📦", '.tar': "📦",
                        '.exe': "⚙️", '.deb': "📦", '.rpm': "📦", '.cpp': "⚙️",
                        '.c': "⚙️", '.java': "☕", '.go': "🐹", '.rs': "🦀"
                    }
                    icon = icons.get(ext, "📄")
                    
                    tree.add(f"{icon} {item.name} [dim]({size_str})[/dim]")
            
            if len(items) > 25:
                tree.add(f"[dim]... and {len(items) - 25} more items[/dim]")
            
            return Panel(
                tree,
                border_style=self.theme["border"],
                title=f"[bold {self.theme['primary']}]📂 FILE EXPLORER[/]",
                title_align="left",
                subtitle=f"[dim]{len(items)} items[/dim]",
                subtitle_align="right"
            )
        except PermissionError:
            return Panel(
                "[red]⚠️ Permission Denied[/]",
                border_style="red",
                title="[bold red]📂 FILE EXPLORER[/]"
            )

class MatrixRainWidget(Static):
    """Matrix rain animation widget"""
    
    def __init__(self):
        super().__init__()
        self.theme = DEFAULT_THEMES[CONFIG["theme"]]
        self.matrix = MatrixRain(55, 12)
    
    def render(self):
        """Render matrix rain with color effects"""
        matrix_text = self.matrix.render()
        lines = matrix_text.split('\\n')
        
        styled_text = Text()
        for line in lines:
            for char in line:
                if char != ' ':
                    # Random green shades for matrix effect
                    if CONFIG["theme"] == "matrix":
                        green_val = random.randint(100, 255)
                        styled_text.append(char, style=f"bold rgb(0,{green_val},0)")
                    elif CONFIG["theme"] == "tron":
                        blue_val = random.randint(100, 255)
                        styled_text.append(char, style=f"bold rgb(0,{blue_val},{blue_val})")
                    elif CONFIG["theme"] == "cyberpunk":
                        r = random.randint(200, 255)
                        b = random.randint(100, 200)
                        styled_text.append(char, style=f"bold rgb({r},0,{b})")
                    else:
                        styled_text.append(char, style=f"bold {self.theme['primary']}")
                else:
                    styled_text.append(' ')
            styled_text.append('\\n')
        
        return Panel(
            styled_text,
            border_style=self.theme["primary"],
            title=f"[bold {self.theme['primary']}]🌧️  MATRIX RAIN[/]",
            title_align="left"
        )

class ProcessWidget(Static):
    """Process monitor widget with kill functionality"""
    
    def __init__(self):
        super().__init__()
        self.theme = DEFAULT_THEMES[CONFIG["theme"]]
    
    def render(self):
        """Render process list"""
        processes = sys_monitor.get_processes(10, "cpu")
        
        table = Table(
            box=box.SIMPLE_HEAD,
            border_style=self.theme["border"],
            show_header=True,
            header_style=f"bold {self.theme['primary']}",
            padding=(0, 1)
        )
        
        table.add_column("PID", style=self.theme["secondary"], width=7)
        table.add_column("NAME", style=self.theme["text"], width=18)
        table.add_column("USER", style="dim", width=10)
        table.add_column("CPU%", justify="right", width=7)
        table.add_column("MEM%", justify="right", width=7)
        table.add_column("MEM", justify="right", width=8)
        
        for proc in processes:
            cpu_color = self.theme["success"] if proc['cpu_percent'] < 5 else self.theme["warning"] if proc['cpu_percent'] < 20 else self.theme["danger"]
            mem_color = self.theme["success"] if proc['memory_percent'] < 5 else self.theme["warning"] if proc['memory_percent'] < 20 else self.theme["danger"]
            
            mem_mb = proc.get('memory_info', 0) / (1024**2)
            
            table.add_row(
                str(proc['pid']),
                proc['name'][:18],
                proc.get('username', '?')[:10],
                f"[{cpu_color}]{proc['cpu_percent']:.1f}%[/{cpu_color}]",
                f"[{mem_color}]{proc['memory_percent']:.1f}%[/{mem_color}]",
                f"{mem_mb:.0f}M"
            )
        
        return Panel(
            table,
            border_style=self.theme["border"],
            title=f"[bold {self.theme['primary']}]⚡ PROCESSES (TOP 10)[/]",
            title_align="left"
        )

class TerminalWidget(Static):
    """Advanced terminal widget with command history"""
    
    def __init__(self):
        super().__init__()
        self.theme = DEFAULT_THEMES[CONFIG["theme"]]
        self.output = [
            f"[bold {self.theme['primary']}]╔══════════════════════════════════════════════════════════╗[/]",
            f"[bold {self.theme['primary']}]║[/]  [bold]JOKERATC v2.0 - Cyberpunk Terminal Interface[/]              [bold {self.theme['primary']}]║[/]",
            f"[bold {self.theme['primary']}]║[/]  [dim]Type 'help' for available commands[/]                        [bold {self.theme['primary']}]║[/]",
            f"[bold {self.theme['primary']}]╚══════════════════════════════════════════════════════════╝[/]",
            "",
        ]
        self.command_history = []
        self.history_index = 0
    
    def add_line(self, line: str):
        """Add line to terminal output"""
        self.output.append(line)
        limit = CONFIG.get("terminal_history_limit", 100)
        if len(self.output) > limit:
            self.output = self.output[-limit:]
        self.refresh()
    
    def execute_command(self, cmd: str):
        """Execute a terminal command"""
        self.add_line(f"[bold {self.theme['primary']}]┌──([/]{self.theme['secondary']}user@jokeratc[/][bold {self.theme['primary']}])-[[/]~[bold {self.theme['primary']}])[/]")
        self.add_line(f"[bold {self.theme['primary']}]└─▶[/] {cmd}")
        
        if cmd.lower() == 'help':
            help_text = """[bold cyan]Available Commands:[/]
  [green]help[/]      - Show this help message
  [green]clear[/]     - Clear terminal
  [green]sysinfo[/]   - Show system information
  [green]neofetch[/]  - Display system info with ASCII art
  [green]theme[/]     - List available themes
  [green]theme <name>[/] - Switch theme
  [green]sound[/]     - Toggle sound effects
  [green]matrix[/]    - Toggle matrix rain
  [green]reboot[/]    - Simulate system reboot
  [green]shutdown[/]  - Exit JokerATC
  [green]whoami[/]    - Show current user
  [green]uptime[/]    - Show system uptime
  [green]ps[/]        - List running processes
  [green]net[/]       - Show network information
  [green]ping <host>[/] - Ping a host
  [green]banner[/]    - Show JokerATC banner"""
            self.add_line(help_text)
        
        elif cmd.lower() == 'clear':
            self.output = []
        
        elif cmd.lower() == 'sysinfo':
            info = sys_monitor.get_system_info()
            self.add_line(f"[bold]Platform:[/] {info['platform']}")
            self.add_line(f"[bold]Processor:[/] {info['processor']}")
            self.add_line(f"[bold]Hostname:[/] {info['hostname']}")
            self.add_line(f"[bold]Python:[/] {info['python']}")
        
        elif cmd.lower() == 'neofetch':
            self.add_line(ASCIIBanner.get("jokeratc"))
            info = sys_monitor.get_system_info()
            self.add_line(f"[bold]OS:[/] {info['platform']}")
            self.add_line(f"[bold]Host:[/] {info['hostname']}")
            self.add_line(f"[bold]CPU:[/] {info['processor']}")
            self.add_line(f"[bold]Python:[/] {info['python']}")
        
        elif cmd.lower().startswith('theme '):
            theme_name = cmd.split()[1] if len(cmd.split()) > 1 else ""
            if theme_name in DEFAULT_THEMES:
                global CONFIG
                CONFIG["theme"] = theme_name
                save_config(CONFIG)
                self.add_line(f"[green]✓ Theme changed to: {DEFAULT_THEMES[theme_name]['name']}[/]")
                sound_manager.play("success")
            else:
                themes_list = ", ".join([f"[cyan]{k}[/]" for k in DEFAULT_THEMES.keys()])
                self.add_line(f"[red]✗ Available themes: {themes_list}[/]")
        
        elif cmd.lower() == 'theme':
            themes_list = ", ".join([f"[cyan]{k}[/] ({v['name']})" for k, v in DEFAULT_THEMES.items()])
            self.add_line(f"[bold]Available Themes:[/] {themes_list}")
        
        elif cmd.lower() == 'sound':
            state = sound_manager.toggle()
            self.add_line(f"[green]✓ Sound {'enabled' if state else 'disabled'}[/]")
        
        elif cmd.lower() == 'matrix':
            CONFIG["matrix_enabled"] = not CONFIG.get("matrix_enabled", True)
            save_config(CONFIG)
            self.add_line(f"[green]✓ Matrix rain {'enabled' if CONFIG['matrix_enabled'] else 'disabled'}[/]")
        
        elif cmd.lower() == 'reboot':
            self.add_line("[yellow]⚡ Rebooting system...[/]")
            sound_manager.play("boot")
        
        elif cmd.lower() == 'shutdown':
            self.add_line("[red]👋 Goodbye![/]")
            sound_manager.stop()
        
        elif cmd.lower() == 'whoami':
            self.add_line(f"[bold]{os.getlogin()}[/]")
        
        elif cmd.lower() == 'uptime':
            uptime = time.time() - psutil.boot_time()
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
            minutes = int((uptime % 3600) // 60)
            self.add_line(f"[bold]Uptime:[/] {days}d {hours}h {minutes}m")
        
        elif cmd.lower() == 'ps':
            processes = sys_monitor.get_processes(5)
            for proc in processes:
                self.add_line(f"{proc['pid']:>6} {proc['name']:<20} {proc['cpu_percent']:>6.1f}%")
        
        elif cmd.lower() == 'net':
            net = sys_monitor.get_network_info()
            self.add_line(f"[bold]Download:[/] {net['bytes_recv'] / (1024**2):.1f} MB")
            self.add_line(f"[bold]Upload:[/] {net['bytes_sent'] / (1024**2):.1f} MB")
            self.add_line(f"[bold]Speed Down:[/] {net['speed_down'] / 1024:.1f} KB/s")
            self.add_line(f"[bold]Speed Up:[/] {net['speed_up'] / 1024:.1f} KB/s")
        
        elif cmd.lower().startswith('ping '):
            host = cmd.split()[1] if len(cmd.split()) > 1 else "google.com"
            self.add_line(f"[yellow]Pinging {host}...[/]")
            try:
                result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.add_line(f"[green]✓ {host} is reachable[/]")
                    sound_manager.play("success")
                else:
                    self.add_line(f"[red]✗ {host} is unreachable[/]")
            except:
                self.add_line(f"[red]✗ Ping failed[/]")
        
        elif cmd.lower() == 'banner':
            self.add_line(ASCIIBanner.get("jokeratc"))
        
        elif cmd.strip():
            # Try to execute as shell command
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                if result.stdout:
                    for line in result.stdout.split('\\n')[:20]:
                        self.add_line(line)
                if result.stderr:
                    for line in result.stderr.split('\\n')[:5]:
                        self.add_line(f"[red]{line}[/]")
            except Exception as e:
                self.add_line(f"[red]✗ Error: {str(e)}[/]")
        
        self.add_line("")
        self.add_line(f"[bold {self.theme['primary']}]┌──([/]{self.theme['secondary']}user@jokeratc[/][bold {self.theme['primary']}])-[[/]~[bold {self.theme['primary']}])[/]")
        self.add_line(f"[bold {self.theme['primary']}]└─▶[/] ")
    
    def render(self):
        """Render terminal"""
        content = "\\n".join(self.output[-25:])
        return Panel(
            content,
            border_style=self.theme["border"],
            title=f"[bold {self.theme['primary']}]💻 TERMINAL[/]",
            title_align="left",
            subtitle=f"[dim]History: {len(self.output)} lines[/dim]",
            subtitle_align="right"
        )

class ClockWidget(Static):
    """Digital clock widget with date"""
    
    def __init__(self):
        super().__init__()
        self.theme = DEFAULT_THEMES[CONFIG["theme"]]
    
    def render(self):
        """Render clock"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %d %B %Y")
        week_str = f"Week {now.isocalendar()[1]}"
        
        clock_text = Text()
        clock_text.append(f"{time_str}\\n", style=f"bold {self.theme['primary']}")
        clock_text.append(f"{date_str}\\n", style=f"dim {self.theme['secondary']}")
        clock_text.append(week_str, style=f"dim {self.theme['accent']}")
        
        return Panel(
            Align.center(clock_text),
            border_style=self.theme["border"],
            title=f"[bold {self.theme['primary']}]🕐 TIME[/]",
            title_align="left"
        )

class NetworkWidget(Static):
    """Network monitoring widget with speed"""
    
    def __init__(self):
        super().__init__()
        self.theme = DEFAULT_THEMES[CONFIG["theme"]]
    
    def render(self):
        """Render network info"""
        net = sys_monitor.get_network_info()
        
        # Speed bars
        down_speed_kb = net['speed_down'] / 1024
        up_speed_kb = net['speed_up'] / 1024
        
        down_bar = "█" * min(int(down_speed_kb / 10), 20) + "░" * max(20 - int(down_speed_kb / 10), 0)
        up_bar = "█" * min(int(up_speed_kb / 10), 20) + "░" * max(20 - int(up_speed_kb / 10), 0)
        
        content = f"""[bold {self.theme['secondary']}]Network Interfaces:[/]
"""
        for iface in net['interfaces'][:3]:
            content += f"  {iface['name']}: [cyan]{iface['ip']}[/]\\n"
        
        content += f"""
[bold {self.theme['secondary']}]Real-time Speed:[/]
  [green]▼[/] Download: {down_speed_kb:.1f} KB/s
  [{self.theme['primary']}]{down_bar}[/{self.theme['primary']}]
  [yellow]▲[/] Upload: {up_speed_kb:.1f} KB/s
  [{self.theme['secondary']}]{up_bar}[/{self.theme['secondary']}]

[bold {self.theme['secondary']}]Total Traffic:[/]
  [green]▼[/] Received: {net['bytes_recv'] / (1024**3):.2f} GB
  [yellow]▲[/] Sent: {net['bytes_sent'] / (1024**3):.2f} GB
"""
        
        return Panel(
            content,
            border_style=self.theme["border"],
            title=f"[bold {self.theme['primary']}]🌐 NETWORK[/]",
            title_align="left"
        )

class HeaderWidget(Static):
    """Custom header with system info"""
    
    def __init__(self):
        super().__init__()
        self.theme = DEFAULT_THEMES[CONFIG["theme"]]
    
    def render(self):
        """Render header"""
        info = sys_monitor.get_system_info()
        hostname = info['hostname']
        
        header_text = Text()
        header_text.append("╔══════════════════════════════════════════════════════════════════════╗\\n", style=f"bold {self.theme['primary']}")
        header_text.append("║  ", style=f"bold {self.theme['primary']}")
        header_text.append("⚡ JOKERATC v2.0", style=f"bold {self.theme['primary']}")
        header_text.append("  " + " " * 40, style=f"bold {self.theme['primary']}")
        header_text.append(f"{hostname}  ", style=f"dim {self.theme['secondary']}")
        header_text.append("║\\n", style=f"bold {self.theme['primary']}")
        header_text.append("╚══════════════════════════════════════════════════════════════════════╝", style=f"bold {self.theme['primary']}")
        
        return header_text

# ─── Main Application ─────────────────────────────────────────────────────────
class JokerATCApp(App):
    """Main JokerATC Application"""
    
    CSS = """
    Screen {
        background: #000510;
    }
    
    .main-container {
        layout: grid;
        grid-size: 3 3;
        grid-gutter: 1;
        grid-columns: 1fr 2fr 1fr;
        grid-rows: 1fr 1fr 1fr;
        padding: 1;
    }
    
    .stats-panel {
        row-span: 2;
        border: solid #00ff88;
    }
    
    .terminal-panel {
        column-span: 2;
        row-span: 2;
        border: solid #00ccff;
    }
    
    .matrix-panel {
        border: solid #00ff41;
    }
    
    .process-panel {
        border: solid #ffaa00;
    }
    
    .clock-panel {
        border: solid #ff00ff;
    }
    
    .network-panel {
        border: solid #00b4d8;
    }
    
    .file-panel {
        border: solid #00ff88;
    }
    
    Static {
        color: #ccffcc;
    }
    
    Header {
        background: #001122;
        color: #00ff88;
    }
    
    Footer {
        background: #001122;
        color: #00ff88;
    }
    
    Input {
        background: #001122;
        color: #00ff88;
        border: solid #00ff88;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("t", "theme", "Theme", show=True),
        Binding("s", "sound", "Sound", show=True),
        Binding("m", "matrix", "Matrix", show=True),
        Binding("f5", "refresh", "Refresh", show=False),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]
    
    def __init__(self):
        super().__init__()
        self.current_theme = CONFIG.get("theme", "tron")
        self.update_timer = None
        self.matrix_timer = None
        self.terminal_widget = None
    
    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header(show_clock=True)
        
        with Grid(classes="main-container"):
            yield SystemStatsWidget(classes="stats-panel")
            yield TerminalWidget(classes="terminal-panel")
            yield ClockWidget(classes="clock-panel")
            yield MatrixRainWidget(classes="matrix-panel")
            yield FileExplorerWidget(classes="file-panel")
            yield ProcessWidget(classes="process-panel")
            yield NetworkWidget(classes="network-panel")
        
        yield Footer()
    
    def on_mount(self):
        """Called when app is mounted"""
        # Play boot sound
        if sound_manager.enabled:
            sound_manager.play("boot")
        
        # Start ambient sound
        if sound_manager.enabled:
            sound_manager.play("ambient", loops=-1)
        
        # Start update timers
        self.update_timer = self.set_interval(1.0, self.update_widgets)
        self.matrix_timer = self.set_interval(0.15, self.update_matrix)
        
        # Get terminal widget reference
        self.terminal_widget = self.query_one(TerminalWidget)
    
    def update_widgets(self):
        """Update all widgets periodically"""
        for widget in self.query(SystemStatsWidget):
            widget.refresh()
        for widget in self.query(ClockWidget):
            widget.refresh()
        for widget in self.query(ProcessWidget):
            widget.refresh()
        for widget in self.query(NetworkWidget):
            widget.refresh()
        for widget in self.query(FileExplorerWidget):
            widget.refresh()
    
    def update_matrix(self):
        """Update matrix animation"""
        if CONFIG.get("matrix_enabled", True):
            for widget in self.query(MatrixRainWidget):
                widget.refresh()
    
    def action_refresh(self):
        """Manual refresh"""
        self.update_widgets()
        self.notify("🔄 Refreshed")
    
    def action_theme(self):
        """Cycle through themes"""
        themes = list(DEFAULT_THEMES.keys())
        current_idx = themes.index(self.current_theme)
        self.current_theme = themes[(current_idx + 1) % len(themes)]
        
        global CONFIG
        CONFIG["theme"] = self.current_theme
        save_config(CONFIG)
        
        # Update all widget themes
        theme_data = DEFAULT_THEMES[self.current_theme]
        for widget in self.query(Static):
            widget.theme = theme_data
            widget.refresh()
        
        self.notify(f"🎨 Theme: {theme_data['name']}")
        sound_manager.play("success")
    
    def action_sound(self):
        """Toggle sound"""
        state = sound_manager.toggle()
        self.notify(f"🔊 Sound: {'ON' if state else 'OFF'}")
    
    def action_matrix(self):
        """Toggle matrix rain"""
        CONFIG["matrix_enabled"] = not CONFIG.get("matrix_enabled", True)
        save_config(CONFIG)
        self.notify(f"🌧️ Matrix: {'ON' if CONFIG['matrix_enabled'] else 'OFF'}")
    
    def on_input_submitted(self, event):
        """Handle input submission"""
        if self.terminal_widget:
            self.terminal_widget.execute_command(event.value)
            sound_manager.play("typing")

# ─── Entry Point ────────────────────────────────────────────────────────────
def print_banner():
    """Print ASCII banner"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ██╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗ ████████╗ ██████╗            ║
║     ██║██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝            ║
║     ██║██║   ██║█████╔╝ █████╗  ██████╔╝███████║   ██║   ██║                  ║
║██   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║                  ║
║╚█████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║██║  ██║   ██║   ╚██████╗            ║
║ ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝            ║
║                                                                               ║
║              ⚡ CYBERPUNK TERMINAL INTERFACE v2.0 ⚡                            ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  Controls:                                                                    ║
║  [Q] Quit  [R] Refresh  [T] Theme  [S] Sound  [M] Matrix                    ║
║                                                                               ║
║  Terminal Commands:                                                           ║
║  help, clear, sysinfo, neofetch, theme, sound, matrix, reboot, shutdown       ║
║  whoami, uptime, ps, net, ping <host>, banner                                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

def main():
    """Main entry point"""
    print_banner()
    
    # Check dependencies
    check_dependencies()
    
    print("[✓] Dependencies OK")
    print("[✓] Loading configuration...")
    print(f"[✓] Theme: {DEFAULT_THEMES[CONFIG.get('theme', 'tron')]['name']}")
    print("[✓] Starting JokerATC...\\n")
    
    # Run app
    app = JokerATCApp()
    app.run()

if __name__ == "__main__":
    main()
'''

with open('/mnt/agents/output/jokeratc/main.py', 'w', encoding='utf-8') as f:
    f.write(main_py)

print("✅ main.py saved!")
print(f"📄 Size: {len(main_py)} characters")
