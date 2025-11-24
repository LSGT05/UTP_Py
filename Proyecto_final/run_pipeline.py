from src.pipeline import (
    Root, ensure_dirs, list_raw_csvs, make_clean_name, safe_stem,
    clean_file, kpis_volt,
    plot_voltage_line, plot_voltage_hist, plot_boxplot_by_sensor
)
from pathlib import Path
import csv

#CONFIGURACIÓN GENERAL
ROOT = Root(__file__)
DATA_RAW = ROOT / "data" / "raw"
DATA_CLEAN = ROOT / "data" / "processed"
PLOTS = ROOT / "plots"
REPORTS = ROOT / "reports"

ensure_dirs(DATA_CLEAN, PLOTS, REPORTS)

UMBRAL_T = 353.15  # 80°C en Kelvin

#PROCESAR ARCHIVOS CRUDOS
raw_files = list_raw_csvs(DATA_RAW)
if not raw_files:
    print("No se encontraron archivos CSV en data/raw.")
    exit()

all_kpis = []
sensor_data = {}

for raw_path in raw_files:
    clean_name = make_clean_name(raw_path)
    clean_path = DATA_CLEAN / clean_name
    print(f"\nProcesando: {raw_path.name} → {clean_name}")

    ts_list, volts_list, temps_list, stats = clean_file(raw_path, clean_path)
    kpi = kpis_volt(temps_list, umbral=UMBRAL_T)
    kpi.update(stats)
    kpi["archivo"] = raw_path.name
    all_kpis.append(kpi)
    sensor_data[safe_stem(raw_path)] = temps_list

    plot_voltage_line(
        ts_list, temps_list, umbral_v=UMBRAL_T,
        title=f"Temperatura (K) vs Tiempo - {raw_path.stem}",
        out_path=PLOTS / f"{safe_stem(raw_path)}_linea.png"
    )

    plot_voltage_hist(
        temps_list,
        title=f"Histograma Temperatura (K) - {raw_path.stem}",
        out_path=PLOTS / f"{safe_stem(raw_path)}_hist.png"
    )

#BOXPLOT GLOBAL
plot_boxplot_by_sensor(sensor_data, PLOTS / "boxplot_global.png")

#REPORTE
report_path = REPORTS / "kpis_por_archivo.csv"
with report_path.open("w", encoding="utf-8", newline="") as f:
    fieldnames = list(all_kpis[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_kpis)

print(f"\n Pipeline completado con éxito.")
print(f"→ Archivos limpios en: {DATA_CLEAN}")
print(f"→ Gráficos en: {PLOTS}")
print(f"→ Reporte KPI en: {report_path}")
