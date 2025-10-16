import csv
from datetime import datetime
from pathlib import Path
from .IO_Utils import detectar_delimitador

NA_TOKENS = {"", "na", "n/a", "nan", "null", "none", "error"}


def parse_ts(s: str):
    s = (s or "").strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    if "T" in s and len(s) >= 19:
        try:
            return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None
    return None


def parse_v(s: str):
    if s is None:
        return None
    s = str(s).strip().replace(",", ".").lower()
    if s in NA_TOKENS:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean_file(in_path: Path, out_path: Path, ts_col="timestamp", v_col_candidates=("voltage_V", "voltaje", "value")):
    """
    Limpia CSV y convierte Voltaje → Temperatura (K)
    Fórmula lineal: (0.4V, -30°C) y (5.6V, 120°C)
    T(K) = 273.15 + (-30 + (150)*(V - 0.4)/5.2)
    """
    delim = detectar_delimitador(in_path)
    ts_list, volts_list, temps = [], [], []
    total = kept = bad_ts = bad_val = 0

    with in_path.open("r", encoding="utf-8", newline="") as fin, \
         out_path.open("w", encoding="utf-8", newline="") as fout:
        reader = csv.DictReader(fin, delimiter=delim)
        writer = csv.DictWriter(fout, fieldnames=["timestamp", "voltage_V", "temperature_K"])
        writer.writeheader()

        for row in reader:
            total += 1
            ts_raw = (row.get(ts_col) or "").strip()
            t = parse_ts(ts_raw)
            if t is None:
                bad_ts += 1
                continue

            v_raw = None
            for cand in v_col_candidates:
                if row.get(cand) is not None:
                    v_raw = row.get(cand)
                    break

            v = parse_v(v_raw)
            if v is None:
                bad_val += 1
                continue

            temp_C = -30 + (120 - (-30)) * (v - 0.4) / (5.6 - 0.4)
            temp_K = temp_C + 273.15

            writer.writerow({
                "timestamp": t.strftime("%Y-%m-%dT%H:%M:%S"),
                "voltage_V": f"{v:.3f}",
                "temperature_K": f"{temp_K:.2f}"
            })

            ts_list.append(t)
            volts_list.append(v)
            temps.append(temp_K)
            kept += 1

    stats = {
        "filas_totales": total,
        "filas_validas": kept,
        "descartes_timestamp": bad_ts,
        "descartes_valor": bad_val,
        "%descartadas": round(((bad_ts + bad_val) / total * 100.0) if total else 0.0, 2),
    }

    return ts_list, volts_list, temps, stats
