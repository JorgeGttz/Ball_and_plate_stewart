import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = [0,0,0]
y = [0,0,0]
z = [0,10,20]

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

ax.scatter(x,y,z)
plt.show()


