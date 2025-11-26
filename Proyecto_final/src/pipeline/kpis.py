import os
import matplotlib.pyplot as plt

# =======================================
#   CÁLCULO DE KPIs
# =======================================

def kpis_volt(rows):
    """
    rows = lista de diccionarios:
    [{'timestamp': '...', 'voltaje': float, 'evento': '0/1'}, ...]
    """

    if not rows:
        return None

    voltajes = [r["voltaje"] for r in rows]

    normales = [r["voltaje"] for r in rows if r["evento"] == "0"]
    eventos = [r["voltaje"] for r in rows if r["evento"] == "1"]

    kpis = {
        "min": min(voltajes),
        "max": max(voltajes),
        "promedio": sum(voltajes) / len(voltajes),
        "conteo_total": len(voltajes),
        "normales": len(normales),
        "eventos": len(eventos),
    }

    return kpis


# =======================================
#   GUARDAR KPIs EN TXT
# =======================================

def save_kpis_txt(kpis, reports_folder="reports", filename="kpis_resultados.txt"):

    os.makedirs(reports_folder, exist_ok=True)
    filepath = os.path.join(reports_folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        for key, value in kpis.items():
            f.write(f"{key}: {value}\n")

    print(f"[OK] KPIs guardados en {filepath}")


# =======================================
#   GRAFICAS
# =======================================

def plot_normal_vs_event(rows, plots_folder="plots"):
    os.makedirs(plots_folder, exist_ok=True)

    normales = [r["voltaje"] for r in rows if r["evento"] == "0"]
    eventos = [r["voltaje"] for r in rows if r["evento"] == "1"]

    plt.figure(figsize=(8, 5))
    plt.hist(normales, alpha=0.7, label="Normal")
    plt.hist(eventos, alpha=0.7, label="Evento")
    plt.title("Distribución Voltaje: Normales vs Eventos")
    plt.xlabel("Voltaje (V)")
    plt.ylabel("Frecuencia")
    plt.legend()

    output_path = os.path.join(plots_folder, "normal_vs_evento.png")
    plt.savefig(output_path)
    plt.close()

    print(f"[OK] Imagen generada: {output_path}")


def plot_time_series(rows, plots_folder="plots"):
    os.makedirs(plots_folder, exist_ok=True)

    x = [int(r["timestamp"]) for r in rows]
    y = [r["voltaje"] for r in rows]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker="o", linestyle="-")
    plt.title("Voltaje en el Tiempo")
    plt.xlabel("timestamp (ms)")
    plt.ylabel("Voltaje (V)")

    out = os.path.join(plots_folder, "time_series.png")
    plt.savefig(out)
    plt.close()

    print(f"[OK] Imagen generada: {out}")


def plot_histograma(rows, plots_folder="plots"):
    os.makedirs(plots_folder, exist_ok=True)

    voltajes = [r["voltaje"] for r in rows]

    plt.figure(figsize=(8, 5))
    plt.hist(voltajes, bins=10)
    plt.title("Histograma del Voltaje")
    plt.xlabel("Voltaje (V)")
    plt.ylabel("Frecuencia")

    out = os.path.join(plots_folder, "histograma.png")
    plt.savefig(out)
    plt.close()

    print(f"[OK] Imagen generada: {out}")


def plot_boxplot(rows, plots_folder="plots"):
    os.makedirs(plots_folder, exist_ok=True)

    voltajes = [r["voltaje"] for r in rows]

    plt.figure(figsize=(6, 6))
    plt.boxplot(voltajes, vert=True)
    plt.title("Boxplot del Voltaje")
    plt.ylabel("Voltaje (V)")

    out = os.path.join(plots_folder, "boxplot.png")
    plt.savefig(out)
    plt.close()

    print(f"[OK] Imagen generada: {out}")
