import numpy as np
import matplotlib.pyplot as plt
# ------------------------------------#
# calculo del sistema de armonicos#
# x(t)=A*sin(2*pi*f*dt+theta_0)#

dt=[i for i in range (200)]
t=np.array(dt)*0.03 #paso de tiempo
#variables de los armonicos
A=[4,3]
f=[1,1.87]
theta_i=[0.26,0.5]
#formulas matematicas a trabajar
x1=A[0]*np.sin(2*np.pi*f[0]*t+f[0])
x2=A[1]*np.sin(2*np.pi*f[1]*t+theta_i[1])
xaco=np.array(x1)+np.array(x2)
#parte grafica
fig,axs = plt.subplots(3)
figtitle="Funciones armonicas y sus acoplados"
fig.suptitle(figtitle.upper(),fontdict={'fontweight': 'bold'})
axs[0].plot(t,x1,color="#10144bd3",marker='x', linestyle='--',linewidth=3, markersize=2,label="aleatorio 1")
axs[0].set_title(f"Armonico con valores (A,f,thetao)={A[0],f[0],theta_i[0]}")
axs[0].set_xticks([])
axs[0].grid()
axs[0].set_ylim(-7, 7)
axs[1].plot(t,x2,color="#52d46cd2",marker='o', linestyle=':',linewidth=3, markersize=2,label="aleatorio 1")
axs[1].set_title(f"Armonico con valores (A,f,thetao)={A[1],f[1],theta_i[1]}")
axs[1].set_xticks([])
axs[1].grid()
axs[1].set_ylim(-7, 7)
axs[2].plot(t,xaco,color="#ff8400d2", linestyle='-',linewidth=1,label="aleatorio 1")
axs[2].grid()
axs[2].set_ylim(-7, 7)
plt.savefig('AcoplamientoArmonico.pdf',bbox_inches ="tight", 
			pad_inches = 0.3,dpi=640,edgecolor="b",facecolor ="#fcb2b2eb")