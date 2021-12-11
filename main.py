import importlib
from pathlib import Path

from utils.debugging import force_no_debug

if __name__ == "__main__":
    force_no_debug()
    year_2021_folder = Path(__file__).parent / "year_2021"
    all_module_folders = (f for f in year_2021_folder.glob("./*") if f.is_dir() and not f.name.startswith("_") and not f.name == "template")
    for folder in all_module_folders:
        module = importlib.import_module(f"year_2021.{folder.name}.main")
        module.main()
