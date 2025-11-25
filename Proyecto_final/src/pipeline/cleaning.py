from .IO_Utils import write_csv, make_clean_name, safe_stem, Root

# Valores de histeresis
ALERT_ON = 70.0     # Humedad arriba de este valor → evento
ALERT_OFF = 65.0    # Humedad abajo → normal


def parse_valores(cadena):
    """
    Recibe:  "77.5|36.3"
    Devuelve: (humedad_float, temperatura_float)
    """
    h, t = cadena.split("|")
    return float(h), float(t)


def clean_file(filepath):
    """
    Carga el CSV, separa filas en:
      - normal
      - evento
    según la histeresis aplicada sobre la humedad.
    """
    from .IO_Utils import read_csv  # evitar import circular

    rows = read_csv(filepath)

    normales = []
    eventos = []

    in_alert = False  # estado interno de histeresis

    for row in rows:
        humedad, temp = parse_valores(row["valor(s)"])

        # ---- Lógica de histeresis ----
        if not in_alert:
            if humedad >= ALERT_ON:
                in_alert = True
        else:
            if humedad <= ALERT_OFF:
                in_alert = False

        # Clasificación final
        if in_alert:
            eventos.append(row)
        else:
            normales.append(row)

    # ----------- Guardar resultados ---------------
    stem = safe_stem(filepath)

    normal_name = make_clean_name(stem, "normal")
    evento_name = make_clean_name(stem, "evento")

    normal_path = f"{Root.PROCESSED}/{normal_name}"
    evento_path = f"{Root.PROCESSED}/{evento_name}"

    fieldnames = ["ts_ms", "sensor_id", "valor(s)", "estado"]

    write_csv(normal_path, fieldnames, normales)
    write_csv(evento_path, fieldnames, eventos)

    return normal_path, evento_path
