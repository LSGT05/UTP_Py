import random as rd
lista = []
for i in range(10):
    lista.append(rd.randint(1, 100))
print("Lista de numeros:", lista)
n = len(lista)
for i in range(n):
    for j in range(0, n - i - 1):
        if lista[j] > lista[j + 1]:
            lista[j], lista[j + 1] = lista[j + 1], lista[j]
print("ascendente:", lista)
print("descendente:", lista[::-1])
