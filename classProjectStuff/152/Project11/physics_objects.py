'''
Created on Nov 12, 2017

@author: Owen
'''
import graphics as gr
import random as rand
import math
import time
from project10.graphics import color_rgb

class Thing:
    def __init__(self, win, the_type, pos = [0,0], mass = 1, radius = 1):
        self.type = the_type
        self.mass = 1
        self.radius = radius
        self.position = pos
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.force = [0,0]
        self.elasticity = 1 #energy retained after collision
        self.scale = 10
        self.win = win
        self.vis = [] #probably need to change to something later
    
    def undraw(self):
        for item in self.vis:
            item.undraw()
    
    def colorItem(self, color):
        '''
          Helper method that just sets the fill
        '''
        for item in self.vis:
            item.setFill(color)
            
    #def properLocation(self):
        '''
          Sets object in the position so that it properly interacts with the environment
        '''
        #self.setPosition((self.getPosition()[0], (self.win.getHeight()/self.scale) - self.getPosition()[1]))
        
    def getFill(self):
        '''
          Returns the fill color of the item.
        '''
        return self.vis[0].getFill()
            
    
    def randomFill(self):
        '''
          Gives the object a random fill color
        '''         
        r = rand.randint(1,255)
        b = rand.randint(1,255)
        g = rand.randint(1,255)
        color = color_rgb(r,b,g)        
            
        for item in self.vis:
            if item.getFill() == color:
                self.randomFill()
            else:
                item.setFill(color)
        
        #Get those Sets!
    def getPosition(self):
        return tuple(self.position)

    def setPosition(self, p):
        self.position[0] = p[0]
        self.position[1] = p[1]

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
        
    def getElasticity(self):
        return self.elasticity
    
    def setElasticity(self, e):
        self.elasticity = e
        
    def getType(self):
        return self.type
    
    def setType(self, t):
        self.type = t      
        
    def draw(self):
        for item in self.vis:
            item.undraw()
            item.draw(self.win)    
            
    def update(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

        dx = self.velocity[0] * dt * self.scale
        dy = -self.velocity[1] * dt * self.scale

        for item in self.vis:
            item.move(dx,dy)
            
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        self.velocity[0] += dt * (self.force[0]/self.mass)
        self.velocity[1] += dt * (self.force[1]/self.mass)

        self.velocity[0] *= .998
        self.velocity[1] *= .998 
        

class Ball(Thing):
    def __init__(self, win, x0 = 0, y0 = 0, mass = 1, radius = 1):        
        Thing.__init__(self, win, "ball",  pos = [x0,y0], mass = mass, radius =  radius)
        
        self.vis = [ gr.Circle( gr.Point(self.position[0]*self.scale, win.getHeight()-self.position[1]*self.scale), 
                    self.radius * self.scale ) ]
                    
        self.colorItem("black")            

    def setPosition(self, p):
        self.position[0] = p[0]
        self.position[1] = p[1]

        for item in self.vis:
            c = item.getCenter()
            dx = self.scale * p[0] - c.getX()
            dy = self.win.getHeight() - self.scale * p[1] - c.getY()
            item.move(dx, dy)
        
class Floor(Thing):
    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "floor", [x0,y0])
        self.width = length
        self.height = thickness
        
        self.vis = [ gr.Rectangle(gr.Point( (x0*self.scale), (win.getHeight() - (y0 + thickness/2.0)*self.scale) ),
                     gr.Point( ((x0 + length)*self.scale), (win.getHeight() - (y0 - thickness/2)*self.scale)) ) ]
      
        self.colorItem("black")
        #self.properLocation()
      
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
        
class Wall(Thing):
    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "wall", [x0,y0])
        self.width = length
        self.height = thickness
        
        self.vis = [ gr.Rectangle(gr.Point( (x0*self.scale), (win.getHeight() - (y0 + thickness/2.0)*self.scale) ),
                     gr.Point( ((x0 + length)*self.scale), (win.getHeight() - (y0 - thickness/2)*self.scale)) ) ]
        
        self.colorItem("black")
        self.properLocation()
        
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
    
    def properLocation(self):
        '''
          Sets object in the position so that it properly interacts with the environment
        '''
        self.setPosition((self.getPosition()[0], (self.win.getHeight()/self.scale) - self.getPosition()[1]))        

