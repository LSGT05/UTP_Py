from src.pipeline import (
    ensure_dirs,
    list_raw_csvs,
    clean_file,
    kpis_volt,
    plot_voltage_line,
    plot_voltage_hist,
    plot_boxplot_by_sensor,
)


def main():
    ensure_dirs()

    raw_files = list_raw_csvs()
    if not raw_files:
        print("No hay CSVs en data/raw")
        return

    for f in raw_files:
        print(f"\nProcesando: {f}")

        normal_path, evento_path = clean_file(f)

        print(" -> Normal:", normal_path)
        print(" -> Evento:", evento_path)

        # KPIs
        print("KPIs Normal:", kpis_volt(normal_path))
        print("KPIs Evento:", kpis_volt(evento_path))

        # Gráficas
        plot_voltage_line(normal_path, "normal")
        plot_voltage_hist(normal_path, "normal")
        plot_boxplot_by_sensor(normal_path, "normal")

        plot_voltage_line(evento_path, "evento")
        plot_voltage_hist(evento_path, "evento")
        plot_boxplot_by_sensor(evento_path, "evento")

    print("\nPipeline completado.")


if __name__ == "__main__":
    main()
