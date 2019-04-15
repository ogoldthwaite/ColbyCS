'''
Created on Nov 12, 2017

@author: Owen
'''
import graphics as gr
import random as rand

class Thing:
    def __init__(self, win, the_type, position = [0,0], mass = 1, radius = 1):
        self.type = the_type
        self.mass = 1
        self.radius = radius
        self.position = position
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.force = [0,0]
        self.elasticity = 1 #energy retained after collision
        self.scale = 10
        self.win = win
        self.vis = [] #probably need to change to something later
    
    def colorItem(self, color):
        '''
          Helper method that just sets the fill
        '''
        for item in self.vis:
            item.setFill(color)
            
    def properLocation(self):
        '''
          Sets object in the position so that it properly interacts with the environment
        '''
        self.setPosition((self.getPosition()[0], (self.win.getHeight()/self.scale) - self.getPosition()[1]))
        
    
    def randomFill(self):
        '''
          Gives the object a random fill color
        '''
        num = rand.randint(0,50)
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
            if item.getFill() == fill:
                self.randomFill()
            else:
                item.setFill(fill)
        
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
        Thing.__init__(self, win, "ball",  position = [x0,y0], mass = mass, radius =  radius)
        
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
        self.properLocation()
      
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

class Block(Thing):
    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "block", [x0,y0])       
        self.width = length
        self.height = thickness
        
        self.vis = [ gr.Rectangle(gr.Point( (x0-self.width/2)*self.scale, (y0-self.height/2)*self.scale ),
                     gr.Point( (x0+self.width/2)*self.scale, (y0+self.height/2)*self.scale )) ]
      
        self.colorItem("black")
        self.properLocation()
        
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width      
    
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
        
        
        
        
        
        
        
        
        
        
        
        