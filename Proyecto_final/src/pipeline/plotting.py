import os
import matplotlib.pyplot as plt


def extract_series(rows):
    """Extrae series separadas (ts, humedad, temperatura)."""
    ts = [r[0] for r in rows]
    h = [r[2] for r in rows]
    t = [r[3] for r in rows]
    return ts, h, t


# ======================================
#     GRAFICA DE LÍNEA
# ======================================

def plot_voltage_line(normal, evento, out_dir, stem):
    ts_n, h_n, _ = extract_series(normal)
    ts_e, h_e, _ = extract_series(evento)

    plt.figure(figsize=(10, 4))
    if ts_n:
        plt.plot(ts_n, h_n, label="Normal")
    if ts_e:
        plt.plot(ts_e, h_e, label="Evento")

    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Humedad")
    plt.title("Humedad vs Tiempo")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(out_dir, f"{stem}_line.png"))
    plt.close()


# ======================================
#     HISTOGRAMA
# ======================================

def plot_voltage_hist(normal, evento, out_dir, stem):
    _, h_n, _ = extract_series(normal)
    _, h_e, _ = extract_series(evento)

    plt.figure(figsize=(8, 4))

    if h_n:
        plt.hist(h_n, bins=20, alpha=0.6, label="Normal")
    if h_e:
        plt.hist(h_e, bins=20, alpha=0.6, label="Evento")

    plt.xlabel("Humedad")
    plt.ylabel("Frecuencia")
    plt.title("Histograma de Humedad")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(out_dir, f"{stem}_hist.png"))
    plt.close()


# ======================================
#     BOX PLOT
# ======================================

def plot_voltage_boxplot(normal, evento, out_dir, stem):
    _, h_n, _ = extract_series(normal)
    _, h_e, _ = extract_series(evento)

    data = []
    labels = []

    if h_n:
        data.append(h_n)
        labels.append("Normal")

    if h_e:
        data.append(h_e)
        labels.append("Evento")

    if not data:
        return

    plt.figure(figsize=(6, 4))
    plt.boxplot(data, labels=labels)
    plt.title("Boxplot de Humedad")
    plt.tight_layout()

    plt.savefig(os.path.join(out_dir, f"{stem}_boxplot.png"))
    plt.close()
