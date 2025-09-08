import csv
from datetime import datetime
from pathlib import Path #importo el comando path (busca el lugar del codigo)

#crear mis variables de rutas para ingreso de archivo y salida de archivo
ROOT=Path(__file__).resolve().parents[1]#busca el lugar donde esta guardado el codigo
IN_FILE=ROOT/"datos"/"raw"/"datos_sucios_250.csv" #ruta de ingreso
OUT_FILE=ROOT/"datos"/"proccesing"/"datos_sucios_250_limpio.csv" #ruta de salida

with open(IN_FILE,'r',encoding="utf-8", newline="") as fin, \
    open(OUT_FILE, "w", encoding="utf-8", newline="") as fout:
    reader=csv.DictReader(fin,delimiter=';')
    writer=csv.DictWriter(fout,fieldnames=["Tiempo","voltaje","control"])
    writer.writeheader()
#leer linea por lineal y seleccionar en crudo raw 
    total = kept = 0
    for row in reader:
        total+=1
        ts_raw  = (row.get("timestamp") or "").strip() #toma todos los valores de la columna timestamp
        val_raw = (row.get("value") or "").strip() #toma todos los valores de la columna value
#limpiar datos
        val_raw = val_raw.replace(",", ".")
        val_low = val_raw.lower() #empezar a eliminar valores no existentes
        if val_low in {"", "na", "n/a", "nan", "null", "none", "error"}:
            continue #salta el comando
        try:
            val = float(val_raw)
        except ValueError:
            continue  # saltar fila si no es número
#limpieza de datos de tiempo 
        ts_clean = None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S"):
            try:
                dt = datetime.strptime(ts_raw, fmt)
                ts_clean = dt.strftime("%Y-%m-%dT%H:%M:%S")
                break
            except ValueError:
                pass
#milisegundo (opcional)
        if ts_clean is None and "T" in ts_raw and len(ts_raw) >= 19:
            try:
                dt = datetime.strptime(ts_raw[:19], "%Y-%m-%dT%H:%M:%S")
                ts_clean = dt.strftime("%Y-%m-%dT%H:%M:%S")
            except ValueError:
                ts_clean = None

        if ts_clean is None:
            continue  # saltar fila si no pudimos interpretar la fecha
        

        if val >= 5:
            control = "CUIDADO"
        else:
            control = "OK"
#grabar datos en writer
        writer.writerow({"Tiempo": ts_clean, "voltaje": f"{val:.2f}", "control":control})
        kept += 1 #sume 1 kept, en nuestro caso cambia de fila