def limpiar_valores(lista):
    limpio = []
    for x in lista:
        try:
            num = float(x)
            if 0 <= num <= 100:
                limpio.append(num)
        except:
            pass
    return limpio
