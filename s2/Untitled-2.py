valor_txt=input("ingrese los valores de temperatura en C: ")
try:
    t=float(valor_txt)
    if t >=30: #condicion if "condicion1"
        print("Alerta! Alta Temperatura")
    elif t < 0: #condicion 2
        print("temperatura bajo 0")
    else:
        print("Temperatura Normal")
except ValueError:
    print("Entrada invalida. Use numeros (eje:120, 30, 5).")