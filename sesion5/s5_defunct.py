def aleatorio(n=20):
    #Docstring
    """permite generar numeros aleatorios de valor entero entre 1 y 30 y da de salida una lista de valores

    Args:
        n (int, optional): numero el datos ingresados. Defecto 20.
    """
    import random as rd
    Value=[] #lista vacia
    for i in range (n): #incio de un bucle es con el : el identado es importante
        Value.append(rd.randint(1,30)) #append añade a la lista\
    return(Value) #lo que devuelve la funcion

def conversor(Volt):
    """convierte los valor de voltaje de un sensor a temperatura en grados centigrados, no acepta valores de lista

    Args:
        Volt (float): voltaje detectado por el sensor
    """
    Temp=2*Volt-15
    return Temp

def clasificar_alertas(temp_c,umbral=0):
    """Devuelve 'ALERTA' si temp_c > umbral, si no 'OK'"""
    return "ALERTA" if temp_c > umbral else "OK" #if corto

def main(): #el codigo principal
    Voltajes=aleatorio(30)
    Temperatura=[conversor(v) for v in Voltajes] #listas compactas con funciones
    # Temperatura = []
    # for v in Voltaje:
    #   Temperatura.apped(conversor(v))
    alertas=[clasificar_alertas(i,10) for i in Temperatura]
    print(Temperatura, alertas)

if __name__ == "__main__": #crear paqueterias
    main()