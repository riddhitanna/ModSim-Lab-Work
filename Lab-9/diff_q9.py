import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


cold = 0
hot = 50
ambient = 25


class Cell:

	def __init__(self, x, y, state=cold):
		self.x = x
		self.y = y
		self.state = state

	def setState(self, diffRate, N,NE,E,SE,S,SW,W,NW):
		"""set the state of site at time t+1
		input : N, NE, E, SE, S, SW, W, NW = temperatures at the neighbour cells
				diffRate = rate of diffusion
				siteTemp = temperature of the site at time t
		ouput : temperature of site at time t+1 

		"""
		rnd = np.random.normal(loc=0, scale=0.5, size=8)
		

		self.state = (1-(8-rnd.sum())*diffRate)*self.state + diffRate*((1-rnd[0])*N + (1-rnd[1])*NE + (1-rnd[2])*E + (1-rnd[3])*SE + 
			(1-rnd[4])*S + (1-rnd[5])*SW + (1-rnd[6])*W + (1-rnd[7])*NW)


m = 20
n = 20
T = 20
diffRate = 0.125
bar = []

for i in range(m):
	for j in range(n):
		bar.append(Cell(i,j))
bar = np.reshape(np.array(bar), [m,n])

for i in range(m):
	bar[i][n-1].state = 25
	bar[i][0].state = 25
for j in range(n):
	bar[0][j].state = 25
	bar[m-1][j].state = 25





# applying hot and cold sites to pre-defined cells - this can be changed to random sites or 
# any sites that you wish to 

hot_sites_x = [3, 4, 5]
hot_sites_y = [4, 6, 8]	

cold_sites_x = [10, 11, 15]	
cold_sites_y = [1, 5, 2]

# applying the diffusion simulation
mid_temps = []
for c in range(100):
	print(c)
	all_states = np.zeros([T,m,n])

	for t in range(T):

		for i in range(m):
			for j in range(n):
				all_states[t][i][j] = bar[i][j].state

	for t in range(1,T):
		count=0
		for i in range(len(hot_sites_x)):
			bar[hot_sites_x[i]][hot_sites_y[i]].state = hot
			all_states[t][hot_sites_x[i]][hot_sites_y[i]] = bar[hot_sites_x[i]][hot_sites_y[i]].state
		for j in range(len(cold_sites_x)):
			bar[cold_sites_y[j]][cold_sites_y[i]].state = cold
			all_states[t][cold_sites_x[i]][cold_sites_y[i]] = bar[cold_sites_x[i]][cold_sites_y[i]].state

		for i in range(1,m-1):
			for j in range(1,n-1):
				bar[i][j].setState(diffRate, 
	            	bar[i-1][j].state, bar[i-1][j+1].state,
	            	bar[i][j+1].state, bar[i+1][j+1].state,
	            	bar[i+1][j].state, bar[i+1][j-1].state,
	            	bar[i][j-1].state, bar[i-1][j-1].state)
				all_states[t][i][j] = bar[i][j].state
				if(abs(all_states[t][i][j]- all_states[t-1][i][j])<0.001):
					count=count+1

	print(count, t)
	if(count==(m-2)*(n-2)):
   		print("Equilibrium state is achieved at time: ",t)
   		equi = t
   		break
	mid_temps.append(bar[int(m/2)][int(n/2)].state)


mid_temps = np.array(mid_temps)	        	
print('Mean of temp of a cell in the middle of the bar: {}'.format(mid_temps.mean()))
print('Min: {}, Max: {}'.format(mid_temps.min(), mid_temps.max()))	        

	    
# animating 

images = []
fig, ax=plt.subplots()
print(np.shape(all_states))
for t in range(T):
	line, = [ax.imshow(all_states[t], cmap='YlOrRd',vmin=cold, vmax=hot)]
	title = ax.text(int(n/2),-1,"Time: {}".format(t+1), size=plt.rcParams["axes.titlesize"],ha="center")
	images.append([line, title])

plt.colorbar(line,)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
anim = animation.ArtistAnimation(fig,images,interval=50, blit=False, repeat = False)
anim.save('anim_q9.mp4', writer=writer)
plt.show()

