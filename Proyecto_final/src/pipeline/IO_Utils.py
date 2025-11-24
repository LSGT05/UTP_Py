import os
from pathlib import Path

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")
REPORTS_DIR = Path("reports")
PLOTS_DIR = Path("plots")


def ensure_dirs():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def list_raw_csvs():
    return list(RAW_DIR.glob("*.csv"))


def make_clean_name(path: Path) -> Path:
    return CLEAN_DIR / f"clean_{path.name}"


def safe_stem(path: Path) -> str:
    return path.stem.replace(" ", "_").replace("-", "_")
