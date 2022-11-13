from pathlib import Path

__version__ = "0.0.0rc1"

with open(Path(__file__).parent / "VERSION") as fin:
    __version__ = fin.read()
