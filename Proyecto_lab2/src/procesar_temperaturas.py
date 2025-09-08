import csv
import os
import statistics

# Rutas de carpetas
RAW_PATH = "Proyecto_lab2/DATA/RAW/"
PROCESSED_PATH = "Proyecto_lab2/DATA/PROCESSED/"
OUTPUT_FILE = os.path.join(PROCESSED_PATH, "Temperaturas_Procesado.csv")

# Fórmula de conversión
def voltaje_a_temp(v):
    return round(18 * v * 64, 2)

# Variables KPI
filas_totales = 0
filas_validas = 0
descartes_timestamp = 0
descartes_valor = 0
temperaturas = []
alertas = 0

# Abrir archivo CSV de entrada
input_file = os.path.join(RAW_PATH, "datos_sucios_250_v2.csv")  

with open(input_file, "r", newline="", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = ["Timestamp", "Voltaje", "Temp_C", "Alertas"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        filas_totales += 1

        timestamp = row.get("Timestamp", "").strip()
        voltaje_str = row.get("Voltaje", "").replace(",", ".").strip()

        # Validación
        if not timestamp:
            descartes_timestamp += 1
            continue
        try:
            voltaje = float(voltaje_str)
        except ValueError:
            descartes_valor += 1
            continue

        # Conversión
        temp = voltaje_a_temp(voltaje)
        temperaturas.append(temp)
        filas_validas += 1

        # Generar alerta
        if temp > 40:
            alerta = "ALERTA"
            alertas += 1
        else:
            alerta = "OK"

        # Escribir salida
        writer.writerow({
            "Timestamp": timestamp,
            "Voltaje": voltaje,
            "Temp_C": temp,
            "Alertas": alerta
        })

# KPIs
print("\n===== RESULTADOS =====")
print(f"Filas_totales: {filas_totales}")
print(f"Filas_validas: {filas_validas}")
print(f"Descartes_Timestamp: {descartes_timestamp}")
print(f"Descartes_valor: {descartes_valor}")
print(f"n: {len(temperaturas)}")
if temperaturas:
    print(f"temp_min: {min(temperaturas)} °C")
    print(f"temp_max: {max(temperaturas)} °C")
    print(f"temp_prom: {round(statistics.mean(temperaturas),2)} °C")
print(f"Alertas (>40°C): {alertas}")
