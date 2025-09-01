import datetime as dt
nombre = "luis" #constante por conversion- str
edad = 20    #int
voltaje = 3.14159 #float
activo = True #bool
fecha = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"Cordial saludo Ing. {nombre}, Edad: {edad}")
print(f"fecha de la medicion: {fecha}")
print(f"El voltaje medido es {voltaje:.5f} V | Activo: {activo}")
print(f"tipos ---> edad:{type(edad).__name__}, voltaje:{type(voltaje).__name__}")