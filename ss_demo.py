# ═══════════════════════════════════════════════════════════════════════════════
# FILE 13: screenshot_demo.py (Demo script to show what JokerATC looks like)
# ═══════════════════════════════════════════════════════════════════════════════

screenshot_demo = '''#!/usr/bin/env python3
"""
JokerATC Screenshot Demo
========================
This script generates a visual representation of what JokerATC looks like
when running. Useful for documentation and screenshots.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.tree import Tree as RichTree
from rich.align import Align
from rich import box
import random
import time

console = Console()

def generate_matrix_rain(width=60, height=10):
    """Generate matrix rain text"""
    chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEF"
    lines = []
    for _ in range(height):
        line = ""
        for _ in range(width):
            if random.random() > 0.7:
                line += random.choice(chars)
            else:
                line += " "
        lines.append(line)
    return "\\n".join(lines)

def show_jokeratc_demo():
    """Show JokerATC demo interface"""
    console.clear()
    
    # Header
    header = Panel(
        "[bold #00ff88]⚡ JOKERATC v2.0 - Cyberpunk Terminal Interface[/]    [dim]joker@kali[/]",
        border_style="#00ff88",
        box=box.DOUBLE
    )
    console.print(header)
    console.print()
    
    # System Stats
    stats_table = Table(
        box=box.DOUBLE_EDGE,
        border_style="#00ff88",
        show_header=False
    )
    stats_table.add_column("Metric", style="bold #00ccff", width=10)
    stats_table.add_column("Value", style="#ccffcc", width=18)
    stats_table.add_column("Bar", width=22)
    
    stats_table.add_row("[bold]CPU[/]", "23.5% (8 cores)", "[green]████░░░░░░░░░░░░░░░░[/]")
    stats_table.add_row("[bold]RAM[/]", "4.2/16.0 GB", "[green]███████░░░░░░░░░░░░░[/]")
    stats_table.add_row("[bold]DISK[/]", "45%", "[yellow]█████████░░░░░░░░░░░[/]")
    stats_table.add_row("[bold]TEMP[/]", "42.0°C", "[green]████████░░░░░░░░░░░░[/]")
    
    stats_panel = Panel(
        stats_table,
        border_style="#00ff88",
        title="[bold #00ff88]◉ SYSTEM MONITOR[/]",
        title_align="left",
        subtitle="[dim]CPU: 2400 MHz[/dim]",
        subtitle_align="right"
    )
    
    # Terminal
    terminal_content = """[bold #00ff88]╔══════════════════════════════════════════════════════════╗[/]
[bold #00ff88]║[/]  [bold]JOKERATC v2.0 - Cyberpunk Terminal Interface[/]              [bold #00ff88]║[/]
[bold #00ff88]║[/]  [dim]Type 'help' for available commands[/]                        [bold #00ff88]║[/]
[bold #00ff88]╚══════════════════════════════════════════════════════════╝[/]

[bold #00ff88]┌──([/#00ccffuser@jokeratc[/#00ff88])-[[/]~[bold #00ff88])[/]
[bold #00ff88]└─▶[/] help
[bold cyan]Available Commands:[/]
  [green]help[/]      - Show this help message
  [green]sysinfo[/]   - Show system information
  [green]theme[/]     - List available themes
  [green]sound[/]     - Toggle sound effects
  [green]matrix[/]    - Toggle matrix rain

[bold #00ff88]┌──([/#00ccffuser@jokeratc[/#00ff88])-[[/]~[bold #00ff88])[/]
[bold #00ff88]└─▶[/] """
    
    terminal_panel = Panel(
        terminal_content,
        border_style="#00ccff",
        title="[bold #00ccff]💻 TERMINAL[/]",
        title_align="left",
        subtitle="[dim]History: 12 lines[/dim]",
        subtitle_align="right"
    )
    
    # Clock
    clock_text = Text()
    clock_text.append("18:06:42\\n", style="bold #00ff88")
    clock_text.append("Tuesday, 30 June 2026\\n", style="dim #00ccff")
    clock_text.append("Week 26", style="dim #00ffaa")
    
    clock_panel = Panel(
        Align.center(clock_text),
        border_style="#00ff88",
        title="[bold #00ff88]🕐 TIME[/]",
        title_align="left"
    )
    
    # Matrix Rain
    matrix_text = Text(generate_matrix_rain(), style="bold green")
    matrix_panel = Panel(
        matrix_text,
        border_style="#00ff41",
        title="[bold #00ff41]🌧️  MATRIX RAIN[/]",
        title_align="left"
    )
    
    # File Explorer
    file_tree = RichTree("[bold #00ff88]📁 /home/joker[/]", guide_style="#00ccff")
    file_tree.add("[bold #00ccff]📂 .config[/]")
    file_tree.add("[bold #00ccff]📂 .local[/]")
    file_tree.add("🐍 main.py [dim](54.5 KB)[/dim]")
    file_tree.add("📋 README.md [dim](5.4 KB)[/dim]")
    file_tree.add("📦 requirements.txt [dim](288 B)[/dim]")
    file_tree.add("⚙️ install.py [dim](4.1 KB)[/dim]")
    
    file_panel = Panel(
        file_tree,
        border_style="#00ff88",
        title="[bold #00ff88]📂 FILE EXPLORER[/]",
        title_align="left",
        subtitle="[dim]6 items[/dim]",
        subtitle_align="right"
    )
    
    # Processes
    proc_table = Table(
        box=box.SIMPLE_HEAD,
        border_style="#ffaa00",
        show_header=True,
        header_style="bold #00ff88"
    )
    proc_table.add_column("PID", style="#00ccff", width=7)
    proc_table.add_column("NAME", style="#ccffcc", width=18)
    proc_table.add_column("USER", style="dim", width=10)
    proc_table.add_column("CPU%", justify="right", width=7)
    proc_table.add_column("MEM%", justify="right", width=7)
    
    proc_table.add_row("1234", "python3", "joker", "[green]12.5%[/]", "[green]3.2%[/]")
    proc_table.add_row("5678", "chrome", "joker", "[yellow]8.3%[/]", "[yellow]15.1%[/]")
    proc_table.add_row("9012", "node", "joker", "[green]4.1%[/]", "[green]2.8%[/]")
    
    proc_panel = Panel(
        proc_table,
        border_style="#ffaa00",
        title="[bold #ffaa00]⚡ PROCESSES (TOP 10)[/]",
        title_align="left"
    )
    
    # Network
    net_content = """[bold #00ccff]Network Interfaces:[/]
  eth0: [cyan]192.168.1.100[/]
  lo: [cyan]127.0.0.1[/]

[bold #00ccff]Real-time Speed:[/]
  [green]▼[/] Download: 1.2 MB/s
  [green]████████████████░░░░░░[/]
  [yellow]▲[/] Upload: 0.3 MB/s
  [yellow]████░░░░░░░░░░░░░░░░░░[/]

[bold #00ccff]Total Traffic:[/]
  [green]▼[/] Received: 15.4 GB
  [yellow]▲[/] Sent: 3.2 GB
"""
    
    net_panel = Panel(
        net_content,
        border_style="#00b4d8",
        title="[bold #00b4d8]🌐 NETWORK[/]",
        title_align="left"
    )
    
    # Layout: Top row
    console.print("[dim]┌─ System Stats ───────────────────┬─ Terminal ─────────────────────────────────────┐[/]")
    console.print(stats_panel)
    console.print(terminal_panel)
    
    # Layout: Bottom row
    console.print("[dim]├─ Clock ───────┬─ Matrix ───────┬─ Files ───────┬─ Processes ─────┬─ Network ─────┤[/]")
    console.print(clock_panel)
    console.print(matrix_panel)
    console.print(file_panel)
    console.print(proc_panel)
    console.print(net_panel)
    
    # Footer
    footer = Panel(
        "[bold #00ff88]Q[/] Quit  [bold #00ff88]R[/] Refresh  [bold #00ff88]T[/] Theme  [bold #00ff88]S[/] Sound  [bold #00ff88]M[/] Matrix  [dim]|  JokerATC v2.0 | MIT License[/]",
        border_style="#00ff88",
        box=box.SINGLE
    )
    console.print(footer)

if __name__ == "__main__":
    show_jokeratc_demo()
'''

