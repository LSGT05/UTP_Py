import random as rd
voltajes = []
for i in range(10):
    num = rd.randint(0, 10)   
    voltajes.append(num)
print("Lista de voltajes:")
print([f"{v:.2f}" for v in voltajes])  
for idx, v in enumerate(voltajes, start=1):
    if v > 5:
        print(f"{idx}: {v:.2f} V -> Voltaje alto")
    else:
        print(f"{idx}: {v:.2f} V -> Voltaje bajo")
