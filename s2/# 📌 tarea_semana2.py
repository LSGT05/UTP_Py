#  tarea_semana2.py

# Constantes de umbral
UMBRAL_BAJO = 3.0
UMBRAL_MEDIO = 4.0
UMBRAL_ALTO = 5.0

print("=== CLASIFICADOR DE ESTADO DE SENSOR ===")

# Entrada de nombre/alumno/equipo
nombre = input("Ingrese el nombre del alumno: ")
equipo = input("Ingrese el código del equipo: ")

# Número de muestras
try:
    n_muestras = int(input("Ingrese el número de lecturas (mínimo 2): "))
    if n_muestras < 2:
        raise ValueError("Debe ingresar al menos 2 lecturas.")
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Lecturas en float
lecturas = []
for i in range(n_muestras):
    try:
        valor = float(input(f"Ingrese lectura {i+1} (V): "))
        lecturas.append(valor)
    except ValueError:
        print("⚠️ Error: Ingrese un número válido (float).")
        exit()

# Calcular promedio
promedio = sum(lecturas) / n_muestras

# Clasificación del estado
if promedio < UMBRAL_BAJO:
    estado = "MUY BAJO"
elif promedio < UMBRAL_MEDIO:
    estado = "BAJO"
elif promedio < UMBRAL_ALTO:
    estado = "MEDIO"
else:
    estado = "ALTO"

# Reporte final
print("\n=== REPORTE DE SENSOR ===")
print(f"Alumno: {nombre} | Equipo: {equipo}")
print(f"Lecturas (V): {', '.join(f'{v:.2f}' for v in lecturas)}")
print(f"Promedio: {promedio:.2f} V")
print(f"Estado: {estado} (>= {UMBRAL_ALTO:.2f} V -> ALTO)")
