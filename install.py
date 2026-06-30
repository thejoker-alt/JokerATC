# ═══════════════════════════════════════════════════════════════════════════════
# FILE 6: install.py (Auto-installer script)
# ═══════════════════════════════════════════════════════════════════════════════

install_script = '''#!/usr/bin/env python3
"""
JokerATC v2.0 - Auto Installer
==============================
Run this script to automatically install all dependencies and setup JokerATC.

Usage:
    python install.py
"""

import os
import sys
import subprocess
import platform

def print_banner():
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
║                         ⚡ AUTO INSTALLER v2.0 ⚡                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required!")
        print(f"   Current: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\\n📦 Installing dependencies...\\n")
    
    # Required packages
    packages = [
        ("textual", "TUI Framework"),
        ("rich", "Rich Text Formatting"),
        ("psutil", "System Monitoring"),
        ("pygame", "Sound Effects (optional)"),
    ]
    
    installed = []
    failed = []
    
    for package, description in packages:
        print(f"   Installing {package} ({description})...", end=" ")
        if install_package(package):
            print("✅")
            installed.append(package)
        else:
            print("❌")
            failed.append(package)
    
    print("\\n" + "="*60)
    print(f"✅ Installed: {len(installed)} packages")
    if failed:
        print(f"❌ Failed: {', '.join(failed)}")
    print("="*60)
    
    # Check if main.py exists
    if os.path.exists("main.py"):
        print("\\n🚀 JokerATC is ready to run!")
        print("   Command: python main.py")
    else:
        print("\\n⚠️  main.py not found in current directory!")
        print("   Make sure you're in the JokerATC directory.")
    
    print("\\n📖 For help: python main.py --help")

if __name__ == "__main__":
    main()
'''

with open('/mnt/agents/output/jokeratc/install.py', 'w') as f:
    f.write(install_script)

print("✅ install.py saved!")

# ═══════════════════════════════════════════════════════════════════════════════
# FILE 7: .gitignore
# ═══════════════════════════════════════════════════════════════════════════════

gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# JokerATC specific
config.json
sounds/generated/
*.log
'''

with open('/mnt/agents/output/jokeratc/.gitignore', 'w') as f:
    f.write(gitignore)

print("✅ .gitignore saved!")

# ═══════════════════════════════════════════════════════════════════════════════
# FILE 8: LICENSE (MIT)
# ═══════════════════════════════════════════════════════════════════════════════

license_text = '''MIT License

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
'''

with open('/mnt/agents/output/jokeratc/LICENSE', 'w') as f:
    f.write(license_text)

print("✅ LICENSE saved!")

# ═══════════════════════════════════════════════════════════════════════════════
# FILE 9: start.sh (Linux/Mac startup script)
# ═══════════════════════════════════════════════════════════════════════════════

start_sh = '''#!/bin/bash
# JokerATC Startup Script for Linux/macOS

echo "⚡ Starting JokerATC..."
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Please install Python 3.8+"
    exit 1
fi

# Check dependencies
python3 -c "import textual, rich, psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Run JokerATC
python3 main.py "$@"
'''

with open('/mnt/agents/output/jokeratc/start.sh', 'w') as f:
    f.write(start_sh)

print("✅ start.sh saved!")

# ═══════════════════════════════════════════════════════════════════════════════
# FILE 10: start.bat (Windows startup script)
# ═══════════════════════════════════════════════════════════════════════════════

start_bat = '''@echo off
REM JokerATC Startup Script for Windows

echo ⚡ Starting JokerATC...
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    exit /b 1
)

REM Check dependencies
python -c "import textual, rich, psutil" 2>nul
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Run JokerATC
python main.py %*
'''

with open('/mnt/agents/output/jokeratc/start.bat', 'w') as f:
    f.write(start_bat)

print("✅ start.bat saved!")

print("\n" + "="*60)
print("📦 ALL JOKERATC FILES CREATED SUCCESSFULLY!")
print("="*60)

# List all files
import os
print("\n📁 Project Structure:")
for root, dirs, files in os.walk('/mnt/agents/output/jokeratc'):
    level = root.replace('/mnt/agents/output/jokeratc', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        filepath = os.path.join(root, file)
        size = os.path.getsize(filepath)
        print(f'{subindent}{file} ({size:,} bytes)')
