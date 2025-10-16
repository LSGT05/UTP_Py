import csv
import statistics
from pathlib import Path

def calcular_kpis(nombre_archivo, ts, volts, temps, stats, out_path: Path):
    if not temps:
        return

    kpis = {
        "archivo": nombre_archivo,
        "lecturas_validas": len(temps),
        "voltaje_promedio": round(statistics.mean(volts), 3),
        "temperatura_promedio_K": round(statistics.mean(temps), 2),
        "temperatura_max_K": round(max(temps), 2),
        "temperatura_min_K": round(min(temps), 2),
        **stats
    }

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=kpis.keys())
        writer.writeheader()
        writer.writerow(kpis)
