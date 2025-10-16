from statistics import mean

def kpis_temp(temps, umbral=310.0):
    """
    Calcula los KPIs de temperatura (en Kelvin):
      - n: cantidad de datos válidos
      - min: temperatura mínima
      - max: temperatura máxima
      - prom: promedio
      - alerts: cantidad de lecturas sobre el umbral
      - alerts_pct: porcentaje de alertas
    """
    temps = [float(v) for v in temps if v is not None]
    n = len(temps)
    if n == 0:
        return {
            "n": 0,
            "min": None,
            "max": None,
            "prom": None,
            "alerts": 0,
            "alerts_pct": 0.0
        }

    alerts = sum(v > umbral for v in temps)
    return {
        "n": n,
        "min": min(temps),
        "max": max(temps),
        "prom": mean(temps),
        "alerts": alerts,
        "alerts_pct": round(100.0 * alerts / n, 2)
    }
