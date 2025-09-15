import matplotlib.pyplot as plt 
import numpy as np
def aleatorio(n=20):
    #Docstring
    """permite generar numeros aleatorios de valor entero entre 1 y 30 y da de salida una lista de valores
    Args:
       n (int, optional): numero el datos ingresados. Defecto 20.
    """
    import random as rd
    Value=[]        #lista vacia
    for i in range (n):       #incio de un bucle es con el: el identado es importante
        Value.append(rd.randint (1,30))      #append añade a la lista\
    return(Value)       #lo que devuelve la funcion
ejex=[i for i in range(30)]
ejey=aleatorio(30)
fig, ax = plt.subplots()   #crear una figura con ejes simples
ax.plot(ejex, ejey)        #datos de ploteo (X, Y)
plt.show()                 #grafica la imagen





