import os
import matplotlib.pyplot as plt
import pandas as pd
import csv
from .IO_Utils import Root


def parse_valores(cadena):
    h, t = cadena.split("|")
    return float(h), float(t)


def load_series(filepath):
    """Carga listas de humedad y temperatura."""
    hum = []
    temp = []
    ts = []

    with open(filepath, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            h, t = parse_valores(row["valor(s)"])
            hum.append(h)
            temp.append(t)
            ts.append(int(row["ts_ms"]))

    return ts, hum, temp


# ---------------- LINE PLOT ----------------

def plot_voltage_line(filepath, label):
    ts, hum, temp = load_series(filepath)

    plt.figure()
    plt.plot(ts, hum, label="Humedad")
    plt.plot(ts, temp, label="Temperatura")
    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Valores")
    plt.title(f"Serie de tiempo ({label})")
    plt.legend()
    plt.grid(True)

    out = os.path.join(Root.PLOTS, f"{label}_line.png")
    plt.savefig(out, dpi=150)
    plt.close()


# ---------------- HISTOGRAM ----------------

def plot_voltage_hist(filepath, label):
    _, hum, temp = load_series(filepath)

    plt.figure()
    plt.hist(hum, alpha=0.6, label="Humedad")
    plt.hist(temp, alpha=0.6, label="Temperatura")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.title(f"Histograma ({label})")
    plt.legend()

    out = os.path.join(Root.PLOTS, f"{label}_hist.png")
    plt.savefig(out, dpi=150)
    plt.close()


# ---------------- BOX PLOT ----------------

def plot_boxplot_by_sensor(filepath, label):
    _, hum, temp = load_series(filepath)

    plt.figure()
    plt.boxplot([hum, temp], labels=["Humedad", "Temperatura"])
    plt.title(f"Boxplot ({label})")

    out = os.path.join(Root.PLOTS, f"{label}_box.png")
    plt.savefig(out, dpi=150)
    plt.close()


# ---------------- COMPARACIÓN NORMAL VS EVENTO ----------------

def plot_compare_normal_evento(normal_path, evento_path):
    """Gráfico comparando Humedad y Temperatura entre Normal y Evento."""
    
    ts_n, hum_n, temp_n = load_series(normal_path)
    ts_e, hum_e, temp_e = load_series(evento_path)

    plt.figure(figsize=(12, 6))
    plt.plot(ts_n, hum_n, label="Humedad - Normal", linewidth=1.2)
    plt.plot(ts_e, hum_e, label="Humedad - Evento", linewidth=1.2)
    plt.plot(ts_n, temp_n, label="Temperatura - Normal", linewidth=1.2)
    plt.plot(ts_e, temp_e, label="Temperatura - Evento", linewidth=1.2)

    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Valores")
    plt.title("Comparación: Normal vs Evento")
    plt.legend()
    plt.grid(True)

    out = os.path.join(Root.PLOTS, "comparacion_normal_evento.png")
    plt.savefig(out, dpi=150)
    plt.close()

    return out
