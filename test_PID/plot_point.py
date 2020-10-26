import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time  

for i in range(100):
	fig = plt.gcf()
	plt.xlim(-300,300)
	plt.ylim(-200,200)
	plt.grid()
	circle1=plt.Circle((i,i),20,color='g')
	fig.gca().add_artist(circle1)
	plt.pause(0.03)
	plt.clf()