with open('/mnt/agents/output/jokeratc/screenshot_demo.py', 'w') as f:
    f.write(screenshot_demo)

print("✅ screenshot_demo.py saved!")

# ═══════════════════════════════════════════════════════════════════════════════
# Create a zip file of the entire project
# ═══════════════════════════════════════════════════════════════════════════════

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
print(f"✅ jokeratc_v2.0_complete.zip created! ({zip_size:,} bytes)")

print("\n" + "="*70)
print("🎉 JOKERATC v2.0 - COMPLETE PROJECT DELIVERED!")
print("="*70)
print(f"""
📦 Project Files:
   ├── main.py              (54,548 bytes) - Main application
   ├── requirements.txt       (288 bytes)   - Dependencies
   ├── README.md             (5,433 bytes) - Documentation
   ├── config.json           (299 bytes)   - Configuration
   ├── install.py            (4,075 bytes) - Auto-installer
   ├── sound_generator.py    (7,319 bytes) - Sound generator
   ├── utils.py              (5,477 bytes) - Utilities
   ├── screenshot_demo.py    (~ bytes)     - Demo script
   ├── start.sh              (477 bytes)   - Linux/Mac startup
   ├── start.bat             (452 bytes)   - Windows startup
   ├── .gitignore            (347 bytes)   - Git ignore rules
   ├── LICENSE               (1,065 bytes) - MIT License
   ├── themes/default.json   (352 bytes)   - Theme template
   └── sounds/               (empty)       - Sound directory

🚀 Quick Start:
   1. cd jokeratc
   2. pip install -r requirements.txt
   3. python main.py

🎨 Features:
   ✅ 6 Themes (TRON, MATRIX, CYBERPUNK, AMBER, NEON, OCEAN)
   ✅ Real-time System Monitoring (CPU, RAM, Disk, Network, Temp)
   ✅ Matrix Rain Animation
   ✅ Sci-fi Sound Effects (Boot, Typing, Ambient, Alert, Success)
   ✅ File Explorer with Icons
   ✅ Process Viewer
   ✅ Built-in Terminal with 15+ Commands
   ✅ Network Speed Monitor
   ✅ Auto-installer for dependencies
   ✅ Cross-platform (Linux, macOS, Windows)

🎵 Sound Effects:
   - Boot: Futuristic power-up sequence
   - Typing: Tech blips on keystrokes
   - Ambient: Background drone atmosphere
   - Alert: Warning beeps
   - Success: Positive chimes
   - Hover: UI interaction sounds

💻 Terminal Commands:
   help, clear, sysinfo, neofetch, theme, sound, matrix
   reboot, shutdown, whoami, uptime, ps, net, ping, banner

📊 Total Size: {total_size:,} bytes ({total_size/1024:.1f} KB)
📦 ZIP Size: {zip_size:,} bytes ({zip_size/1024:.1f} KB)
""")
print("="*70)
