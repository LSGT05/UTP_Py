import os

# =====================================================
# Clase Root: agrupa todas las rutas del proyecto
# =====================================================

class Root:
    def __init__(self, raw, processed, reports, plots):
        self.raw = raw
        self.processed = processed
        self.reports = reports
        self.plots = plots


# =====================================================
# Crear carpetas necesarias
# =====================================================

def ensure_dirs(root: Root):
    os.makedirs(root.raw, exist_ok=True)
    os.makedirs(root.processed, exist_ok=True)
    os.makedirs(root.reports, exist_ok=True)
    os.makedirs(root.plots, exist_ok=True)


# =====================================================
# Listar archivos CSV en /data/raw
# =====================================================

def list_raw_csvs(raw_dir):
    files = []
    for fname in os.listdir(raw_dir):
        if fname.lower().endswith(".csv"):
            files.append(os.path.join(raw_dir, fname))
    return files


# =====================================================
# Limpiar nombre
# =====================================================

def make_clean_name(text: str):
    """
    Reemplaza espacios por guiones bajos y convierte a minúsculas.
    """
    return text.replace(" ", "_").lower()


# =====================================================
# Obtener nombre base del archivo (sin extensión)
# =====================================================

def safe_stem(filename: str):
    """
    Extrae el nombre sin extensión.
    Ejemplo:
    safe_stem("datos_proyectofinal.csv") -> "datos_proyectofinal"
    """
    return os.path.splitext(filename)[0]
