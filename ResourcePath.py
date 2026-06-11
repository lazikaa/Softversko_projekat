from pathlib import Path
import sys

def resoursce_path(*parts):
    if hasattr(sys, "_MEIPASS"):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).resolve().parent
    return str(base_dir.joinpath(*parts))
