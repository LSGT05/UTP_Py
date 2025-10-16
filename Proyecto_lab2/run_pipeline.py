import csv
from pathlib import Path
from src.pipeline.cleaning import clean_file
from Proyecto_lab2.src.pipeline.kpis import kpis_volt
from src.pipeline.plotting import (
    plot_voltage_line,
    plot_voltage_hist,
    plot_boxplot_by_sensor
)
from src.pipeline.IO_Utils import (
    ensure_dirs,
    list_raw_csvs,
    make_clean_name,
    safe_stem
)

# ==============================
# CONFIGURACIÓN DE RUTAS
# ==============================
ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "clean"
PLOTS_DIR = ROOT / "plots"
REPORTS_DIR = ROOT / "reports"

ensure_dirs(CLEAN_DIR, PLOTS_DIR, REPORTS_DIR)

# ==============================
# PARÁMETROS DE CALIBRACIÓN
# ==============================
CAL_V1, CAL_T1 = 0.4, -30 + 273.15   # (0.4V → 243.15K)
CAL_V2, CAL_T2 = 5.6, 120 + 273.15   # (5.6V → 393.15K)
UMBRAL_TEMP_K = 353.15               # 80°C en Kelvin

def voltaje_a_tempK(v: float) -> float:
    """Transforma voltaje (V) a temperatura (K) usando interpolación lineal."""
    return CAL_T1 + (CAL_T2 - CAL_T1) * (v - CAL_V1) / (CAL_V2 - CAL_V1)

# ==============================
# PROCESAMIENTO DE ARCHIVOS
# ==============================
raw_files = list_raw_csvs(RAW_DIR)
if not raw_files:
    print(" No se encontraron archivos en data/raw/")
    exit()

all_kpis = []
sensor_to_temp = {}

for raw_path in raw_files:
    print(f"\n Procesando: {raw_path.name}")
    clean_path = CLEAN_DIR / make_clean_name(raw_path)

    # Limpieza
    ts_list, volts_list, _, stats = clean_file(
        in_path=raw_path,
        out_path=clean_path,
        ts_col="timestamp",
        v_col_candidates=("value", "voltaje", "voltage_V")
    )

    if not volts_list:
        print(f" {raw_path.name}: sin datos válidos, omitido.")
        continue

    # Conversión voltaje → temperatura (K)
    temps_K = [voltaje_a_tempK(v) for v in volts_list]

    # Guardar archivo limpio (temperatura en Kelvin)
    with clean_path.open("w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout)
        writer.writerow(["timestamp", "voltage_V", "temperature_K"])
        for t, v, tk in zip(ts_list, volts_list, temps_K):
            writer.writerow([t.strftime("%Y-%m-%dT%H:%M:%S"), f"{v:.3f}", f"{tk:.3f}"])

    # KPIs
    kpis = kpis_volt(temps_K, umbral=UMBRAL_TEMP_K)
    kpis.update(stats)
    kpis["archivo"] = raw_path.name
    all_kpis.append(kpis)

    # Gráficos individuales
    sensor_name = safe_stem(raw_path)
    plot_voltage_line(ts_list, temps_K, UMBRAL_TEMP_K,
                      f"Temperatura (K) - {sensor_name}",
                      PLOTS_DIR / f"{sensor_name}_line.png")
    plot_voltage_hist(temps_K, f"Histograma Temperatura (K) - {sensor_name}",
                      PLOTS_DIR / f"{sensor_name}_hist.png")

    # Datos para boxplot global
    sensor_to_temp[sensor_name] = temps_K

# ==============================
# BOX PLOT GLOBAL
# ==============================
if sensor_to_temp:
    plot_boxplot_by_sensor(sensor_to_temp, PLOTS_DIR / "boxplot_temperaturas.png")

# ==============================
# REPORTE DE KPIs
# ==============================
if all_kpis:
    report_path = REPORTS_DIR / "kpis_por_archivo.csv"
    with report_path.open("w", encoding="utf-8", newline="") as fout:
        fieldnames = list(all_kpis[0].keys())
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_kpis)

    print("\n Pipeline completado correctamente.")
    print(f" Reporte KPIs: {report_path}")
else:
    print("\n No se generaron KPIs (posibles datos inválidos).")
