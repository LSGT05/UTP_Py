import matplotlib.pyplot as plt
from pathlib import Path

def generar_graficos(nombre_archivo, ts, volts, temps, out_dir: Path):
    if not temps:
        return

    plt.figure()
    plt.plot(ts, temps)
    plt.title(f"Temperatura (K) - {nombre_archivo}")
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura (K)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_dir / f"{nombre_archivo}_linea.png")
    plt.close()

    plt.figure()
    plt.hist(temps, bins=20)
    plt.title(f"Histograma de Temperatura (K) - {nombre_archivo}")
    plt.xlabel("Temperatura (K)")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_dir / f"{nombre_archivo}_hist.png")
    plt.close()
