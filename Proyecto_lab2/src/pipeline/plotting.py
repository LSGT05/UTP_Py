import matplotlib.pyplot as plt
from pathlib import Path

def plot_voltage_line(ts_list, temps_list, umbral_v, title, out_path: Path):
    """Gráfico de línea Temperatura vs Tiempo."""
    plt.figure()
    plt.plot(ts_list, temps_list, label='Temperatura (K)')
    plt.axhline(umbral_v, color='r', linestyle='--', label=f'Umbral {umbral_v:.2f} K')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Temperatura (K)')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_voltage_hist(temps_list, title, out_path: Path):
    """Histograma de Temperatura."""
    plt.figure()
    plt.hist(temps_list, bins=20, edgecolor='black')
    plt.xlabel('Temperatura (K)')
    plt.ylabel('Frecuencia')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_boxplot_by_sensor(sensor_data: dict, out_path: Path):
    """Boxplot comparativo por sensor."""
    plt.figure()
    plt.boxplot(sensor_data.values(), labels=sensor_data.keys())
    plt.ylabel('Temperatura (K)')
    plt.title('Comparación de Temperatura por Sensor')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
