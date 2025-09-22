import S5_defunct as ds
Voltajes=ds.aleatorio(30)
Temperatura=[ds.conversor(v) for v in Voltajes] #listas compactas con funciones
alertas=[ds.clasificar_alertas(i,10) for i in Temperatura]
print(Temperatura, alertas)