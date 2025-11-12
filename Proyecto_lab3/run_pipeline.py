import os
from src.pipeline.IO_Utils import leer_csv
from src.pipeline.kpis import calcular_kpis, guardar_reporte_kpi
from src.pipeline.plotting import plot_line, plot_hist, plot_box

# --- Configuración de rutas ---
DATA_PATH = "Proyecto_lab3/data/raw/datos_dht22.csv"
PLOTS_DIR = "Proyecto_lab3/plots"
REPORTS_DIR = "Proyecto_lab3/reports"

os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# --- Leer datos ---
datos = leer_csv(DATA_PATH)

# --- Calcular KPIs ---
kpi = calcular_kpis(datos)

# --- Generar gráficos ---
plot_line(datos, PLOTS_DIR)
plot_hist(datos, PLOTS_DIR)
plot_box(datos, PLOTS_DIR)

# --- Guardar reporte ---
reporte_path = os.path.join(REPORTS_DIR, "reporte_kpis.txt")
guardar_reporte_kpi(kpi, reporte_path)

print("✅ Pipeline completado con éxito.")
print(f"📊 Gráficos guardados en: {PLOTS_DIR}/")
print(f"📄 Reporte generado en: {reporte_path}")
