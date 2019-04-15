'''
Created on Nov 12, 2017

@author: Owen
'''
import math
import physics_objects as pho
import graphics as gr
import collision as coll
import time

# build the obstacle course
def buildGame(win, x0, y0, width, height):
    floorBot =  pho.Floor(win, x0, y0, width, height)
    floorTop =  pho.Floor(win, x0, y0+50, width, height)
    wallLeft  = pho.Wall(win, x0, y0+25, height-1, width)
    wallRight = pho.Wall(win, x0+49, y0+25, height, width)
    
    flippedHouse = pho.FlippedHouse(win, 35, 35, 5, 5) 
    blockMid = pho.Block(win, 25, 25, 5,5)
    blockML =  pho.Block(win, 10,25, 5,5)
    blockMR =  pho.Block(win, 40,25, 5,5)
    blockBR = pho.Block(win, 30,40,5,5)
    blockTR = pho.Block(win,10,10,5,5)
    
    field = [floorBot, floorTop, wallLeft, wallRight, blockMid, blockML,
             blockMR, blockBR,blockTR]
#    field = [flippedHouse]
    
    for item in field:
        item.draw();
        item.setElasticity(1.1)
    
    return field
    

def launch( ball, x0, y0, dx, dy, forceMag ):

    d = math.sqrt(dx*dx + dy*dy)
    dx /= d
    dy /= d

    fx = dx * forceMag
    fy = dy * forceMag

    ball.setElasticity( 0.9 )
    ball.setPosition( (x0, y0) )
    ball.setForce( (fx, fy) )

    for i in range(5): 
        ball.update(.02)

    ball.setForce( (0., 0.) )
    ball.setAcceleration( (0., -1.) )

# main code

def keyInput(win, ball, obstacles, key):
    '''
      Interprets the pressed key and performs an action accordingly
    '''
    if key == 'w':
        ball.setVelocity((0,10))
    elif key == 'd':
        ball.setVelocity((10,0))
    elif key == 's':
        ball.setVelocity((0,-10))
    elif key == 'a':
        ball.setVelocity((-10,0))
    elif key == 'r':
        launch(ball, 25, 45, 1, 0, 200)
    elif key == 'c':
        ball.randomFill()
    elif key == 'v':
        for item in obstacles:
            item.randomFill()

def main():
    win = gr.GraphWin( 'Pin-Ball', 500, 500, False )
    obstacles = buildGame(win, 0, 0, 50, 2)
    
    ball = pho.Ball(win, 25, 45)
    ball.draw()
    launch(ball, 25, 45, 1, 0, 200)
    
    dt = 0.01
    frame = 0
    
    while win.checkMouse() == None:
        time.sleep(.0001)
        collided = False
        
        for item in obstacles:
                if(coll.collision(ball, item, dt)):
                    collided = True

        if collided == False: 
            ball.update(dt)

        if frame % 10 == 0:
            win.update()

        frame += 1    
        
        key = win.checkKey() 
        keyInput(win, ball, obstacles, key)

        if((ball.getPosition()[0]) > 50 or (ball.getPosition()[1] > 50)):
            launch(ball, 25, 45, 1, 0, 200)
        
            

if __name__ == "__main__":
    main()