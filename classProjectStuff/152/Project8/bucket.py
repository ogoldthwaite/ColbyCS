'''
Created on Nov 6, 2017

@author: Owen
'''
import graphics as gr
import physics_objects as pho
from time import *
from random import *


def main():
    win = gr.GraphWin("Bucket", 500, 500)

    floor = pho.Floor(win, 0, 5, 50, 5)
    floor.draw()
    wall_1 = pho.Wall(win, 0, 0, 50, 5)
    wall_1.draw()
    wall_2 = pho.Wall(win, 50, 0, 50, 5)
    wall_2.draw()
    
    ballList = []
    for i in range(5):
        ballList.append(pho.Ball(win))
        ballList[i].setVelocity([randint(-10,10), 0])
        ballList[i].setAcceleration([0, randint(1,10)])
        ballList[i].randomFill()
        ballList[i].draw()
        
    lossFact = .95
    dt = 0.1
    count = 0
        
    while win.checkMouse() == None:
#        print(win.getMouse())
        for ball in ballList:
            ball.update(dt)
        
#         if(count >= 300):
#             ball.setVelocity([0,0])
#             ball.setPosition([randint(0,50), randint(4.0,5.0)])
#             count = 0
        
            if(floor.collision(ball)):
                v = ball.getVelocity()
                ball.setVelocity([v[0], -v[1]*lossFact])
                ball.randomFill()
                while(floor.collision(ball)):
                    ball.update(.001)
                
            if(wall_1.collision(ball)):
                v = ball.getVelocity()
                ball.setVelocity([-v[0]*lossFact, v[1]])
                ball.randomFill()
                while(wall_1.collision(ball)):
                    ball.update(.001)

            if(wall_2.collision(ball)):
                v = ball.getVelocity()
                ball.setVelocity([-v[0]*lossFact, v[1]])
                ball.randomFill()
                while(wall_2.collision(ball)):
                    ball.update(.001)
        
               
        
        count += 1
        win.update()
        sleep(.025)
    
    win.close()













if __name__=="__main__":
    main()