#!/usr/bin/env python3
"""
JokerATC - Hacker Terminal Dashboard
Author: rc8447327-jpg
GitHub: https://github.com/rc8447327-jpg/JokerATC
For educational and ethical use only.
"""

import curses
import subprocess
import threading
import time
import os
import platform
import datetime
import random
import sys

try:
    import psutil
except ImportError:
    print("Install requirements: pip install -r requirements.txt")
    sys.exit(1)

try:
    import pygame
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False

# ─────────────────────────────────────────────
#  SOUND ENGINE
# ─────────────────────────────────────────────

def init_sound():
    if not SOUND_ENABLED:
        return
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=256)
    except Exception:
        pass

def play_beep(freq=800, duration=60):
    if not SOUND_ENABLED:
        return
    try:
        import numpy as np
        sample_rate = 44100
        t = np.linspace(0, duration / 1000, int(sample_rate * duration / 1000), False)
        wave = (np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(wave)
        sound.play()
    except Exception:
        pass

def play_boot_sound():
    if not SOUND_ENABLED:
        return
    threading.Thread(target=_boot_sequence, daemon=True).start()

def _boot_sequence():
    freqs = [300, 500, 700, 900, 1100, 900, 700, 1200]
    for f in freqs:
        play_beep(f, 80)
        time.sleep(0.09)

# ─────────────────────────────────────────────
#  MATRIX RAIN
# ─────────────────────────────────────────────

MATRIX_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF@#$%^&*<>/?\\|"

class MatrixRain:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.drops = [random.randint(-height, 0) for _ in range(width)]
        self.speeds = [random.uniform(0.3, 1.0) for _ in range(width)]
        self.chars = [[random.choice(MATRIX_CHARS) for _ in range(height)] for _ in range(width)]

    def update(self):
        for i in range(self.width):
            self.drops[i] += self.speeds[i]
            if self.drops[i] > self.height:
                self.drops[i] = random.randint(-10, 0)
                self.speeds[i] = random.uniform(0.3, 1.0)
            if random.random() < 0.1:
                col = random.randint(0, self.height - 1)
                self.chars[i][col] = random.choice(MATRIX_CHARS)

    def draw(self, win, color_green, color_white, color_dim):
        h, w = win.getmaxyx()
        for x in range(min(self.width, w - 1)):
            head = int(self.drops[x])
            for y in range(min(self.height, h - 1)):
                ch = self.chars[x][y % len(self.chars[x])]
                if y == head:
                    try:
                        win.addch(y, x, ch, color_white | curses.A_BOLD)
                    except curses.error:
                        pass
                elif head - 8 < y < head:
                    try:
                        win.addch(y, x, ch, color_green | curses.A_BOLD)
                    except curses.error:
                        pass
                elif head - 20 < y <= head - 8:
                    try:
                        win.addch(y, x, ch, color_dim)
                    except curses.error:
                        pass

# ─────────────────────────────────────────────
#  SYSTEM STATS
# ─────────────────────────────────────────────

class SystemStats:
    def __init__(self):
        self.cpu = 0.0
        self.ram_used = 0
        self.ram_total = 0
        self.ram_pct = 0.0
        self.cpu_temp = None
        self.disk_used = 0
        self.disk_total = 0
        self._running = True
        threading.Thread(target=self._update_loop, daemon=True).start()

    def _update_loop(self):
        while self._running:
            try:
                self.cpu = psutil.cpu_percent(interval=1)
                vm = psutil.virtual_memory()
                self.ram_used = vm.used // (1024 ** 2)
                self.ram_total = vm.total // (1024 ** 2)
                self.ram_pct = vm.percent
                du = psutil.disk_usage('/')
                self.disk_used = du.used // (1024 ** 3)
                self.disk_total = du.total // (1024 ** 3)
                # CPU temperature
                try:
                    temps = psutil.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            if entries:
                                self.cpu_temp = entries[0].current
                                break
                except Exception:
                    self.cpu_temp = None
            except Exception:
                pass
            time.sleep(1)

    def stop(self):
        self._running = False

# ─────────────────────────────────────────────
#  FILE EXPLORER
# ─────────────────────────────────────────────

class FileExplorer:
    def __init__(self):
        self.cwd = os.path.expanduser("~")
        self.entries = []
        self.scroll = 0
        self.selected = 0
        self.refresh()

    def refresh(self):
        try:
            items = os.listdir(self.cwd)
            dirs = sorted([i for i in items if os.path.isdir(os.path.join(self.cwd, i))])
            files = sorted([i for i in items if os.path.isfile(os.path.join(self.cwd, i))])
            self.entries = [".."] + dirs + files
        except PermissionError:
            self.entries = ["[Permission Denied]"]
        self.scroll = 0
        self.selected = 0

    def enter(self):
        if not self.entries:
            return
        sel = self.entries[self.selected]
        if sel == "..":
            self.cwd = os.path.dirname(self.cwd)
        else:
            path = os.path.join(self.cwd, sel)
            if os.path.isdir(path):
                self.cwd = path
        self.refresh()

    def move(self, direction):
        self.selected = max(0, min(len(self.entries) - 1, self.selected + direction))

# ─────────────────────────────────────────────
#  TERMINAL EMULATOR
# ─────────────────────────────────────────────

class Terminal:
    def __init__(self):
        self.history = []
        self.input_buf = ""
        self.cwd = os.path.expanduser("~")
        self.history.append(("sys", "JokerATC Terminal Ready. Type commands below."))
        self.history.append(("sys", f"cwd: {self.cwd}"))

    def run_command(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return
        self.history.append(("in", f"$ {cmd}"))
        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            if path == "~":
                path = os.path.expanduser("~")
            elif not os.path.isabs(path):
                path = os.path.join(self.cwd, path)
            if os.path.isdir(path):
                self.cwd = path
                self.history.append(("out", f"→ {self.cwd}"))
            else:
                self.history.append(("err", f"cd: {path}: No such directory"))
        elif cmd == "clear":
            self.history.clear()
        else:
            try:
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True,
                    cwd=self.cwd, timeout=10
                )
                if result.stdout:
                    for line in result.stdout.splitlines()[-30:]:
                        self.history.append(("out", line))
                if result.stderr:
                    for line in result.stderr.splitlines()[-10:]:
                        self.history.append(("err", line))
            except subprocess.TimeoutExpired:
                self.history.append(("err", "Command timed out."))
            except Exception as e:
                self.history.append(("err", str(e)))
        # Keep history manageable
        if len(self.history) > 200:
            self.history = self.history[-200:]

# ─────────────────────────────────────────────
#  ASCII BANNER
# ─────────────────────────────────────────────

BANNER = [
    r"       ██╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗ ████████╗ ██████╗",
    r"       ██║██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝",
    r"       ██║██║   ██║█████╔╝ █████╗  ██████╔╝███████║   ██║   ██║     ",
    r"  ██   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║     ",
    r"  ╚█████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║██║  ██║   ██║   ╚██████╗",
    r"   ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝",
    r"                          [ A T C ]  v1.0  |  by rc8447327-jpg",
]

# ─────────────────────────────────────────────
#  DRAW HELPERS
# ─────────────────────────────────────────────

def draw_box(win, y, x, h, w, title, color):
    try:
        win.attron(color)
        win.border()
        win.attroff(color)
        # Draw box manually
        for i in range(w - 2):
            try:
                win.addch(0, i + 1, curses.ACS_HLINE, color)
                win.addch(h - 1, i + 1, curses.ACS_HLINE, color)
            except curses.error:
                pass
        for i in range(h - 2):
            try:
                win.addch(i + 1, 0, curses.ACS_VLINE, color)
                win.addch(i + 1, w - 1, curses.ACS_VLINE, color)
            except curses.error:
                pass
        for corner in [(0, 0, curses.ACS_ULCORNER), (0, w-1, curses.ACS_URCORNER),
                       (h-1, 0, curses.ACS_LLCORNER), (h-1, w-1, curses.ACS_LRCORNER)]:
            try:
                win.addch(corner[0], corner[1], corner[2], color)
            except curses.error:
                pass
        if title:
            label = f"[ {title} ]"
            tx = max(1, (w - len(label)) // 2)
            try:
                win.addstr(0, tx, label, color | curses.A_BOLD)
            except curses.error:
                pass
    except curses.error:
        pass

def bar(value, maxval, width=20, fill="█", empty="░"):
    filled = int((value / maxval) * width) if maxval else 0
    return fill * filled + empty * (width - filled)

# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────

class JokerATC:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stats = SystemStats()
        self.terminal = Terminal()
        self.explorer = FileExplorer()
        self.focus = "terminal"  # terminal | explorer
        self.show_matrix = True
        self.matrix = None
        self.tick = 0
        self.input_mode = False
        self._setup_colors()
        init_sound()
        play_boot_sound()
        self._show_boot_screen()

    def _setup_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)       # green
        curses.init_pair(2, curses.COLOR_RED, -1)         # red
        curses.init_pair(3, curses.COLOR_BLUE, -1)        # blue
        curses.init_pair(4, curses.COLOR_WHITE, -1)       # white
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)  # selected
        curses.init_pair(6, curses.COLOR_CYAN, -1)        # cyan accent
        curses.init_pair(7, 8, -1)                        # dim green (dark)

        self.C_GREEN = curses.color_pair(1)
        self.C_RED   = curses.color_pair(2)
        self.C_BLUE  = curses.color_pair(3)
        self.C_WHITE = curses.color_pair(4)
        self.C_SEL   = curses.color_pair(5)
        self.C_CYAN  = curses.color_pair(6)
        self.C_DIM   = curses.color_pair(7)

    def _show_boot_screen(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        lines = BANNER
        start_y = max(0, (h - len(lines) - 4) // 2)
        for i, line in enumerate(lines):
            x = max(0, (w - len(line)) // 2)
            color = self.C_RED if i == len(lines) - 1 else self.C_GREEN
            try:
                self.stdscr.addstr(start_y + i, x, line[:w-1], color | curses.A_BOLD)
            except curses.error:
                pass
        msg = "[ INITIALIZING SYSTEMS... ]"
        try:
            self.stdscr.addstr(start_y + len(lines) + 2, max(0, (w - len(msg)) // 2),
                               msg, self.C_RED | curses.A_BLINK)
        except curses.error:
            pass
        self.stdscr.refresh()
        time.sleep(2.5)

    def run(self):
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        self.input_mode = False

        while True:
            h, w = self.stdscr.getmaxyx()

            if h < 24 or w < 80:
                self.stdscr.clear()
                try:
                    self.stdscr.addstr(0, 0, "Terminal too small! Min: 80x24", self.C_RED)
                except curses.error:
                    pass
                self.stdscr.refresh()
                time.sleep(0.2)
                continue

            # Layout math
            # Top: banner strip (3 lines)
            # Left col (~55%): terminal (top 60%) | explorer (bottom 40%)
            # Right col (~45%): stats + clock + matrix

            left_w = int(w * 0.57)
            right_w = w - left_w
            top_h = 3
            term_h = int((h - top_h) * 0.62)
            expl_h = h - top_h - term_h
            stat_h = 14
            mat_h  = h - top_h - stat_h

            self.stdscr.erase()

            # ── HEADER ──
            self._draw_header(top_h, w)

            # ── TERMINAL ──
            term_win = curses.newwin(term_h, left_w, top_h, 0)
            self._draw_terminal(term_win, term_h, left_w)

            # ── EXPLORER ──
            expl_win = curses.newwin(expl_h, left_w, top_h + term_h, 0)
            self._draw_explorer(expl_win, expl_h, left_w)

            # ── STATS ──
            stat_win = curses.newwin(stat_h, right_w, top_h, left_w)
            self._draw_stats(stat_win, stat_h, right_w)

            # ── MATRIX ──
            mat_win = curses.newwin(mat_h, right_w, top_h + stat_h, left_w)
            self._draw_matrix(mat_win, mat_h, right_w)

            # Refresh all
            self.stdscr.noutrefresh()
            term_win.noutrefresh()
            expl_win.noutrefresh()
            stat_win.noutrefresh()
            mat_win.noutrefresh()
            curses.doupdate()

            # Input
            try:
                key = self.stdscr.getch()
            except Exception:
                key = -1

            if key != -1:
                self._handle_key(key)

            self.tick += 1
            time.sleep(0.05)

    def _draw_header(self, top_h, w):
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %d %B %Y")
        time_str = now.strftime("%H:%M:%S")
        title = "◈ J O K E R A T C ◈"
        try:
            self.stdscr.addstr(0, 0, "─" * w, self.C_RED)
            tx = max(0, (w - len(title)) // 2)
            self.stdscr.addstr(1, tx, title, self.C_RED | curses.A_BOLD)
            self.stdscr.addstr(1, 2, f"[{date_str}]", self.C_GREEN)
            ts = f"[{time_str}]"
            self.stdscr.addstr(1, w - len(ts) - 2, ts, self.C_CYAN | curses.A_BOLD)
            hint = " TAB:switch focus  F:explorer  Q:quit  M:matrix toggle "
            self.stdscr.addstr(2, 0, "─" * w, self.C_RED)
            hx = max(0, (w - len(hint)) // 2)
            self.stdscr.addstr(2, hx, hint, self.C_DIM)
        except curses.error:
            pass

    def _draw_terminal(self, win, h, w):
        color = self.C_GREEN if self.focus == "terminal" else self.C_WHITE
        draw_box(win, 0, 0, h, w, "TERMINAL", color)
        lines_area = h - 3
        visible = self.terminal.history[-lines_area:] if len(self.terminal.history) > lines_area else self.terminal.history
        for i, (kind, line) in enumerate(visible):
            y = 1 + i
            if y >= h - 2:
                break
            c = self.C_GREEN if kind == "out" else self.C_RED if kind == "err" else self.C_CYAN
            try:
                win.addstr(y, 2, line[:w-4], c)
            except curses.error:
                pass
        # Input line
        prompt = f"$ {self.terminal.input_buf}"
        if self.focus == "terminal":
            cursor = "█" if (self.tick // 10) % 2 == 0 else " "
            prompt += cursor
        try:
            win.addstr(h - 2, 2, prompt[:w-4], self.C_WHITE | curses.A_BOLD)
        except curses.error:
            pass

    def _draw_explorer(self, win, h, w):
        color = self.C_BLUE if self.focus == "explorer" else self.C_WHITE
        draw_box(win, 0, 0, h, w, "FILE EXPLORER", color)
        cwd_display = self.explorer.cwd[-w+6:] if len(self.explorer.cwd) > w - 6 else self.explorer.cwd
        try:
            win.addstr(1, 2, f"⌂ {cwd_display}", self.C_CYAN)
        except curses.error:
            pass
        visible_h = h - 4
        start = max(0, self.explorer.selected - visible_h + 1)
        for i, entry in enumerate(self.explorer.entries[start:start + visible_h]):
            y = 2 + i
            if y >= h - 2:
                break
            full = os.path.join(self.explorer.cwd, entry)
            is_dir = os.path.isdir(full) or entry == ".."
            icon = "▶ " if is_dir else "  "
            c = self.C_BLUE if is_dir else self.C_WHITE
            line = f"{icon}{entry}"
            if (i + start) == self.explorer.selected and self.focus == "explorer":
                try:
                    win.addstr(y, 2, line[:w-4], self.C_SEL | curses.A_BOLD)
                except curses.error:
                    pass
            else:
                try:
                    win.addstr(y, 2, line[:w-4], c)
                except curses.error:
                    pass

    def _draw_stats(self, win, h, w):
        draw_box(win, 0, 0, h, w, "SYSTEM STATS", self.C_RED)
        s = self.stats
        now = datetime.datetime.now()

        def stat_line(y, label, val_str, bar_str, color):
            try:
                win.addstr(y, 2, label, self.C_WHITE | curses.A_BOLD)
                win.addstr(y, 2 + len(label), val_str, color)
            except curses.error:
                pass
            if bar_str:
                try:
                    win.addstr(y + 1, 2, bar_str, color)
                except curses.error:
                    pass

        bw = max(8, w - 18)

        # CPU
        cpu_color = self.C_RED if s.cpu > 80 else self.C_GREEN
        stat_line(1, "CPU  ", f"{s.cpu:5.1f}%", bar(s.cpu, 100, bw) + f" {s.cpu:.0f}%", cpu_color)

        # RAM
        ram_color = self.C_RED if s.ram_pct > 80 else self.C_GREEN
        stat_line(3, "RAM  ", f"{s.ram_used}M/{s.ram_total}M",
                  bar(s.ram_pct, 100, bw) + f" {s.ram_pct:.0f}%", ram_color)

        # DISK
        disk_pct = (s.disk_used / s.disk_total * 100) if s.disk_total else 0
        disk_color = self.C_RED if disk_pct > 85 else self.C_BLUE
        stat_line(5, "DISK ", f"{s.disk_used}G/{s.disk_total}G",
                  bar(disk_pct, 100, bw) + f" {disk_pct:.0f}%", disk_color)

        # CPU Temp
        if s.cpu_temp is not None:
            temp_color = self.C_RED if s.cpu_temp > 75 else self.C_GREEN
            temp_str = f"{s.cpu_temp:.1f}°C"
            heat_bar = bar(s.cpu_temp, 100, bw)
            try:
                win.addstr(7, 2, "TEMP ", self.C_WHITE | curses.A_BOLD)
                win.addstr(7, 7, temp_str, temp_color | curses.A_BOLD)
                win.addstr(8, 2, heat_bar, temp_color)
            except curses.error:
                pass
        else:
            try:
                win.addstr(7, 2, "TEMP  N/A (sensors not available)", self.C_DIM)
            except curses.error:
                pass

        # Clock
        try:
            win.addstr(10, 2, "─" * (w - 4), self.C_RED)
            t_str = now.strftime("%H:%M:%S")
            d_str = now.strftime("%d %b %Y")
            day_str = now.strftime("%A")
            cx = max(2, (w - len(t_str)) // 2)
            win.addstr(11, cx, t_str, self.C_RED | curses.A_BOLD)
            dx = max(2, (w - len(d_str)) // 2)
            win.addstr(12, dx, d_str, self.C_GREEN)
            dayx = max(2, (w - len(day_str)) // 2)
            win.addstr(13, dayx, day_str, self.C_CYAN)
        except curses.error:
            pass

    def _draw_matrix(self, win, h, w):
        draw_box(win, 0, 0, h, w, "MATRIX", self.C_GREEN)
        if not self.show_matrix:
            try:
                msg = "[ MATRIX DISABLED - press M ]"
                win.addstr(h // 2, max(1, (w - len(msg)) // 2), msg, self.C_DIM)
            except curses.error:
                pass
            return
        if self.matrix is None or self.matrix.width != w - 2 or self.matrix.height != h - 2:
            self.matrix = MatrixRain(w - 2, h - 2)
        if self.tick % 2 == 0:
            self.matrix.update()
        # Draw in inner area
        inner = win.derwin(h - 2, w - 2, 1, 1)
        self.matrix.draw(inner, self.C_GREEN, self.C_WHITE, self.C_DIM)

    def _handle_key(self, key):
        if self.focus == "terminal":
            if key == 9:  # TAB
                self.focus = "explorer"
                play_beep(600, 40)
            elif key == ord('q') or key == ord('Q'):
                if not self.terminal.input_buf:
                    self._quit()
                else:
                    self.terminal.input_buf += 'q'
                    play_beep(800, 30)
            elif key == ord('m') or key == ord('M'):
                if not self.terminal.input_buf:
                    self.show_matrix = not self.show_matrix
                    play_beep(500, 40)
                else:
                    self.terminal.input_buf += 'm'
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                self.terminal.input_buf = self.terminal.input_buf[:-1]
                play_beep(400, 20)
            elif key == ord('\n') or key == curses.KEY_ENTER or key == 10:
                cmd = self.terminal.input_buf
                self.terminal.input_buf = ""
                threading.Thread(target=self.terminal.run_command, args=(cmd,), daemon=True).start()
                play_beep(900, 50)
            elif 32 <= key <= 126:
                self.terminal.input_buf += chr(key)
                play_beep(700 + random.randint(-100, 100), 25)

        elif self.focus == "explorer":
            if key == 9:  # TAB
                self.focus = "terminal"
                play_beep(600, 40)
            elif key == curses.KEY_UP:
                self.explorer.move(-1)
                play_beep(500, 20)
            elif key == curses.KEY_DOWN:
                self.explorer.move(1)
                play_beep(500, 20)
            elif key in (ord('\n'), curses.KEY_ENTER, 10):
                self.explorer.enter()
                play_beep(800, 40)
            elif key == ord('q') or key == ord('Q'):
                self._quit()
            elif key == ord('m') or key == ord('M'):
                self.show_matrix = not self.show_matrix
                play_beep(500, 40)

    def _quit(self):
        play_beep(300, 200)
        self.stats.stop()
        curses.endwin()
        print("\n[JokerATC] Session terminated. Stay ethical. 🃏")
        sys.exit(0)


def main():
    os.environ.setdefault('TERM', 'xterm-256color')
    try:
        curses.wrapper(lambda s: JokerATC(s).run())
    except KeyboardInterrupt:
        print("\n[JokerATC] Interrupted.")


if __name__ == "__main__":
    main()
