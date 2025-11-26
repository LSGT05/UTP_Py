from src.pipeline import (
    read_csv_as_dict,
    kpis_volt,
    save_kpis_txt,
    plot_normal_vs_event,
    plot_time_series,
    plot_histograma,
    plot_boxplot
)

CSV_PATH = "Proyecto_final/data/raw/datos_proyectofinal.csv"

# Leer datos
rows = read_csv_as_dict(CSV_PATH)

# KPIs
kpis = kpis_volt(rows)
save_kpis_txt(kpis)

# Gráficas
plot_normal_vs_event(rows)
plot_time_series(rows)
plot_histograma(rows)
plot_boxplot(rows)

print("\n[OK] Todas las gráficas generadas y KPIs guardados.\n")
