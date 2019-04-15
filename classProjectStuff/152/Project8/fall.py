'''
Created on Nov 5, 2017

@author: Owen
'''
import graphics as gr
import physics_objects as pho
from time import *
from random import *
 

def main():
    win = gr.GraphWin("Fall", 500, 500)
    ball = pho.Ball(win)
    ball.setPosition([2.5,4.5])
    ball.setAcceleration([10,10])
    ball.draw()

    

    
    floor = pho.Floor(win, 0, 5, 50, 5)
    floor.draw()
    
    wall = pho.Wall(win, 50, 0, 50, 5)
    wall.draw()
    
    dt = 0.1
    
    count = 0
    while win.checkMouse() == None:
#        print(win.getMouse())
        ball.update(dt)
         
#         if(pos[1] > 49):
#             ball.setVelocity([0,0])
#             ball.setPosition([randint(0,50), randint(4.0,5.0)])
        
        if(count >= 300):
            ball.setVelocity([0,0])
            ball.setPosition([randint(0,50), randint(4.0,5.0)])
            count = 0
        
        if(floor.collision(ball)):
            v = ball.getVelocity()
            ball.setVelocity([v[0], -v[1]*.95])
            while(floor.collision(ball)):
                ball.update(.001)
                
        if(wall.collision(ball)):
            v = ball.getVelocity()
            ball.setVelocity([-v[0]*.95, v[1]])
            while(wall.collision(ball)):
                ball.update(.001)
        
               
        
        count += 1
        win.update()
        sleep(.075)
    
    win.close()







if __name__=="__main__":
    main()