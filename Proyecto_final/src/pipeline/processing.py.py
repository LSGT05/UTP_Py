"""
processing.py
Contiene la función procesar_archivo que separa registros en NORMAL / EVENTO
según la histeresis (sin usar pandas).
Devuelve un diccionario simple de KPIs calculados sobre humedad y temperatura.
"""

from pathlib import Path
from typing import Dict, List, Tuple

# Histeresis (ajustar si es necesario)
ALERT_ON = 70.0
ALERT_OFF = 65.0

def _parse_line(line: str) -> Tuple[str, str, float, float, str]:
    """
    Parsear una línea CSV con formato:
    ts_ms,sensor_id,valor(s),estado
    donde valor(s) = humedad|temperatura
    Retorna (ts_ms, sensor_id, humedad, temperatura, estado_original)
    """
    parts = [p.strip() for p in line.split(",")]
    if len(parts) < 4:
        raise ValueError(f"Línea con formato inesperado: {line}")

    ts_ms = parts[0]
    sensor_id = parts[1]
    valor = parts[2]
    estado_original = parts[3]

    if "|" not in valor:
        raise ValueError(f"Campo 'valor(s)' sin separador '|': {valor}")

    humedad_str, temp_str = [v.strip() for v in valor.split("|", 1)]
    humedad = float(humedad_str)
    temperatura = float(temp_str)

    return ts_ms, sensor_id, humedad, temperatura, estado_original

def _append_csv_rows(path: Path, header: str, rows: List[str]):
    """Guardar filas (ya formateadas) en CSV, creando folder si es necesario."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for r in rows:
            f.write(r + "\n")

def _compute_kpis(hum_list: List[float], temp_list: List[float]) -> Dict[str, float]:
    """Calcular KPIs básicos (min, max, mean, count)."""
    def mean(xs):
        return sum(xs) / len(xs) if xs else 0.0

    return {
        "hum_min": min(hum_list) if hum_list else 0.0,
        "hum_max": max(hum_list) if hum_list else 0.0,
        "hum_mean": mean(hum_list),
        "hum_count": len(hum_list),
        "temp_min": min(temp_list) if temp_list else 0.0,
        "temp_max": max(temp_list) if temp_list else 0.0,
        "temp_mean": mean(temp_list),
        "temp_count": len(temp_list),
    }

def procesar_archivo(ruta_entrada: Path, ruta_salida_normal: Path, ruta_salida_evento: Path, base: Path = Path(".")) -> Dict[str, float]:
    """
    Procesa un CSV raw (sin pandas), separando filas en normal / evento usando histeresis.
    - ruta_entrada: Path al CSV raw
    - ruta_salida_normal: Path a donde guardar normal CSV
    - ruta_salida_evento: Path a donde guardar evento CSV
    Retorna un dict con KPIs.
    """
    ruta_entrada = Path(ruta_entrada)
    ruta_salida_normal = Path(ruta_salida_normal)
    ruta_salida_evento = Path(ruta_salida_evento)

    # leer todo el archivo
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines()]

    if not lines:
        raise ValueError("Archivo vacío: " + str(ruta_entrada))

    header = lines[0].strip()
    raw_data = lines[1:]

    estado_actual = "OK"
    normal_rows: List[str] = []
    evento_rows: List[str] = []

    hum_normal: List[float] = []
    temp_normal: List[float] = []
    hum_evento: List[float] = []
    temp_evento: List[float] = []

    for idx, linea in enumerate(raw_data, start=1):
        if not linea.strip():
            continue
        try:
            ts_ms, sensor_id, humedad, temperatura, estado_original = _parse_line(linea)
        except Exception as e:
            # ignorar líneas mal formateadas pero avisar por consola
            print(f"[WARN] Saltando línea {idx}: {e}")
            continue

        # aplicar histeresis
        if humedad >= ALERT_ON:
            estado_actual = "ALERT"
        elif humedad <= ALERT_OFF:
            estado_actual = "OK"
        # else: mantener estado_actual (zona neutra)

        # nueva fila formateada
        nueva_fila = f"{ts_ms},{sensor_id},{humedad:.2f},{temperatura:.2f},{estado_actual}"

        if estado_actual == "ALERT":
            evento_rows.append(nueva_fila)
            hum_evento.append(humedad)
            temp_evento.append(temperatura)
        else:
            normal_rows.append(nueva_fila)
            hum_normal.append(humedad)
            temp_normal.append(temperatura)

    # guardar archivos
    header_out = "ts_ms,sensor_id,humedad,temperatura,estado"
    _append_csv_rows(ruta_salida_normal, header_out, normal_rows)
    _append_csv_rows(ruta_salida_evento, header_out, evento_rows)

    # calcular KPIs combinados (sobre todo de interest: eventos y normal)
    kpis_normal = _compute_kpis(hum_normal, temp_normal)
    kpis_evento = _compute_kpis(hum_evento, temp_evento)

    kpis = {
        "file": ruta_entrada.name,
        "normal_count": kpis_normal["hum_count"],
        "evento_count": kpis_evento["hum_count"],
        "normal_hum_min": kpis_normal["hum_min"],
        "normal_hum_max": kpis_normal["hum_max"],
        "normal_hum_mean": kpis_normal["hum_mean"],
        "evento_hum_min": kpis_evento["hum_min"],
        "evento_hum_max": kpis_evento["hum_max"],
        "evento_hum_mean": kpis_evento["hum_mean"],
        "normal_temp_mean": kpis_normal["temp_mean"],
        "evento_temp_mean": kpis_evento["temp_mean"]
    }

    print(f"[OK] Procesado '{ruta_entrada.name}': normal={len(normal_rows)} evento={len(evento_rows)}")
    return kpis
