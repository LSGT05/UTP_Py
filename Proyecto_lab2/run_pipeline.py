from pathlib import Path
from src.pipeline.cleaning import clean_file
from src.pipeline.kpi import calcular_kpis
from src.pipeline.plotting import generar_graficos


def run_pipeline():
    RAW_DIR = Path("data/raw")
    CLEAN_DIR = Path("data/clean")
    KPI_DIR = Path("reports")
    PLOT_DIR = Path("plots")

    for d in [CLEAN_DIR, KPI_DIR, PLOT_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    print("=== Iniciando pipeline voltaje → temperatura (K) ===")

    for file in RAW_DIR.glob("*.csv"):
        print(f"\nProcesando: {file.name}")
        clean_path = CLEAN_DIR / file.name

        ts, volts, temps, stats = clean_file(file, clean_path)
        print(f"   Filas válidas: {stats['filas_validas']} / {stats['filas_totales']}")

        kpi_path = KPI_DIR / f"kpi_{file.stem}.csv"
        calcular_kpis(file.name, ts, volts, temps, stats, kpi_path)
        print(f"   KPIs guardados en {kpi_path.name}")

        generar_graficos(file.name, ts, volts, temps, PLOT_DIR)
        print("   Gráficos generados ✓")

    print("\n=== Pipeline finalizado correctamente ===")


if __name__ == "__main__":
    run_pipeline()
