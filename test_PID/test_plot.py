import matplotlib.pyplot as plt
import numpy as np
 
x_plot = range(0,5)
y_plot = np.sin(x_plot)

plt.title("Test Plot")
plt.xlabel("Time(ms)")
plt.ylabel("Position")

plt.plot(x_plot,y_plot,":")
plt.show()