class Block(Thing):
    def __init__(self, win, x0, y0, length, height):
        Thing.__init__(self, win, "block", [x0, y0])       
        self.width = length
        self.height = height
        
        self.vis = [ gr.Rectangle(gr.Point( (x0-self.width/2)*self.scale, (y0-self.height/2)*self.scale ),
                     gr.Point( (x0+self.width/2)*self.scale, (y0+self.height/2)*self.scale )) ]
      
        self.colorItem("black")
        self.properLocation()
        
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
    
    def properLocation(self):
        '''
          Sets object in the position so that it properly interacts with the environment
        '''
        #self.setPosition((self.getPosition()[0], (self.win.getHeight()/self.scale) - self.getPosition()[1]))      
    
class FlippedHouse(Thing):    
    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "block", [x0,y0])       
        self.width = length
        self.height = thickness
        
        initPoint = gr.Point( (x0-self.width/2)*self.scale, (y0-self.height/2)*self.scale )
        secPoint = gr.Point( (x0-self.width/2)*self.scale + 25, (y0-self.height/2)*self.scale + 25)
        thirdPoint = gr.Point( (x0-self.width/2)*self.scale + 50, (y0-self.height/2)*self.scale)
        fourthPoint = gr.Point( (x0-self.width/2)*self.scale + 50, (y0-self.height/2)*self.scale - 50)
        fifthPoint = gr.Point( (x0-self.width/2)*self.scale, (y0-self.height/2)*self.scale - 50)    
            
        self.vis = [ gr.Polygon([initPoint,secPoint,thirdPoint,fourthPoint,fifthPoint]) ]
        
        self.properLocation()
        self.colorItem("black")
            
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
    
    def properLocation(self):
        '''
          Sets object in the position so that it properly interacts with the environment
        '''
        self.setPosition((self.getPosition()[0], (self.win.getHeight()/self.scale) - self.getPosition()[1]))
        
class RotatingBlock(Thing):
    def __init__(self, win, x0, y0, width, height, Ax = None, Ay = None):        
        Thing.__init__(self, win, "rotating block", pos=[x0, y0])
        #self.win = win
        self.width = width
        self.height = height
        #self.pos = [x0,y0]
        self.points = [ [-width/2, - height/2], [width/2, -height/2], 
                        [width/2, height/2], [-width/2, height/2] ]
        self.angle = 0.0
        self.rvel = 0.0
        self.drawn = False
        if((Ax != None) and (Ay != None)):
            self.anchor = [Ax, Ay]
        else:
            self.anchor = [x0, y0]
            
    def toRadians(self, value):
        return (value*math.pi/180.0)
        
    
    def draw(self):
        for item in self.vis:
            item.undraw()
        
        self.render()
        
        for item in self.vis:
            item.draw(self.win)
        
        self.drawn = True
        
    def rotate(self, val):   
        self.angle += val
        
        if self.drawn:
            self.draw() 
        
    def render(self):
        theta = self.toRadians(self.angle)
        cth = math.cos(theta)
        sth =  math.sin(theta)
        pts = []
        
        for vertex in self.points:
            x = self.position[0] + vertex[0] - self.anchor[0]
            y = self.position[1] + vertex[1] - self.anchor[1]

            xt = (x * cth) - (y * sth)
            yt = (x * sth) + (y * cth) 

            x = xt + self.anchor[0]
            y = yt + self.anchor[1]

            pts.append(gr.Point(self.scale * x, self.win.getHeight() - self.scale * y))

        self.vis = [ gr.Polygon(pts[0], pts[1], pts[2], pts[3]) ]
        
        if(self.rvel == 0):
            self.colorItem("white")
        else:
            self.randomFill()
        
        
    def update(self, dt):
        '''
          Updates This with time step dt, overrides inherited update to account for rvel
        '''
        da = self.rvel * dt
        
        if( da != 0):
            self.rotate(da)
        
        Thing.update(self,dt)
        
    
    def getAngle(self):
        return self.angle
    
    def setAngle(self, val):
        self.angle = val
        
        if self.drawn:
            self.draw()
            
    def getAnchor(self):
        return self.anchor
    
    def setAnchor(self, x0, y0):
        self.anchor = [x0,y0]
        
    def getRotVelocity(self):
        return self.rvel
    
    def setRotVelocity(self, vel):
        self.rvel = vel
        
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
        

        
        
        