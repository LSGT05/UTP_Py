import csv
import os

# ==============================
# RUTAS (según la estructura solicitada)
# ==============================
base_path = os.path.dirname(os.path.abspath(__file__))  # carpeta SRC
input_file = os.path.join(base_path, "../DATA/RAW/datos_sucios_250_v2.csv")
output_file = os.path.join(base_path, "../DATA/PROCESSED/Temperaturas_Procesado.csv")
kpi_file = os.path.join(base_path, "../DATA/PROCESSED/KPIs.txt")

# Crear carpetas si no existen
os.makedirs(os.path.join(base_path, "../DATA/RAW"), exist_ok=True)
os.makedirs(os.path.join(base_path, "../DATA/PROCESSED"), exist_ok=True)

# ==============================
# VARIABLES DE CONTROL
# ==============================
filas_totales = 0
filas_validas = 0
descartes_timestamp = 0
descartes_valor = 0
alertas_count = 0
temperaturas = []

# ==============================
# LECTURA Y LIMPIEZA DE DATOS
# ==============================
with open(input_file, "r", encoding="utf-8", errors="ignore") as f_in, \
     open(output_file, "w", newline="", encoding="utf-8") as f_out:

    reader = csv.DictReader(f_in, delimiter=";")
    fieldnames = ["Timestamp", "Voltaje", "Temp_C", "Alertas"]
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        filas_totales += 1
        timestamp = row.get("timestamp", "").strip()
        valor = row.get("value", "").strip()

        # Validación de Timestamp
        if timestamp == "" or timestamp.upper() == "NA":
            descartes_timestamp += 1
            continue

        # Limpieza de Voltaje
        valor = valor.replace(",", ".")
        try:
            voltaje = float(valor)
        except ValueError:
            descartes_valor += 1
            continue

        # Conversión Voltaje → Temperatura
        temp_c = round(18 * voltaje - 64, 2)
        temperaturas.append(temp_c)

        # Generar alerta
        alerta = "ALERTA" if temp_c > 40 else "OK"
        if alerta == "ALERTA":
            alertas_count += 1

        # Guardar fila válida
        writer.writerow({
            "Timestamp": timestamp,
            "Voltaje": voltaje,
            "Temp_C": temp_c,
            "Alertas": alerta
        })

        filas_validas += 1

# ==============================
# CÁLCULO DE KPIs
# ==============================
kpis = {
    "Filas_totales": filas_totales,
    "Filas_Validas": filas_validas,
    "Descartes_Timestamp": descartes_timestamp,
    "Descartes_valor": descartes_valor,
    "n": len(temperaturas),
    "temp_min": min(temperaturas) if temperaturas else None,
    "temp_max": max(temperaturas) if temperaturas else None,
    "temp_prom": round(sum(temperaturas)/len(temperaturas), 2) if temperaturas else None,
    "Alertas": alertas_count
}

# ==============================
# GUARDAR KPIs EN TXT
# ==============================
with open(kpi_file, "w", encoding="utf-8") as f_kpi:
    f_kpi.write("===== KPIs DEL PROCESAMIENTO =====\n")
    for k, v in kpis.items():
        f_kpi.write(f"{k}: {v}\n")

# Mostrar resultados en pantalla
print("===== KPIs =====")
for k, v in kpis.items():
    print(f"{k}: {v}")

print(f"\nArchivo generado: {output_file}")
print(f"KPIs guardados en: {kpi_file}")
