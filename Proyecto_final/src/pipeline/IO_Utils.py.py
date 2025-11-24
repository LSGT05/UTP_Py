"""
IO_Utils.py
Funciones auxiliares para rutas y operaciones con archivos (sin dependencias externas).
"""
from pathlib import Path
from typing import List

# Nombres de carpetas relativas al BASE (no hardcodear root absoluto)
RAW_DIRNAME = "data/raw"
PROCESSED_DIRNAME = "data/processed"
PLOTS_DIRNAME = "plots"
REPORTS_DIRNAME = "reports"

def Root(base: Path) -> Path:
    """Devuelve el path base del proyecto (wrapper simple)."""
    return Path(base)

def ensure_dirs(base: Path):
    """Crear carpetas necesarias si no existen (raw, processed, plots, reports)."""
    base = Root(base)
    (base / RAW_DIRNAME).mkdir(parents=True, exist_ok=True)
    (base / PROCESSED_DIRNAME).mkdir(parents=True, exist_ok=True)
    (base / PLOTS_DIRNAME).mkdir(parents=True, exist_ok=True)
    (base / REPORTS_DIRNAME).mkdir(parents=True, exist_ok=True)

def list_raw_csvs(base: Path) -> List[Path]:
    """Lista los archivos .csv dentro de data/raw (devuelve Paths)."""
    base = Root(base)
    raw_dir = base / RAW_DIRNAME
    if not raw_dir.exists():
        return []
    return sorted([p for p in raw_dir.iterdir() if p.is_file() and p.suffix.lower() == ".csv"])

def make_clean_name(path: Path) -> Path:
    """Genera un nombre para archivo 'limpio' en data/processed."""
    return Path(PROCESSED_DIRNAME) / f"clean_{path.name}"

def safe_stem(path: Path) -> str:
    """Devuelve un stem seguro (sin espacios ni guiones)."""
    return path.stem.replace(" ", "_").replace("-", "_")
