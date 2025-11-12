import matplotlib.pyplot as plt
import os

def plot_line(datos, carpeta_salida):
    plt.figure()
    plt.plot(datos["ts"], datos["valor"], label="Valor", linewidth=1)
    plt.plot(datos["ts"], datos["valor_avg"], "--", label="Promedio móvil")
    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Humedad (%)")
    plt.title(f"Evolución del sensor {datos['sensor_id']}")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(carpeta_salida, "line_dht22.png"))
    plt.close()

def plot_hist(datos, carpeta_salida):
    plt.figure()
    plt.hist(datos["valor"], bins=10, edgecolor="black")
    plt.xlabel("Humedad (%)")
    plt.ylabel("Frecuencia")
    plt.title(f"Histograma de valores - Sensor {datos['sensor_id']}")
    plt.grid(True)
    plt.savefig(os.path.join(carpeta_salida, "hist_dht22.png"))
    plt.close()

def plot_box(datos, carpeta_salida):
    plt.figure()
    plt.boxplot(datos["valor"], labels=[datos["sensor_id"]])
    plt.ylabel("Humedad (%)")
    plt.title("Boxplot del sensor DHT22")
    plt.grid(True)
    plt.savefig(os.path.join(carpeta_salida, "boxplot_dht22.png"))
    plt.close()
