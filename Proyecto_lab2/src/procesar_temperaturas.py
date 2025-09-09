import csv
import os
import statistics

# === Configuración de carpetas ===
RAW_PATH = "Proyecto_lab2/DATA/RAW/"          # Carpeta de entrada
PROCESSED_PATH = "Proyecto_lab2/DATA/PROCESSED/"  # Carpeta de salida
INPUT_FILE = os.path.join(RAW_PATH, "datos_sucios_250_v2.csv")  # Cambia "datos.csv" por tu archivo real
OUTPUT_FILE = os.path.join(PROCESSED_PATH, "Temperaturas_Procesado.csv")
REPORT_FILE = os.path.join(PROCESSED_PATH, "Resultados.txt")

# === Función de conversión ===
def voltaje_a_temp(v):
    """Convierte voltaje a temperatura (°C) con 2 decimales"""
    return round(18 * v * 64, 2)

# === Variables para KPIs ===
filas_totales = 0
filas_validas = 0
descartes_timestamp = 0
descartes_valor = 0
temperaturas = []
alertas = 0

# === Procesamiento de datos ===
with open(INPUT_FILE, "r", newline="", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = ["Timestamp", "Voltaje", "Temp_C", "Alertas"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        filas_totales += 1

        timestamp = row.get("Timestamp", "").strip()
        voltaje_str = row.get("Voltaje", "").replace(",", ".").strip()

        # Validación de timestamp
        if not timestamp:
            descartes_timestamp += 1
            continue

        # Validación de voltaje
        try:
            voltaje = float(voltaje_str)
        except ValueError:
            descartes_valor += 1
            continue

        # Conversión Voltaje → Temperatura
        temp = voltaje_a_temp(voltaje)
        temperaturas.append(temp)
        filas_validas += 1

        # Alerta si temp > 40 °C
        if temp > 40:
            alerta = "ALERTA"
            alertas += 1
        else:
            alerta = "OK"

        # Escribir en archivo de salida
        writer.writerow({
            "Timestamp": timestamp,
            "Voltaje": voltaje,
            "Temp_C": temp,
            "Alertas": alerta
        })

# === Crear reporte en archivo TXT ===
with open(REPORT_FILE, "w", encoding="utf-8") as report:
    report.write("===== RESULTADOS DEL PROCESAMIENTO =====\n")
    report.write(f"Filas_totales: {filas_totales}\n")
    report.write(f"Filas_validas: {filas_validas}\n")
    report.write(f"Descartes_Timestamp: {descartes_timestamp}\n")
    report.write(f"Descartes_valor: {descartes_valor}\n")
    report.write(f"n: {len(temperaturas)}\n")

    if temperaturas:
        report.write(f"temp_min: {min(temperaturas)} °C\n")
        report.write(f"temp_max: {max(temperaturas)} °C\n")
        report.write(f"temp_prom: {round(statistics.mean(temperaturas),2)} °C\n")

    report.write(f"Alertas (>40°C): {alertas}\n")

print(f"\n Procesamiento finalizado. Resultados guardados en:\n- {OUTPUT_FILE}\n- {REPORT_FILE}")
