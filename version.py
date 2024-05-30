# version.py

from pathlib import Path

version_file = Path(__file__).parent / 'version.txt'
version = '1.0'

if version_file.exists():
    with open(version_file, 'r') as f:
        version = f.read().strip()

print(version)
