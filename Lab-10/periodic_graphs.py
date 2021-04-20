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

# probability that the tree adjacent will burn 
burnProbability = 0.1

# probability of lightning hitting a site
probLightning = 0.0000001

# probability that a tree is burning initially.
probBurning = 0.0005

# probability that a site is initially occupied by tree
probTree = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

class Cell:
    def __init__(self, x, y, p,state=tree):
        self.x = x
        self.y = y
        if random.uniform(0,1) < probTree[p]:
           if random.uniform(0,1) < probBurning:
              
               self.state = burning
           else:
               
               self.state = tree
        else:
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
           
            self.state = empty 
            

        if self.state == empty:
            self.state = empty

        if self.state == tree:
            if N == burning or S == burning or E == burning or W == burning:
                if random.uniform(0,1) < probImmune:
                    self.state = tree
                else:
                    self.state = burning

            elif random.uniform(0,1) < probLightning*(1-probImmune):
                
                self.state = burning
            else:
                self.state = self.state
                     
        return 


n = 50
T = 50
bar = []

for i in range(n):
    for j in range(n):
        bar.append(Cell(i,j,0))
bar = np.reshape(np.array(bar), [n,n])



all_states = np.zeros([T,n,n])

for t in range(T):
    for i in range(n):
        for j in range(n):
            all_states[t][i][j] = bar[i][j].state
          
sims = 5
probs = np.array([[0 for x in range(sims)] for y in range(len(probTree))])

for p in range(len(probTree)): 
    n = 50
    T = 50
    bar = []

    for i in range(n):
        for j in range(n):
            bar.append(Cell(i,j, p))
    bar = np.reshape(np.array(bar), [n,n])

    init_forest_cov = 0
    for s in range(sims):
        for i in range(1,n-1):
                for j in range(1,n-1): 
                    if bar[i][j].state != empty:
                        init_forest_cov = init_forest_cov + 1
        print(init_forest_cov,'initial')

        all_states = np.zeros([T,n,n])
        print(np.shape(all_states))
        for t in range(T):
            for i in range(n):
                for j in range(n):
                    all_states[t][i][j] = bar[i][j].state


        forest_cov = 0

        for t in range(1,T):

                count=0
                for i in range(1,n-1):
                        for j in range(1,n-1):                   
                            bar[i][j].setState(bar[i-1][j].state, bar[i][j+1].state, bar[i+1][j].state, bar[i][j-1].state)
                            all_states[t][i][j] = bar[i][j].state

                # periodic boundary condition

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


        
        print(forest_cov,'before loop')
        for i in range(1,n-1):
                for j in range(1,n-1): 
                    if bar[i][j].state != empty:
                        forest_cov = forest_cov + 1

        print(forest_cov, probTree[p])
        probs[p][s] = forest_cov



means = np.zeros(len(probs))
for i in range(len(means)):
    means[i] = probs[i].mean()

plt.plot(probTree,means/((n-1)*(n-1)), 'b-o')

plt.xlabel('Initial density of trees')
plt.ylabel('Final density of trees')
#plt.xticks(ticks=np.arange(0,9),labels=probs)
plt.savefig('neigh_burn_graph.eps')
plt.show()        

