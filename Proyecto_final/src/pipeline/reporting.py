"""
reporting.py
Generación de reportes simples (texto plano) con los KPIs que devuelve procesar_archivo.
"""
from pathlib import Path
from typing import Dict

def generate_report(kpis: Dict[str, float], output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Reporte de procesamiento\n")
        f.write("========================\n\n")
        f.write(f"Archivo: {kpis.get('file', 'unknown')}\n\n")
        f.write(f"Registros NORMAL: {kpis.get('normal_count', 0)}\n")
        f.write(f"Registros EVENTO: {kpis.get('evento_count', 0)}\n\n")
        f.write("Humedad (NORMAL):\n")
        f.write(f"  min: {kpis.get('normal_hum_min', 0)}\n")
        f.write(f"  max: {kpis.get('normal_hum_max', 0)}\n")
        f.write(f"  mean: {kpis.get('normal_hum_mean', 0):.2f}\n\n")
        f.write("Humedad (EVENTO):\n")
        f.write(f"  min: {kpis.get('evento_hum_min', 0)}\n")
        f.write(f"  max: {kpis.get('evento_hum_max', 0)}\n")
        f.write(f"  mean: {kpis.get('evento_hum_mean', 0):.2f}\n\n")
        f.write(f"Temperatura media (NORMAL): {kpis.get('normal_temp_mean', 0):.2f}\n")
        f.write(f"Temperatura media (EVENTO): {kpis.get('evento_temp_mean', 0):.2f}\n")
