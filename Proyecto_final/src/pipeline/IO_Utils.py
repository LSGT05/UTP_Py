import os

def leer_archivo(ruta):
    with open(ruta, "r") as f:
        return f.read().strip().split("\n")

def guardar_archivo(ruta, contenido):
    with open(ruta, "w") as f:
        f.write(contenido)

def listar_archivos(directorio):
    return [f for f in os.listdir(directorio) if f.endswith(".csv")]
