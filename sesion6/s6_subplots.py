import matplotlib.pyplot  as plt
import numpy as np

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

ejex=[i for i in range(30)] #crear numeros del 0 al 29
ejey=aleatorio(30)
ejey2=aleatorio(30)

fig,axs = plt.subplots(1,2)
fig.suptitle("datos por separado")
axs[0].plot(ejex,ejey,'go',label="datos de tiempo de sueño")
axs[0].set_title("datos de tiempo de sueño")
axs[0].set_xlabel("tiempo")
axs[1].plot(ejex,ejey2,'rx',label="datos de tiempo de juego")
axs[1].set_title("datos de tiempo de juego")
plt.show()