#!/usr/bin/env python3
"""
run_pipeline.py
Punto de entrada del pipeline: crea dirs, detecta CSVs raw y procesa cada uno
(separa en normal / evento aplicando histeresis) y genera un reporte simple.
"""
import sys
from pathlib import Path

# importar desde el paquete pipeline
from src.pipeline import ensure_dirs, list_raw_csvs, make_clean_name, safe_stem
from src.pipeline import procesar_archivo
from src.pipeline import generate_report

BASE = Path(__file__).resolve().parent

def main():
    print("=== PIPELINE: INICIO ===")
    # asegurar directorios
    ensure_dirs(base=BASE)

    # buscar CSVs en data/raw
    raws = list_raw_csvs(base=BASE)
    if not raws:
        print("No se encontraron archivos CSV en data/raw. Coloca tus archivos y vuelve a ejecutar.")
        sys.exit(0)

    for raw_path in raws:
        print(f"\nProcesando: {raw_path.name}")
        stem = safe_stem(raw_path)
        # rutas de salida en data/processed
        processed_dir = BASE / "data" / "processed"
        normal_out = processed_dir / f"{raw_path.stem}_normal.csv"
        evento_out = processed_dir / f"{raw_path.stem}_evento.csv"

        # procesar archivo (separador de eventos)
        kpis = procesar_archivo(
            ruta_entrada=raw_path,
            ruta_salida_normal=normal_out,
            ruta_salida_evento=evento_out,
            base=BASE
        )

        # generar reporte por archivo
        report_path = BASE / "reports" / f"{raw_path.stem}_report.txt"
        generate_report(kpis, report_path)
        print(f"Reporte guardado en: {report_path}")

    print("\n=== PIPELINE: FIN ===")

if __name__ == "__main__":
    main()
