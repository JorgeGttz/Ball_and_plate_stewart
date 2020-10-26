import numpy as np
import matplotlib.pyplot as plt

#Ejemplo para graficar puntos en 2D
periodo = 2

# Definimos el array dimensional
x = np.linspace(0, 10, 1000)
# Definimos la funciÃ³n senoidal
y = np.sin(2*np.pi*x/periodo)  

plt.figure()
plt.plot(x,y,'r')
plt.show()

