from src.pipeline import (
    ensure_dirs,
    list_raw_csvs,
    clean_file,
    kpis_volt,
    save_kpis_txt,
    plot_voltage_line,
    plot_voltage_hist,
    plot_boxplot_by_sensor,
    plot_compare_normal_evento,
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

        # =======================
        #    KPIs Normal
        # =======================
        kpi_normal = kpis_volt(normal_path)
        txt_normal = save_kpis_txt(kpi_normal, normal_path, "normal")
        print("KPIs Normal guardados en:", txt_normal)

        # =======================
        #    KPIs Evento
        # =======================
        kpi_evento = kpis_volt(evento_path)
        txt_evento = save_kpis_txt(kpi_evento, evento_path, "evento")
        print("KPIs Evento guardados en:", txt_evento)

        # =======================
        #    GRÁFICOS
        # =======================
        plot_voltage_line(normal_path, "normal")
        plot_voltage_hist(normal_path, "normal")
        plot_boxplot_by_sensor(normal_path, "normal")

        plot_voltage_line(evento_path, "evento")
        plot_voltage_hist(evento_path, "evento")
        plot_boxplot_by_sensor(evento_path, "evento")

        # =======================
        #    GRÁFICO COMPARATIVO
        # =======================
        compare_img = plot_compare_normal_evento(normal_path, evento_path)
        print("Gráfico comparativo guardado en:", compare_img)

    print("\nPipeline completado.")


if __name__ == "__main__":
    main()
