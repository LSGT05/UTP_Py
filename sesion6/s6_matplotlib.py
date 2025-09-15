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
plt.title("Estudio de tiempo de sueño de adultos")                          #TITULOS
plt.xlabel("dias de la semana")                                             #TITULO DE EJE X
plt.ylabel("horas al dia")                                                  #TITULO DE EJE Y
plt.plot(ejex,ejey,'r-+',label="datos de tiempo de sueño de adultos")       # datos de ploteo (X,Y,formato y label)
plt.plot(ejex,ejey2,'bo',label="datos de tiempo de juego de adultos")      
plt.legend()                                                                #"leyenda"
plt.show()   