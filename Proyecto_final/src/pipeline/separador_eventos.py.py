import os

ALERT_ON = 70.0
ALERT_OFF = 65.0

def procesar_archivo(ruta_entrada, ruta_salida_normal, ruta_salida_evento):

    with open(ruta_entrada, "r") as f:
        lines = f.read().strip().split("\n")

    header = lines[0]
    data = lines[1:]

    estado_actual = "OK"
    normal = []
    evento = []

    for linea in data:
        partes = linea.split(",")

        ts_ms = partes[0]
        sensor_id = partes[1]
        valores = partes[2]
        estado_original = partes[3]

        humedad_str, temp_str = valores.split("|")
        humedad = float(humedad_str)
        temp = float(temp_str)

        # ----- HISTERESIS -----
        if humedad >= ALERT_ON:
            estado_actual = "ALERT"
        elif humedad <= ALERT_OFF:
            estado_actual = "OK"

        nueva = f"{ts_ms},{sensor_id},{humedad},{temp},{estado_actual}"

        if estado_actual == "ALERT":
            evento.append(nueva)
        else:
            normal.append(nueva)

    # Guardar NORMAL
    with open(ruta_salida_normal, "w") as f:
        f.write("ts_ms,sensor_id,humedad,temperatura,estado\n")
        f.write("\n".join(normal))

    # Guardar EVENTO
    with open(ruta_salida_evento, "w") as f:
        f.write("ts_ms,sensor_id,humedad,temperatura,estado\n")
        f.write("\n".join(evento))

    print(f"[OK] Procesado: {ruta_entrada}")
    print(f" → Normal: {ruta_salida_normal}")
    print(f" → Evento: {ruta_salida_evento}")
