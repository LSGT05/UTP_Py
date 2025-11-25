import os
from src.pipeline import (
    Root,
    ensure_dirs,
    list_raw_csvs,
    make_clean_name,
    safe_stem,
)
from src.pipeline.cleaning import process_file_separating_hysteresis
from src.pipeline.kpis import compute_kpis
from src.pipeline.plotting import (
    plot_voltage_line,
    plot_voltage_hist,
    plot_voltage_boxplot,
)

# ==========================
# CONFIGURACIÓN DEL PROYECTO
# ==========================

ROOT = Root(
    raw="data/raw",
    processed="data/processed",
    reports="reports",
    plots="plots"
)

ALERT_ON = 70.0   # fuera de histeresis (evento)
ALERT_OFF = 65.0  # volver a normal


# ==========================
# EJECUCIÓN DEL PIPELINE
# ==========================

def main():

    print("\n=== INICIANDO PIPELINE ===\n")

    # 1) Crear carpetas
    ensure_dirs(ROOT)

    # 2) Buscar CSV en /data/raw
    raw_csvs = list_raw_csvs(ROOT.raw)

    if not raw_csvs:
        print("No se encontraron archivos .csv en data/raw/")
        return

    for filepath in raw_csvs:
        filename = os.path.basename(filepath)
        stem = safe_stem(filename)

        print(f"\nProcesando archivo: {filename}")

        # --------------------------
        # 3) Limpiar y dividir datos
        # --------------------------
        out_normal = os.path.join(ROOT.processed, f"{stem}_normal.csv")
        out_evento = os.path.join(ROOT.processed, f"{stem}_evento.csv")

        normal_rows, evento_rows = process_file_separating_hysteresis(
            filepath,
            out_normal,
            out_evento,
            ALERT_ON,
            ALERT_OFF
        )

        print(f"  -> Registros normales: {len(normal_rows)}")
        print(f"  -> Registros evento:   {len(evento_rows)}")

        # --------------------------
        # 4) Generar KPIs
        # --------------------------
        report_file = os.path.join(ROOT.reports, f"{stem}_kpis.txt")
        compute_kpis(normal_rows, evento_rows, report_file)

        print(f"  -> KPIs guardados en: {report_file}")

        # --------------------------
        # 5) Graficar
        # --------------------------
        plot_voltage_line(normal_rows, evento_rows, ROOT.plots, stem)
        plot_voltage_hist(normal_rows, evento_rows, ROOT.plots, stem)
        plot_voltage_boxplot(normal_rows, evento_rows, ROOT.plots, stem)

        print(f"  -> Gráficos guardados en: {ROOT.plots}/")

    print("\n=== PIPELINE COMPLETADO ===\n")


if __name__ == "__main__":
    main()
