def parse_row(line):
    """
    Convierte una línea:
    ts_ms,sensor_id,valor(s),estado
    en una tupla usable.
    """
    parts = line.strip().split(",")
    if len(parts) != 4:
        return None

    ts = int(parts[0])
    sensor = parts[1]
    vals = parts[2].split("|")

    try:
        h = float(vals[0])  # humedad
        t = float(vals[1])  # temperatura
    except:
        return None

    estado_label = parts[3]

    return (ts, sensor, h, t, estado_label)


def write_rows(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("ts_ms,sensor_id,humedad,temperatura,estado\n")
        for r in rows:
            f.write(f"{r[0]},{r[1]},{r[2]},{r[3]},{r[4]}\n")


def process_file_separating_hysteresis(infile, out_normal, out_evento, alert_on, alert_off):
    """
    Separa en normal / evento usando histeresis.
    Sin pandas.
    """

    with open(infile, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header = True
    normal_rows = []
    evento_rows = []

    estado_actual = "OK"

    for line in lines:
        if header:
            header = False
            continue

        row = parse_row(line)
        if not row:
            continue

        ts, sensor, h, t, old_state = row

        # --- Lógica de histeresis ---
        if estado_actual == "OK" and h >= alert_on:
            estado_actual = "ALERT"
        elif estado_actual == "ALERT" and h <= alert_off:
            estado_actual = "OK"

        new_row = (ts, sensor, h, t, estado_actual)

        if estado_actual == "OK":
            normal_rows.append(new_row)
        else:
            evento_rows.append(new_row)

    write_rows(out_normal, normal_rows)
    write_rows(out_evento, evento_rows)

    return normal_rows, evento_rows
