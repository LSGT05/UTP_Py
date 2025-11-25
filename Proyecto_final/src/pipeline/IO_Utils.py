import os
import csv

# =====================
# Rutas principales
# =====================
class Root:
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    RAW = os.path.join(BASE, "data/raw")
    PROCESSED = os.path.join(BASE, "data/processed")
    PLOTS = os.path.join(BASE, "plots")
    REPORTS = os.path.join(BASE, "reports")


# =====================
# Utilidades de carpetas
# =====================
def ensure_dirs():
    """Crea las carpetas necesarias si no existen."""
    for d in [Root.RAW, Root.PROCESSED, Root.PLOTS, Root.REPORTS]:
        os.makedirs(d, exist_ok=True)


# =====================
# Listar CSVs RAW
# =====================
def list_raw_csvs():
    """Devuelve lista de archivos CSV en data/raw."""
    return [
        os.path.join(Root.RAW, f)
        for f in os.listdir(Root.RAW)
        if f.endswith(".csv")
    ]


# =====================
# Generar nombres de salida
# =====================
def safe_stem(path):
    """Devuelve el nombre del archivo sin extensión."""
    return os.path.splitext(os.path.basename(path))[0]


def make_clean_name(stem, tipo):
    """
    Devuelve el nombre del archivo procesado:
    ejemplo:
       datos_proyectofinal_normal.csv
       datos_proyectofinal_evento.csv
    """
    return f"{stem}_{tipo}.csv"


# =====================
# Lectura de CSV sin pandas
# =====================
def read_csv(filepath):
    """Lee el csv como lista de diccionarios."""
    rows = []
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


# =====================
# Escritura de CSV sin pandas
# =====================
def write_csv(filepath, fieldnames, rows):
    """Escribe una lista de diccionarios en CSV."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
