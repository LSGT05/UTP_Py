import os
import matplotlib.pyplot as plt
from .IO_Utils import Root


def parse_valores(cadena):
    h, t = cadena.split("|")
    return float(h), float(t)


def load_series(filepath):
    """
    Carga listas de humedad y temperatura.
    """
    import csv
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
