import csv
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# === ENRUTAMIENTO ===
ROOT = Path(__file__).resolve().parents[1]  # Carpeta principal
DATA_DIR = ROOT / "Proyecto_lab" / "DATA" / "PROCESSED"
FILENAME = "Temperaturas_Procesado.csv"
CSV_PATH = DATA_DIR / FILENAME

print(f"Archivo de entrada: {CSV_PATH}")
if not CSV_PATH.exists():
    raise FileNotFoundError(f"No existe el archivo: {CSV_PATH}")

# Carpeta de salida: sesion8/plots
PLOTS_DIR = ROOT/"sesion8"/"plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# === CONFIGURACIONES ===
Umbral_T = 30.0  # umbral de temperatura (°C)

# === FUNCIÓN PARA DETECTAR DELIMITADOR ===
def detectar_delimitador(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        head = f.readline()
    return ";" if head.count(";") > head.count(",") else ","

# === FUNCIÓN PARA PARSEAR TIMESTAMP ===
def parse_ts(s: str):
    """Convierte texto en datetime, aceptando múltiples formatos."""
    if not s:
        return None
    s = s.strip()
    formatos = [
        "%Y-%m-%dT%H:%M:%S",  # 2025-09-01T10:00:04
        "%d/%m/%Y %H:%M:%S",  # 01/09/2025 10:00:05
        "%Y-%m-%d %H:%M:%S",  # 2025-09-01 10:00:05
        "%d-%m-%Y %H:%M:%S",  # 01-09-2025 10:00:05
    ]
    for fmt in formatos:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

# === LECTURA DEL CSV ===
Tiempo, Voltaje, Temp_C, Alertas = [], [], [], []
delim = detectar_delimitador(CSV_PATH)

with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f, delimiter=delim)
    for row in reader:
        try:
            t = parse_ts(row["Timestamp"])
            if t is None:
                continue
            v = float(str(row["Voltaje"]).replace(",", "."))
            T = float(str(row["Temp_C"]).replace(",", "."))
            alerta = str(row.get("Alertas", "")).strip().upper()
        except Exception:
            continue

        Tiempo.append(t)
        Voltaje.append(v)
        Temp_C.append(T)
        Alertas.append(alerta)

if not Tiempo:
    raise RuntimeError("No se pudieron leer datos válidos del archivo CSV.")
print(f"Filas válidas leídas: {len(Tiempo)}")

# === GRAFICO 1: TEMPERATURA VS TIEMPO ===
alerta_t = [t for t, a in zip(Tiempo, Alertas) if a == "ALERTA"]
alerta_T = [T for T, a in zip(Temp_C, Alertas) if a == "ALERTA"]

plt.figure(figsize=(9, 4))
plt.plot(Tiempo, Temp_C, color="#0057b7", label="Temperatura (°C)")
plt.scatter(alerta_t, alerta_T, color="#ff3b3b", label="ALERTA (> Umbral)")
plt.axhline(Umbral_T, color="orange", linestyle="--", label=f"Umbral {Umbral_T} °C")

plt.title(f"TEMPERATURA vs TIEMPO — {CSV_PATH.stem}".upper(), fontweight='bold')
plt.xlabel("Tiempo")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.tight_layout()
out1 = PLOTS_DIR / f"temp_line_{CSV_PATH.stem}.png"
plt.savefig(out1, dpi=200)
plt.show()
print("Guardado:", out1)

# === GRAFICO 2: VOLTAJE VS TEMPERATURA ===
alerta_v = [v for v, a in zip(Voltaje, Alertas) if a == "ALERTA"]
alerta_T2 = [T for T, a in zip(Temp_C, Alertas) if a == "ALERTA"]

plt.figure(figsize=(7, 4))
plt.scatter(Temp_C, Voltaje, color="#2ca02c", alpha=0.7, label="Datos normales")
plt.scatter(alerta_T2, alerta_v, color="#ff3b3b", label="ALERTAS")
plt.title(f"VOLTAJE vs TEMPERATURA — {CSV_PATH.stem}".upper(), fontweight='bold')
plt.xlabel("Temperatura (°C)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.legend()
plt.tight_layout()
out2 = PLOTS_DIR / f"volt_vs_temp_{CSV_PATH.stem}.png"
plt.savefig(out2, dpi=200)
plt.show()
print("Guardado:", out2)

# === GRAFICO 3: HISTOGRAMA DE TEMPERATURA ===
plt.figure(figsize=(6, 4))
plt.hist(Temp_C, bins=25, color="#4287f5", alpha=0.8)
plt.title(f"HISTOGRAMA DE TEMPERATURA — {CSV_PATH.stem}".upper(), fontweight='bold')
plt.xlabel("Temperatura (°C)")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.tight_layout()
out3 = PLOTS_DIR / f"temp_hist_{CSV_PATH.stem}.png"
plt.savefig(out3, dpi=200)
plt.show()
print("Guardado:", out3)

# === GRAFICO 4: BOX PLOT DE TEMPERATURA ===
plt.figure(figsize=(4, 5))
plt.boxplot(Temp_C, vert=True, showmeans=True, meanline=True)
plt.title(f"BOXPLOT DE TEMPERATURA — {CSV_PATH.stem}".upper(), fontweight='bold')
plt.ylabel("Temperatura (°C)")
plt.grid(True)
plt.tight_layout()
out4 = PLOTS_DIR / f"temp_box_{CSV_PATH.stem}.png"
plt.savefig(out4, dpi=200)
plt.show()
print("Guardado:", out4)
