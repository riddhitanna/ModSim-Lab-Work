import numpy as np
import matplotlib.pyplot as plt
import pylab as pyl
import matplotlib.animation as animation
import random

empty = 0
tree = 1
burning = 2

# probability that a tree is immune from burning by a tree or lightning
probImmune = 0.25

# probability of lightning hitting a site
probLightning = 0.0000001

# probability that a tree is burning initially.
probBurning = 0.8

# probability that a site is initially occupied by tree
probTree = 0.8

class Cell:
    def __init__(self, x, y, state=tree):
        self.x = x
        self.y = y
        if random.uniform(0,1) < probTree:
            if random.uniform(0,1) < probBurning:
                print('Im a BURNING tree')
                self.state = burning
            else:
                print('Im a tree')
                self.state = tree

        else:
            print('Im an empty cell')
            self.x = x
            self.y = y
            self.state = empty

    def setState(self, N, E, S, W):
        """
        set the state of site at time t+1
        input :

        N, NE, E, SE, S, SW, W, NW = temperatures at the neighbour cells
        diffRate = rate of diffusion
        siteTemp = temperature of the site at time t
        ouput : 

        temperature of site at time t+1 

        """
    
     
        if (self.state == burning):
            print('becoming empty')
            self.state = empty 
            

        if self.state == empty:
            self.state = empty

        count = 0
        if self.state == tree:
            if N == burning:
                count = count + 1 
            if S == burning:
                count = count + 1 
            if E == burning:
                count = count + 1 
            if W == burning:
                count = count + 1 

            if random.uniform(0,1) > count/4:
                self.state = tree
            else:
                self.state = burning

        if self.state == tree:
            if random.uniform(0,1) < probLightning*(1-probImmune):
                print('lightning')
                self.state = burning
            else:
                self.state = self.state
                     
        return 


n = 50
t = 50
bar = []

for i in range(n):
    for j in range(n):
        bar.append(Cell(i,j))
bar = np.reshape(np.array(bar), [n,n])



all_states = np.zeros([t,n,n])

for t in range(t):
    for i in range(n):
        for j in range(n):
            all_states[t][i][j] = bar[i][j].state
            


for t in range(1,t):
        count=0
            
        for i in range(1,n-1):
                for j in range(1,n-1):                   
                    bar[i][j].setState(bar[i-1][j].state, bar[i][j+1].state, bar[i+1][j].state, bar[i][j-1].state)
                    all_states[t][i][j] = bar[i][j].state
                    #print(all_states[t][i][j]-all_states[t-1][i][j])
                    if(abs(all_states[t][i][j]-all_states[t-1][i][j])<0.001):
                        count=count+1

        for i in range(n):
            bar[i][n-1].state = bar[i][1].state
            bar[i][0].state = bar[i][n-2].state
            all_states[t][i][n-1] = bar[i][n-1].state
            all_states[t][i][0] = bar[i][0].state

        for j in range(n):
            bar[0][j].state = bar[n-2][j].state
            bar[n-1][j].state = bar[1][j].state
            all_states[t][0][j] = bar[0][j].state
            all_states[t][n-1][j] = bar[n-1][j].state
        
        #equilibrium
        if(count==(n-2)*(n-2)):
            print("Equilibrium state is achieved at time: ",t)
            break
            
             
images = []
fig, ax=plt.subplots()

for t in range(t):
    line, = [ax.imshow(all_states[t], cmap='binary',vmin=empty, vmax=burning)]
    title = ax.text(int(n/2),-1,"Time: {}".format(t+1), size=plt.rcParams["axes.titlesize"],ha="center")
    images.append([line, title])

    # fig = plt.imshow(all_states[t], cmap='YlOrRd',vmin=0, vmax=50)
    # ax.set_title('Time = {}'.format(t))
    #plt.title('Equilibrium reached at time {}'.format(equi))
    #plt.title('Time = {}'.format(t))


plt.colorbar(line,)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
anim = animation.ArtistAnimation(fig,images,interval=300, blit=False, repeat = False)
anim.save('forest_neigh_prop.mp4', writer=writer)
plt.show()

