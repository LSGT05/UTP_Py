import csv

def leer_csv(filepath):
    """Lee un CSV con formato ts_ms,sensor_id,valor,valor_avg,estado"""
    ts, vals, vals_avg, estados = [], [], [], []
    sensor_id = None
    with open(filepath, "r") as f:
        lector = csv.reader(f)
        next(lector)  # saltar encabezado
        for fila in lector:
            if len(fila) < 5:
                continue
            ts.append(int(fila[0]))
            sensor_id = fila[1]
            vals.append(float(fila[2]))
            vals_avg.append(float(fila[3]))
            estados.append(fila[4])
    return {
        "sensor_id": sensor_id,
        "ts": ts,
        "valor": vals,
        "valor_avg": vals_avg,
        "estado": estados
    }
