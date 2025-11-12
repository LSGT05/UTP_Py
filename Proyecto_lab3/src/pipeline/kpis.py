import statistics

def calcular_kpis(datos):
    """Calcula KPIs básicos de un conjunto de mediciones."""
    vals = datos["valor"]
    sid = datos["sensor_id"]
    if not vals:
        return {"sensor_id": sid, "n": 0}
    return {
        "sensor_id": sid,
        "n": len(vals),
        "min": min(vals),
        "max": max(vals),
        "promedio": round(statistics.mean(vals), 2),
        "mediana": round(statistics.median(vals), 2),
        "desv_std": round(statistics.stdev(vals), 2) if len(vals) > 1 else 0
    }

def guardar_reporte_kpi(kpi, filepath):
    """Guarda un diccionario de KPIs en un archivo de texto."""
    with open(filepath, "w") as f:
        f.write("Reporte de KPIs del sensor DHT22\n")
        f.write("="*40 + "\n\n")
        for k, v in kpi.items():
            f.write(f"{k}: {v}\n")
