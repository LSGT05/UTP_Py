import random as rd
Vingreso = []
for i in range(20):
    Vingreso.append(rd.randint(1, 30))
print("Lista de voltajes generados:")
print(Vingreso)
Vbajo = []
Vmedio = []
Valto = []
for v in Vingreso:
    if v < 10:
        Vbajo.append(v)
    elif v <= 20:
        Vmedio.append(v)
    else:
        Valto.append(v)
print("\n⚡ Clasificación de voltajes:")
print(f"Voltajes bajos (<10V): {Vbajo} → Total: {len(Vbajo)}")
print(f"Voltajes medios (10-20V): {Vmedio} → Total: {len(Vmedio)}")
print(f"Voltajes altos (>20V): {Valto} → Total: {len(Valto)}")
