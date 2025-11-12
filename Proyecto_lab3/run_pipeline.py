import os
from src.pipeline.IO_Utils import leer_csv, obtener_archivos_csv
from src.pipeline.kpis import calcular_kpis, guardar_reporte_kpi
from src.pipeline.plotting import plot_line, plot_hist, plot_boxplot

# --- Configuración de rutas ---
DATA_DIR = "data/raw"
PLOTS_DIR = "plots"
REPORTS_DIR = "reports"

os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# --- Leer datos ---
archivos = obtener_archivos_csv(DATA_DIR)
datos_sensores = []
kpi_list = []

for archivo in archivos:
    datos = leer_csv(archivo)
    datos_sensores.append(datos)
    kpi = calcular_kpis(datos)
    kpi_list.append(kpi)
    plot_line(datos, PLOTS_DIR)
    plot_hist(datos, PLOTS_DIR)

# --- Graficar boxplot comparativo ---
if len(datos_sensores) > 1:
    plot_boxplot(datos_sensores, PLOTS_DIR)

# --- Guardar KPIs ---
guardar_reporte_kpi(kpi_list, os.path.join(REPORTS_DIR, "reporte_kpis.txt"))

print("✅ Pipeline completado con éxito.")
print(f"📊 Gráficos en '{PLOTS_DIR}' y reporte en '{REPORTS_DIR}'.")
