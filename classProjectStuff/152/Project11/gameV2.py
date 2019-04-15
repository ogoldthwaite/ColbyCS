'''
Created on Dec 8, 2017

@author: Owen
'''
import time
import math
import physics_objects as pho
import random as rand
import graphics as gr
import collision as coll
import ship as sh
import threading as th
import tkinter as tk

class Game(tk.Tk):
    def __init__(self, threaded = False):
        #tk.Tk.__init__(self)
        self.win = gr.GraphWin('GameV2', 500, 500, False)
        self.ship = sh.Ship(self.win, 10, 15)
        self.vicColor = gr.color_rgb(249,22,174)
        self.bullets = []
        self.obstacles = self.buildObstacles()
        self.walls = self.buildWalls(50, 2)
        self.threaded = threaded
        self.time = 0
        self.scores = self.readHighscore()
        self.highscore = ""
    
    def writeHighscore(self):
        '''
          Writes the score of the player to the highscores.txt file
        '''
        self.highscore = time.time() - self.time
        file = open('highscores.txt', 'a')
        file.write(str(self.highscore) + "\n")
        file.close()
    
    def readHighscore(self):
        '''
          reads in all past highscores and sorts them to show on end screen, also
          sorts the file itself for easy viewing of all scores
        '''
        scores = []
        
        file = open('highscores.txt', 'r')
        for line in file:
            scores.append(float(line))
        scores.sort()
        file.close()
        
        file = open('highscores.txt', 'w')        
        for score in scores:
            file.write(str(score) + "\n")
        file.close()
        
        return scores
        
    def buildWalls(self, width, height, x0 = 0, y0 = 0):
        '''
          Generates the walls that the bullet bounces off of
        '''
        floorBot =  pho.Floor(self.win, x0, y0-1, width, height)
        floorTop =  pho.Floor(self.win, x0, y0+51, width, height)
        wallLeft  = pho.Wall(self.win, x0-1, y0+25, height-1, width)
        wallRight = pho.Wall(self.win, x0+51, y0+25, height-1, width)
    
        walls = [floorBot, floorTop, wallLeft, wallRight] 
        return walls  

    def buildObstacles(self):
        '''
          Makes the obstacles that the bullet needs to hit
        '''
        blockRotMid = pho.RotatingBlock(self.win, 25, 25, 2, 10 )
        blockRotMid.setRotVelocity(109)
    
        blockRotOut = pho.RotatingBlock(self.win, 25, 45, 2, 7 )
        blockRotOut.setAnchor( 25, 25 )
        blockRotOut.setRotVelocity(15)
        
        coin = rand.randint(1,2)
        if(coin == 1):
            blockTR = pho.RotatingBlock(self.win, 40,40,5,5)
            blockBL = pho.RotatingBlock(self.win,10,10,5,5)
            blockTL = pho.RotatingBlock(self.win, 10,40,5,5)
            blockBR = pho.RotatingBlock(self.win,40,10,5,5)
        else:
            blockTR = pho.RotatingBlock(self.win, 40,25,5,5)
            blockBL = pho.RotatingBlock(self.win,25,40,5,5)
            blockTL = pho.RotatingBlock(self.win, 10,25,5,5)
            blockBR = pho.RotatingBlock(self.win,25,10,5,5)
    
        obstacles = [blockRotMid, blockRotOut, blockTR, blockBL, blockTL,blockBR]
    
        for item in obstacles:
            item.colorItem("white")
    
            return obstacles     
         
    def singleRandomFill(self, item):
        '''
          Gives the zelle graphics object a random fill color
        '''         
        r = rand.randint(1,255)
        b = rand.randint(1,255)
        g = rand.randint(1,255)
        color = gr.color_rgb(r,b,g)        
            
        if item.getFill() == color:
            self.singleRandomFill(item)
        else:
            item.setFill(color)    
        
    def testWrap(self): 
        '''
          Wraps ship around screen
        '''
        winWidth = 50 
        winHeight = 50
    
        moveIt = False
        p = list(self.ship.getPosition())
         
        if(p[0] < 0):
            p[0] += winWidth
            moveIt = True
        elif(p[0] > winWidth):
            p[0] -= winWidth
            moveIt = True
            
        if(p[1] < 0):
            p[1] += winHeight
            moveIt = True
        elif(p[1] > winHeight):
            p[1] -= winHeight
            moveIt = True
            
        if(moveIt):
            self.ship.setPosition(p)
            self.ship.draw()
            moveIt = False
            
    def shoot(self):
        '''
          Shoots a ball from the ship!
        '''
        pos = self.ship.getPosition()
        ball = pho.Ball(self.win, pos[0], pos[1], radius = .25)
        color = gr.color_rgb(249,22,174)
        ball.colorItem(color)
        ball.setElasticity(0.9)
        ball.setVelocity((self.ship.getVelocity()[0] *15, self.ship.getVelocity()[1] *15))
        ball.draw()
        self.bullets.append(ball)        

    def undrawAll(self):
        '''
          Undraws everything
        '''
        self.ship.undraw()
        for item in self.obstacles:
            item.undraw()
        for item in self.walls:
            item.undraw

    def updateMap(self, dt):
        '''
          Updates stuff, and checks to see if all obstacles are win color.
        '''
        count = 0
    
        self.ship.update(dt)
    
        for item in self.obstacles:
            item.update(dt)
            if item.getFill() == self.vicColor:
                count += 1   
    
        for item in self.bullets:
            item.update(dt) 
        
        if count == len(self.obstacles) - 2:
            return True
        else:
            return False

    def checkColl(self, things, edit = False):
        '''
          Checks for collision and updates things accordingly
        '''
        dt = 0.01
        if(not(edit)):
            for item in things:
                item.update(dt)
                if(self.bullets != [] and coll.collision(self.bullets[-1], item, dt)):
                    return
        else:
            for item in things:
                item.update(dt)
                if(self.bullets != [] and coll.collision(self.bullets[-1], item, dt)):
                    color = gr.color_rgb(249,22,174)
                    if item.getFill() == color:
                        item.colorItem("white")
                    else:
                        item.colorItem(self.vicColor)
                        return

    def useKey(self, key):
        '''
          Performs a specific action based upon the value of key. 
          Left/Right rotate, up accelerates forward, down brings to a sudden stop.
        '''
        delta = .5
        gamma = 5
        win = self.win
        ship = self.ship    
    
        if(key == "q"):
            self.readHighscore()
            win.close()
            exit()
        elif(key == "Left"):
            ship.setRotVelocity(ship.getRotVelocity() + gamma)
            ship.setFlickerOn()
        elif(key == "Right"):
            ship.setRotVelocity(ship.getRotVelocity() - gamma)
            ship.setFlickerOn()
        elif(key == "Up"):
            a = ship.getAngle()
            theta = a * (math.pi/180.0)
            v =  ship.getVelocity()
            velX = v[0] + math.cos(theta) * delta
            velY = v[1] + math.sin(theta) * delta
            ship.setVelocity((velX, velY))
            ship.setFlickerOn()
        elif(key == "Down"):
            a = ship.getAngle()
            theta = a * (math.pi/180.0)
            v =  ship.getVelocity()
            velX = v[0] + math.cos(theta) * delta
            velY = v[1] + math.sin(theta) * delta
            ship.setVelocity((-velX, -velY))
            ship.setRotVelocity(0)
            ship.setFlickerOn()
        elif(key == "space"):
            self.shoot()
        elif(key == 'r'):
            self.playGame()

    def parrellKeyInput(self):
        '''
          Performs a specific action based upon the value of key in a different thread 
          Left/Right rotate, up accelerates forward, down brings to a sudden stop.
          In testing phase, will be broken up into thread/key later if I can actually
          figure out how to get a thread to work with graphics
        ''' 
        delta = .5
        gamma = 5
        ship = self.ship
        win = self.win
    
        while True:
            key = win.checkKey()
        
            if(key == "q"):
                win.close()
                exit()
            elif(key == "Left"):
                ship.setRotVelocity(ship.getRotVelocity() + gamma)
                ship.setFlickerOn()
            elif(key == "Right"):
                ship.setRotVelocity(ship.getRotVelocity() - gamma)
                ship.setFlickerOn()
            elif(key == "Up"):
                a = ship.getAngle()
                theta = a * (math.pi/180.0)
                v =  ship.getVelocity()
                velX = v[0] + math.cos(theta) * delta
                velY = v[1] + math.sin(theta) * delta
                ship.setVelocity((velX, velY))
                ship.setFlickerOn()
            elif(key == "Down"):
                a = ship.getAngle()
                theta = a * (math.pi/180.0)
                v =  ship.getVelocity()
                velX = v[0] + math.cos(theta) * delta
                velY = v[1] + math.sin(theta) * delta
                ship.setVelocity((-velX, -velY))
                ship.setRotVelocity(0)
                ship.setFlickerOn()
            elif(key == "space"):
                self.shoot(win,ship)

    def phase1(self):
        '''
          First phase, title screen
        '''
        self.win.setBackground("black")
        line1 = gr.Text( gr.Point(250, 25), "The Best Game Ever Made" )
        line1.setSize( 24 )
        line2 = gr.Text( gr.Point(250, 75), "Make sure you're seated!" )
        line2.setSize( 24 )
        line3 = gr.Text( gr.Point(250, 125), "S to Start, Q to Quit!" )
        line3.setSize( 24 )
    
        words = [line1, line2, line3]
    
        for item in words:
            item.draw(self.win)
            self.singleRandomFill(item)
    
        while True:
            for item in words:
                self.singleRandomFill(item)
        
            key = self.win.checkKey()
            if key == 's':
                break
            if key == 'q':
                self.win.close()
                exit()
                return

        for item in words:
            item.undraw()
            
    def phase2(self):
        '''
          Second phase of the game where you actually play
        '''
        self.time = time.time()
        if(self.threaded):
            keyThread = th.Thread(target = self.parrellKeyInput)
            keyThread.start()
    
        self.ship.draw()
        for item in self.walls:
            item.draw()
        for item in self.obstacles:
            item.draw()
    
            frame = 0
            dt = 0.01
            key = ""
            victory = False
    
        while(not(victory)):
            
            if(not(self.threaded)): 
                key = self.win.checkKey()
                if(key == "v"):
                    victory = True
                self.useKey(key)
            
            victory = self.testWrap()
               
            if(frame % 10 == 0):
                self.win.update()
                time.sleep(dt * 0.5)
            if(self.bullets != [] and len(self.bullets) > 1):
                self.bullets[0].undraw()
                self.bullets.remove(self.bullets[0])
            
            self.checkColl(self.walls)
            self.checkColl(self.obstacles, True)
            
            victory = self.updateMap(dt)
            frame += 1
        pass
                  
    def phase3(self):
        '''
          End screen of the game
        '''
        for item in self.obstacles:
            item.undraw()
        for item in self.bullets:
            item.undraw()
            self.ship.undraw()

        line1 = gr.Text( gr.Point(250, 35), "YOU WON!! Press Q to quit" + "\n" + "or R to play again!" )
        line2 = gr.Text( gr.Point(250, 95), "You're Time:" + str(self.highscore))
        line3 = gr.Text( gr.Point(250, 250), "Top 3 Past Times:" +"\n"+ str(self.scores[0])+"\n" + 
                                        str(self.scores[1])+"\n" + str(self.scores[2])+"\n")
        
        words = [line1, line2, line3]
        for item in words:
            self.singleRandomFill(item)
            item.setSize(24)
            item.draw(self.win)
        
        while True:
            for item in words:
                self.singleRandomFill(item)
            key = self.win.checkKey()
            if key == 'q':
                self.win.close()
                exit()
                break
            if key == 'r':
                self.playGame()
        line1.undraw()
    
        self.win.close() 

    def playGame(self):  
        self.win.close()
        self.__init__()
        self.phase1()
        self.phase2()
        self.writeHighscore()
        self.phase3()
        self.readHighscore()
            
def main():
    game = Game()
    game.playGame()
 
if __name__ == "__main__":
    main()
#             
# root = Game()
# root.mainloop()
