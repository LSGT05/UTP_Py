def parse_valores(cadena):
    h, t = cadena.split("|")
    return float(h), float(t)


def kpis_volt(filepath):
    """
    KPIs simples sobre humedad y temperatura.
    """
    import csv

    humid_values = []
    temp_values = []

    with open(filepath, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            h, t = parse_valores(row["valor(s)"])
            humid_values.append(h)
            temp_values.append(t)

    if not humid_values:
        return {"error": "archivo vacío"}

    return {
        "humedad_min": min(humid_values),
        "humedad_max": max(humid_values),
        "humedad_prom": sum(humid_values) / len(humid_values),

        "temp_min": min(temp_values),
        "temp_max": max(temp_values),
        "temp_prom": sum(temp_values) / len(temp_values),
    }
