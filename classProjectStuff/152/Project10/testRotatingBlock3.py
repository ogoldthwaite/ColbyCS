# Bruce A. Maxwell
# Fall 2015
# CS 151S Project 10
#
# third test function for RotatingBlock, testing collisions
#
# Updated for Python3 by Caitrin Eaton
# 15 November 2017


import graphics as gr
import physics_objects as pho
import collision as coll
import math
import time

            
def test():
    win = gr.GraphWin('rotator', 500, 500, False)

    block = pho.RotatingBlock(win,  25, 25, 20, 10 )
    block.draw()
    block.setRotVelocity(109)

    ball = pho.Ball( win, 30, 45 )
    ball.setAcceleration( (0, -10) )
    ball.draw()

    floorBot =  pho.Floor(win, 0, 0, 50, 2)
    floorBot.draw()

    dt = 0.02
    for i in range(360):
        block.update(dt)
        time.sleep(.001)
        
        if coll.collision( ball, block, dt ):
            print('collision')
        else:
            ball.update( dt )
            
        #Testing for floor collision!
        if coll.collision( ball, floorBot, dt ): 
            print('collision')
        else:
            ball.update( dt )

        if i % 10:
            win.update()
            time.sleep(0.01)
            
        if win.checkMouse() != None:
            break

    win.getMouse()
    win.close()

if __name__ == "__main__":
    test()
    