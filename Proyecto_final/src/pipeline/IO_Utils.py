import os

# =======================================
#    FUNCION PARA LEER CSV SIN PANDAS
# =======================================

def read_csv_as_dict(csv_path):
    """
    Convierte el CSV en una lista de diccionarios:
    [
        {"timestamp": int, "sensor": str, "voltaje": float, "evento": "0/1"},
        ...
    ]
    """

    rows = []

    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Quitar salto de línea
    lines = [l.strip() for l in lines if l.strip()]

    # Quitar encabezado
    header = lines[0]
    data_lines = lines[1:]

    for line in data_lines:
        parts = line.split(",")

        if len(parts) != 4:
            continue

        timestamp = parts[0]
        sensor_id = parts[1]
        valores = parts[2]
        estado_txt = parts[3]

        # valores = "77.5|36.3"
        volt_txt, temp_txt = valores.split("|")

        volt = float(volt_txt)

        evento = "1" if estado_txt == "ALERT" else "0"

        rows.append({
            "timestamp": timestamp,
            "sensor": sensor_id,
            "voltaje": volt,
            "evento": evento
        })

    return rows
