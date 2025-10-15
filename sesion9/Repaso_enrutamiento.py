from pathlib import Path
#enrutamiento de entrada
ROOT=Path(__file__).resolve().parents[1] #estandar en TODOS LOS LUGARES
DATA_DIR=ROOT/"Sesion 4"/"datos"/"proccesing"
Filename="voltajes_250_sucio_limpio.csv"
CSV_PATH=DATA_DIR/Filename
if not CSV_PATH.exists():
    raise FileNotFoundError(f"No existe: {CSV_PATH}")
#comandos de extraccion de informacion 
#name extrae el nombre del archivo con todo y su extension.
#print(CSV_PATH.name)
#stem extra el nombre del archivo sin su extension
#print(CSV_PATH.stem)
#para cambiar de extension usamos el comando with_suffix
#INFO_DIR=CSV_PATH.with_suffix(".png")
#nombre=CSV_PATH.with_name(f"{CSV_PATH.stem.replace('limpio','procesado')}{CSV_PATH.suffix}")
#print(nombre)
prefijo, valor, estado, n = CSV_PATH.stem.split("_")
nuevo = CSV_PATH.with_name(f"{prefijo}_{valor}_Procesados_{n}{CSV_PATH.suffix}")
print(nuevo)

Umbral_V=5.1
ts_run = "20251006" #YYYYMMDD
nombre_salida=f"{prefijo}_{valor}_umbral_{Umbral_V}_fecha_{ts_run}.png"
print(nombre_salida)
