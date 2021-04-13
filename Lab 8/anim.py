import numpy as np
import turtle as t
import random
n = 25

def walking(col, n):
    
    #setup for turtle
    t.setpos(0,0)
    t.shape("arrow")
    t.color(col)
    t.speed('slow')
    #initiate the steps
    steps = 0
    step_size = 30
    t.delay(40)
    t.dot(20,'turquoise')
    
    while steps<n:
        choice = np.random.randint(4, size=1)
        if choice == 0:
            t.forward(step_size)  
            t.dot(5,'red')        
            steps+=1
        elif choice == 1:
            t.right(90)
            t.forward(step_size)
            t.dot(5,'red')  
            steps+=1
        elif choice == 2:
            t.left(90)
            t.forward(step_size)
            t.dot(5,'red')  
            steps+=1
        else:
            t.left(180)
            t.forward(step_size)
            t.dot(5,'red')  
            steps+=1
    
    t.done()
    
    

if __name__ == "__main__":
    walking("blue", n)