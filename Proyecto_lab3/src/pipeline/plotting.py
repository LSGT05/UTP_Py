import matplotlib.pyplot as plt
import os

def plot_line(datos, carpeta_salida):
    plt.figure()
    plt.plot(datos["ts"], datos["valor"], label="valor", linewidth=1)
    plt.plot(datos["ts"], datos["valor_avg"], "--", label="promedio")
    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Valor")
    plt.title(f"Evolución Sensor {datos['sensor_id']}")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(carpeta_salida, f"line_{datos['sensor_id']}.png"))
    plt.close()

def plot_hist(datos, carpeta_salida):
    plt.figure()
    plt.hist(datos["valor"], bins=10, edgecolor="black")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.title(f"Histograma Sensor {datos['sensor_id']}")
    plt.grid(True)
    plt.savefig(os.path.join(carpeta_salida, f"hist_{datos['sensor_id']}.png"))
    plt.close()

def plot_boxplot(lista_datos, carpeta_salida):
    etiquetas = [d["sensor_id"] for d in lista_datos]
    valores = [d["valor"] for d in lista_datos]
    plt.figure()
    plt.boxplot(valores, labels=etiquetas)
    plt.ylabel("Valor")
    plt.title("Boxplot comparativo por sensor")
    plt.grid(True)
    plt.savefig(os.path.join(carpeta_salida, "boxplot_comparativo.png"))
    plt.close()
