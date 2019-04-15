'''
Created on Nov 5, 2017

@author: Owen
'''

import graphics as gr
from random import *

class Ball:
    def __init__(self, win):
        self.mass = 1
        self.radius = 1
        self.position = [0,0]
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.force = [0,0]
        self.scale = 10
        self.win = win
        self.vis = [ gr.Circle( gr.Point(self.position[0]*self.scale, win.getHeight()-self.position[1]*self.scale), 
                    self.radius * self.scale ) ]

    def draw(self):
        for item in self.vis:
            item.draw(self.win) 

    #Get those Sets!
    def getPosition(self):
        return tuple(self.position)

    def setPosition(self, p):
        self.position[0] = p[0]
        self.position[1] = p[1]

        for item in self.vis:
            c = item.getCenter()
            dx = self.scale * p[0] - c.getX()
            dy = self.scale * p[1] - c.getY()
            item.move(dx, dy)

    def getVelocity(self):
        return tuple(self.velocity)

    def setVelocity(self, v):
        self.velocity[0] = v[0]
        self.velocity[1] = v[1]

    def getAcceleration(self):
        return tuple(self.acceleration)

    def setAcceleration(self, a):
        self.acceleration[0] = a[0]
        self.acceleration[1] = a[1]

    def getForce(self):
        return tuple(self.force)

    def setForce(self, f):
        self.force[0] = f[0]
        self.force[1] = f[1]

    def getMass(self):
        return self.mass

    def setMass(self, m):
        self.mass = m
        
    def getRadius(self):
        return self.radius
    
    def setRadius(self, r):
        self.radius = r

    def update(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

        dx = self.velocity[0] * dt * self.scale
        dy = self.velocity[1] * dt * self.scale

        for item in self.vis:
            item.move(dx,dy)

        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        self.velocity[0] += dt * (self.force[0]/self.mass)
        self.velocity[1] += dt * (self.force[1]/self.mass)

        self.velocity[0] *= .998
        self.velocity[1] *= .998
    
    def randomFill(self):
        num = randint(0,50)
        if(num <= 10):
            fill = "yellow"
        elif(num <= 20):
            fill = "purple"
        elif(num <= 30):
            fill = "blue"
        elif(num <= 40):
            fill = "red"
        elif(num <= 50):
            fill = "pink"
        else:
            fill = "black"
            
        for item in self.vis:
            item.setFill(fill)
            
class Floor:
    def __init__ (self, win, x0, y0, length=50, thickness=5, fill="black"):
        self.win = win
        self.scale = 10
        self.position = [x0, y0]
        self.length = length
        self.thickness = thickness
        self.fill = fill
        self.vis = [ gr.Rectangle(gr.Point( (x0*self.scale), (win.getHeight() - (y0 + thickness/2.0)*self.scale) ),
                     gr.Point( ((x0 + length)*self.scale), (win.getHeight() - (y0 - thickness/2)*self.scale)) ) ]
      
        for item in self.vis:
            item.setFill(fill)

    def draw(self):
        for item in self.vis:
            item.draw(self.win)
            
    def collision(self, item): 
        '''
          Returns true if there is a collision between floor and item, false otherwise
          Uses getRadius, so must be changed if you want to use something other than ball object
        '''
        dist = abs( (item.getPosition()[1] + self.thickness) - self.position[1]*self.scale )
        if(dist <= (item.getRadius() + self.thickness/2)):
            return True
        else:
            return False
        
class Wall:
    def __init__ (self, win, x0, y0, height=50, thickness=5, fill="black"):
        self.win = win
        self.scale = 10
        self.position = [x0, y0]
        self.height = height
        self.thickness = thickness
        self.fill = fill
        self.vis = [ gr.Rectangle(gr.Point( ((x0+thickness/2.0)*self.scale), win.getHeight() - (y0*self.scale) ),
                      gr.Point( (x0-thickness/2.0)*self.scale, win.getHeight() - (y0+height)*self.scale)) ]
        
        for item in self.vis:
            item.setFill(fill)

    def draw(self):
        for item in self.vis:
            item.draw(self.win)
            
    def collision(self, item): 
        '''
          Returns true if there is a collision between wall and item, false otherwise
          Uses getRadius, so must be changed if you want to use something other than ball object
        '''
        dist = abs(self.position[0] - item.getPosition()[0])
        if(dist <= (item.getRadius() + self.thickness/2)):
            return True
        else:
            return False
        
        