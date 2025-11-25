import os
from .IO_Utils import Root, safe_stem


def parse_valores(cadena):
    """Recibe cadena 'humedad|temperatura' -> retorna dos floats."""
    h, t = cadena.split("|")
    return float(h), float(t)


def kpis_volt(filepath):
    """
    Calcula KPIs sobre los valores del CSV (humedad y temperatura).
    No usa pandas.
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


def save_kpis_txt(kpi_dict, filepath, etiqueta):
    """
    Guarda los KPIs en un archivo TXT dentro de /reports.
    """
    filename = f"kpis_{safe_stem(filepath)}_{etiqueta}.txt"
    fullpath = os.path.join(Root.REPORTS, filename)

    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(f"KPIs del archivo procesado: {filepath}\n")
        f.write(f"Tipo de datos: {etiqueta}\n\n")

        for k, v in kpi_dict.items():
            f.write(f"{k}: {v}\n")

    return fullpath
