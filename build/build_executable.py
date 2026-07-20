"""Build configuration and PyInstaller setup"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent
os.chdir(project_root)

# Build arguments
build_args = [
    'src/main.py',
    '--name=VulnerabilityScanner',
    '--onefile',
    '--windowed',
    '--icon=build/app.ico',
    '--add-data=src:src',
    '--add-data=data:data',
    '--hidden-import=PyQt6',
    '--hidden-import=nmap',
    '--collect-all=nmap',
    '--distpath=dist',
    '--buildpath=build/.build',
    '--specpath=build',
]

print("Building Network Vulnerability Scanner executable...")
print(f"Project root: {project_root}")
print(f"Build arguments: {build_args}")

try:
    PyInstaller.__main__.run(build_args)
    print("\n✓ Build completed successfully!")
    print(f"Executable location: {project_root / 'dist' / 'VulnerabilityScanner.exe'}")
except Exception as e:
    print(f"\n✗ Build failed: {e}")
    sys.exit(1)
