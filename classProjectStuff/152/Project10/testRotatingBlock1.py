# Bruce A. Maxwell
# Fall 2015
# CS 151S Project 10
#
# First Test function for the RotatingBlock class

import graphics as gr
import physics_objects as rot
import math
import time

def test():
    win = gr.GraphWin('rotator', 500, 500, False)

    block = rot.RotatingBlock(win,  25, 25, 20, 10 )
    block.draw()
    block.setAngle(45)

    dt = 0.02
    for i in range(360):
        block.rotate(1)
        win.update()
        time.sleep(0.01)
            
        if win.checkMouse() != None:
            break

    win.getMouse()
    win.close()

if __name__ == "__main__":
    test()
    