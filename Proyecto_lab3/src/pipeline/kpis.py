import statistics

def calcular_kpis(datos):
    """Calcula indicadores básicos para un sensor."""
    vals = datos["valor"]
    sensor_id = datos["sensor_id"]
    if len(vals) == 0:
        return {"sensor_id": sensor_id, "n": 0}
    return {
        "sensor_id": sensor_id,
        "n": len(vals),
        "min": min(vals),
        "max": max(vals),
        "promedio": round(statistics.mean(vals), 2),
        "mediana": round(statistics.median(vals), 2),
        "desv_std": round(statistics.stdev(vals), 2) if len(vals) > 1 else 0
    }

def guardar_reporte_kpi(kpi_list, filepath):
    """Guarda los KPIs en un archivo de texto plano."""
    with open(filepath, "w") as f:
        f.write("Reporte de KPIs por sensor\n")
        f.write("="*35 + "\n\n")
        for k in kpi_list:
            for clave, valor in k.items():
                f.write(f"{clave}: {valor}\n")
            f.write("\n")
