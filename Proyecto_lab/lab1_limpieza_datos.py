import csv
import statistics
import os

# Archivos
BASE_DIR = "Proyecto_lab"
INPUT_FILE = os.path.join(BASE_DIR, "datos_sucios_250_v2.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "Temperaturas_Procesado.csv")
REPORT_FILE = os.path.join(BASE_DIR, "informe.txt")

def limpiar_valor(valor):
    """Convierte el valor de voltaje a float. Corrige comas decimales."""
    try:
        if valor is None or valor.strip() == "" or valor.strip().upper() == "NA":
            return None
        return float(valor.replace(",", "."))
    except:
        return None

def voltaje_a_temp(v):
    return round(18 * v - 64, 2)

def main():
    filas_totales = 0
    filas_validas = 0
    descartes_timestamp = 0
    descartes_valor = 0
    temperaturas = []
    alertas_count = 0

    # Crear carpeta si no existe
    os.makedirs(BASE_DIR, exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)
        writer = csv.writer(f_out)
        writer.writerow(["Timestamp", "Voltaje", "Temp_C", "Alertas"])

        for row in reader:
            filas_totales += 1
            timestamp = row.get("Timestamp", "").strip()
            voltaje_raw = row.get("Voltaje", "").strip()

            # Descarte por timestamp vacío
            if timestamp == "":
                descartes_timestamp += 1
                continue

            # Limpieza de voltaje
            v = limpiar_valor(voltaje_raw)
            if v is None:
                descartes_valor += 1
                continue

            # Conversión a temperatura
            temp = voltaje_a_temp(v)
            alerta = "ALERTA" if temp > 40 else "OK"
            if alerta == "ALERTA":
                alertas_count += 1

            # Escribir fila procesada
            writer.writerow([timestamp, f"{v:.2f}", temp, alerta])
            filas_validas += 1
            temperaturas.append(temp)

    # KPIs
    if temperaturas:
        temp_min = min(temperaturas)
        temp_max = max(temperaturas)
        temp_prom = round(statistics.mean(temperaturas), 2)
    else:
        temp_min = temp_max = temp_prom = None

    with open(REPORT_FILE, "w", encoding="utf-8") as rep:
        rep.write("KPIs DEL PROCESO\n")
        rep.write(f"Filas_totales: {filas_totales}\n")
        rep.write(f"Filas_validas: {filas_validas}\n")
        rep.write(f"Descartes_Timestamp: {descartes_timestamp}\n")
        rep.write(f"Descartes_Valor: {descartes_valor}\n")
        rep.write(f"n: {len(temperaturas)}\n")
        rep.write(f"temp_min: {temp_min}\n")
        rep.write(f"temp_max: {temp_max}\n")
        rep.write(f"temp_prom: {temp_prom}\n")
        rep.write(f"Alertas: {alertas_count}\n")

    print("Procesamiento terminado. Resultados en:")
    print(f"   → {OUTPUT_FILE}")
    print(f"   → {REPORT_FILE}")

if __name__ == "__main__":
    main()
