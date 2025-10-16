# comandos útiles para gestionar carpetas de entradas y salidas.
from pathlib import Path
import re

def Root(file=__file__) -> Path:
    """Ubica la carpeta raíz (ROOT) del archivo de trabajo."""
    return Path(file).resolve().parents[0]

def ensure_dirs(*dirs: Path) -> None:
    """Crea las carpetas especificadas si no existen."""
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        
def safe_stem(p: Path) -> str:
    """Nombre seguro (sin espacios, acentos ni símbolos raros) para salidas."""
    base = p.stem.strip().replace(" ", "_")
    base = re.sub(r"[^A-Za-z0-9_\-]+", "", base)
    return base or "archivo"

def detectar_delimitador(path: Path) -> str:
    """Detecta ';' o ',' a partir de la primera línea del archivo CSV."""
    with path.open("r", encoding="utf-8", newline="") as f:
        head = f.readline()
    return ";" if head.count(";") > head.count(",") else ","

def list_raw_csvs(raw_dir: Path, pattern: str = "*.csv"):
    """Lista los archivos CSV crudos en la carpeta data/raw/."""
    return sorted(raw_dir.glob(pattern), key=lambda p: p.name.lower())

def make_clean_name(p: Path) -> str:
    """
    Genera un nombre de salida 'limpio' a partir del nombre original:
      - si contiene 'sucio'/'sucios' → reemplaza por 'limpio'/'limpios'
      - si no contiene → agrega sufijo '_limpio'
    """
    nombre = p.stem
    if "sucio" in nombre:
        nombre = nombre.replace("sucios", "limpios").replace("sucio", "limpio")
    else:
        nombre = f"{nombre}_limpio"
    return f"{nombre}.csv"
