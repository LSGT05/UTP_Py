import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def plot_temperature_line(ts, temps, umbral_k: float, title: str, out_path: Path):
    """
    Genera un gráfico de línea de temperatura en Kelvin con umbral de alerta.
    """
    plt.figure(figsize=(9, 4))
    plt.plot(ts, temps, label="Temperatura (K)", color="tab:blue")
    
    # Puntos de alerta si superan el umbral
    alerts_t = [t for t, temp in zip(ts, temps) if temp > umbral_k]
    alerts_v = [temp for temp in temps if temp > umbral_k]
    if alerts_t:
        plt.scatter(alerts_t, alerts_v, label=f"Alertas (> {umbral_k:.2f} K)", color="red")
    plt.axhline(umbral_k, linestyle="--", label=f"Umbral {umbral_k:.2f} K", color="orange")
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.title(title)
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura (K)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.show()


def plot_temperature_hist(temps, title: str, out_path: Path, bins: int = 20):
    """
    Genera un histograma de temperaturas (K).
    """
    plt.figure(figsize=(6, 4))
    plt.hist(temps, bins=bins, color="tab:green", edgecolor="black")
    plt.title(title)
    plt.xlabel("Temperatura (K)")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.tight_layout()
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.show()


def plot_boxplot_by_sensor(sensor_to_temps: dict[str, list[float]], out_path: Path):
    """
    Genera un boxplot comparativo de temperatura (K) por sensor.
    """
    labels = list(sensor_to_temps.keys())
    data = [sensor_to_temps[k] for k in labels if sensor_to_temps[k]]
    if not data:
        raise RuntimeError("No hay datos para boxplot.")
    
    horizontal = len(labels) > 10
    plt.figure(figsize=(max(8, len(labels)*0.8) if not horizontal else 8,
                        5 if not horizontal else max(6, len(labels)*0.6)))
    plt.boxplot(data, vert=not horizontal, showmeans=True, patch_artist=True,
                boxprops=dict(facecolor="lightblue", color="navy"),
                medianprops=dict(color="red"))
    
    if horizontal:
        plt.yticks(range(1, len(labels)+1), labels)
        plt.xlabel("Temperatura (K)")
        plt.ylabel("Sensor")
    else:
        plt.xticks(range(1, len(labels)+1), labels, rotation=60)
        plt.ylabel("Temperatura (K)")
        plt.xlabel("Sensor")
    
    plt.title("Boxplot de Temperatura por Sensor")
    plt.grid(True, axis="y" if not horizontal else "x")
    plt.tight_layout()
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.show()
