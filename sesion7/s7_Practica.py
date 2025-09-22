import numpy as np
import matplotlib.pyplot as plt

dt=[i for i in range(200)] #lista
A=[12,20] #lista
f=[0.23,0.35]
theta_i=[0.26,1.45]
x1=A[0]*np.sin(2*np.pi*f[0]*np.array(dt)*0.1+theta_i[0]) #lista
x2=A[1]*np.sin(2*np.pi*f[1]*np.array(dt)*0.1+theta_i[1]) #lista
xaco=np.array(x1)+np.array(x2)

plt.plot(x1)
plt.plot(x2)
plt.plot(xaco)
plt.show()