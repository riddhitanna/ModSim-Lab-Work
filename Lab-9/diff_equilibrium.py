import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

cold = 0
hot = 50
ambient = 25


class Cell:

	def __init__(self, x, y, state=ambient):
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
		self.state = (1-8*diffRate)*self.state + diffRate*(N + NE + E + SE + S + SW + W + NW)


m = 20
n = 20
t = 500
diffRate = 0.125
bar = []

for i in range(m):
	for j in range(n):
		bar.append(Cell(i,j))
bar = np.reshape(np.array(bar), [m,n])

for i in range(m):
	bar[i][n-1].state = 0
	bar[i][0].state = 0
for j in range(n):
	bar[0][j].state = 0
	bar[m-1][j].state = 0

all_states = np.zeros([t,m,n])

for t in range(t):
	for i in range(m):
		for j in range(n):
			all_states[t][i][j] = bar[i][j].state

# applying hot and cold sites to pre-defined cells - this can be changed to random sites or 
# any sites that you wish to 

hot_sites_x = [1, 2, 5]
hot_sites_y = [1, 6, 8]	

cold_sites_x = [0, 11, 15]	
cold_sites_y = [1, 0, 0]

# applying the diffusion simulation
for t in range(0,t):
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
            
            
images = []
fig, ax=plt.subplots()

for t in range(t):
	line, = [ax.imshow(all_states[t], cmap='YlOrRd',vmin=cold, vmax=hot)]
	title = ax.text(int(n/2),-1,"Time: {}".format(t+1), size=plt.rcParams["axes.titlesize"],ha="center")
	images.append([line, title])


plt.colorbar(line,)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
anim = animation.ArtistAnimation(fig,images,interval=50, blit=False, repeat = False)
anim.save('anim_equi_abs_cold.mp4', writer=writer)
plt.show()

