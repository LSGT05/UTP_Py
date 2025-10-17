import csv
from datetime import datetime
from pathlib import Path
from .IO_Utils import detectar_delimitador

# Tokens que representan datos no válidos
NA_TOKENS = {"", "na", "n/a", "nan", "null", "none", "error"}

# Calibración lineal Voltaje→Temperatura (°C)
# Datos de calibración:
V1, T1 = 0.4, -30.0   # Punto 1: (V1, T1)
V2, T2 = 5.6, 120.0   # Punto 2: (V2, T2)

def voltaje_a_kelvin(v):
    """Convierte un voltaje (V) a temperatura en Kelvin (K)."""
    t_celsius = T1 + (T2 - T1) * (v - V1) / (V2 - V1)
    return t_celsius + 273.15  # °C → K


def parse_ts(s: str):
    """Normaliza timestamp a datetime (acepta 'YYYY-MM-DDTHH:MM:SS' y 'dd/mm/YYYY HH:MM:SS')."""
    s = (s or "").strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    # Intento adicional: cortar ISO largo
    if "T" in s and len(s) >= 19:
        try:
            return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None
    return None


def parse_v(s: str):
    """Convierte a float, admitiendo coma decimal y tokens NA."""
    if s is None:
        return None
    s = str(s).strip().replace(",", ".").lower()
    if s in NA_TOKENS:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean_file(in_path: Path, out_path: Path,
               ts_col="timestamp",
               v_col_candidates=("value", "voltage_V", "voltaje")):
    """
    Lee un CSV crudo (ej: timestamp,value), limpia y escribe un CSV con:
       timestamp,voltage_V,temperature_K
    Devuelve: (ts_list, volts_list, temps_list, stats_dict)
    """
    delim = detectar_delimitador(in_path)
    ts_list, volts_list, temps_list = [], [], []
    total = kept = bad_ts = bad_val = 0

    with in_path.open("r", encoding="utf-8", newline="") as fin, \
         out_path.open("w", encoding="utf-8", newline="") as fout:

        reader = csv.DictReader(fin, delimiter=delim)
        writer = csv.DictWriter(fout, fieldnames=["timestamp", "voltage_V", "temperature_K"])
        writer.writeheader()

        for row in reader:
            total += 1

            #Timestamp
            ts_raw = (row.get(ts_col) or "").strip()
            t = parse_ts(ts_raw)
            if t is None:
                bad_ts += 1
                continue

            #Voltaje
            v_raw = None
            for cand in v_col_candidates:
                if row.get(cand) is not None:
                    v_raw = row.get(cand)
                    break
            v = parse_v(v_raw)
            if v is None:
                bad_val += 1
                continue

            #Calibración Voltaje→Temperatura (K)
            temp_k = voltaje_a_kelvin(v)

            writer.writerow({
                "timestamp": t.strftime("%Y-%m-%dT%H:%M:%S"),
                "voltage_V": f"{v:.3f}",
                "temperature_K": f"{temp_k:.2f}"
            })

            ts_list.append(t)
            volts_list.append(v)
            temps_list.append(temp_k)
            kept += 1

    stats = {
        "filas_totales": total,
        "filas_validas": kept,
        "descartes_timestamp": bad_ts,
        "descartes_valor": bad_val,
        "%descartadas": round(((bad_ts + bad_val) / total * 100.0) if total else 0.0, 2),
    }

    return ts_list, volts_list, temps_list, stats
