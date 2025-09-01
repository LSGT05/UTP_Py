import datetime as dt
import random as rd
#constante
nombre= "Luis"
# fecha actual
fecha = dt.datetime.now().strftime("%Y-%m-%d")

# función para clasificar voltaje
def clasificar_voltaje(v):
    if v <= 341:
        return "Bajo"
    elif v <= 682:
        return "Medio"
    else:
        return "Alto"

# salida en pantalla
print("Cordial saludo Ing. " + nombre)
print("Fecha:", fecha)
print("Los valores tomados:")

# generar 15 valores aleatorios
for i in range(15):
    v = rd.randint(1, 1023)
    nivel = clasificar_voltaje(v)
    print(f"{i+1}. Voltaje: {v} ({nivel})")
