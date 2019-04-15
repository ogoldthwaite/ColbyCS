# Template by Bruce A Maxwell
# Fall 2015
# CS 151S Project 11
#
# Make an Asteroids-like ship move around
#
#
# import useful packages
import math
import time
import graphics as gr
import physics_objects as pho

# make a ship object, treat it as a ball
# but it needs to be able to rotate
# should probably have a parent rotator class that does most of this for you
class Ship(pho.Thing):
    def __init__(self, win, x0=0, y0=0, mass=1, radius=1):
        pho.Thing.__init__(self, win, "ball", pos=[x0, y0], mass=mass, radius=radius)

        # anchor point is by default the center of the ship/circle so we don't need it
        self.angle = 0.
        self.dangle = 0.

        # visualization properties
        # This is a two-part visualization
        # the ship is a triangle
        self.bodypts = [ (radius, 0),
                         (- radius*0.5,   1.732*radius*0.5),
                         (- radius*0.5, - 1.732*radius*0.5) ]
        # the exhaust is another triangle
        self.flamepts = [ (- radius*0.2,   0.2*radius),
                          (- radius*0.2, - 0.2*radius),
                          (- radius*1, 0) ]

        self.scale = 10.
        self.vis = []
        self.drawn = False

        # these are for handling the flicker of the exhaust
        self.flickertime = 6
        self.flicker = False
        self.countdown = 0

    #########
    # these functions are identical to the rotating block
    # a smart coder would make a parent rotator class

    # draw the object into the window
    def draw(self):
        for item in self.vis:
            item.undraw()
        self.render()
        for item in self.vis:
            item.draw(self.win)
        self.drawn = True

    # undraw the object from the window
    def undraw(self):
        for item in self.vis:
            item.undraw()
        self.drawn = False

    # get and set the angle of the object
    # these are unique to rotators
    def getAngle(self):
        return self.angle

    # setAngle has to update the visualization
    def setAngle(self, a):
        self.angle = a
        if self.drawn:
            self.draw()

    # get and set rotational velocity
    def setRotVelocity(self, rv):
        self.dangle = rv # degrees per second

    def getRotVelocity(self):
        return self.dangle

    # incrementally rotate by da (in degrees)
    # has to update the visualization
    def rotate(self, da):
        self.angle += da
        if self.drawn:
            self.draw()

    # special ship methods
    def setFlickerOn(self, countdown = 50):
        self.flicker = True
        self.countdown = countdown

    def setFlickerOff(self):
        self.countdown = 0
        self.flicker = False
        
    # simplified render function since the ship always rotates around its center
    def render(self):

        # get the cos and sin of the current orientation
        theta = math.pi * self.angle / 180.
        cth = math.cos(theta)
        sth = math.sin(theta)

        # rotate each point around the object's center
        pts = []
        for vertex in self.bodypts + self.flamepts:
            # move the object's center to 0, 0, which it is already in model coordinates
            xt = vertex[0]
            yt = vertex[1]

            # rotate the vertex by theta around the Z axis
            xtt = cth*xt - sth*yt
            ytt = sth*xt + cth*yt

            # move the object's center back to its original location
            xf = xtt + self.position[0]
            yf = ytt + self.position[1]

            # create a point with the screen space coordinates
            pts.append( gr.Point(self.scale * xf, self.win.getHeight() - self.scale * yf) )

        # make the two objects
        self.vis = [ gr.Polygon( pts[:3] ), gr.Polygon( pts[3:] ) ]
        self.vis[0].setFill(gr.color_rgb(249,22,174))
        self.vis[0].setOutline("dark red")
        self.vis[1].setOutline("yellow")

    # update the various state variables
    # add a unique flicker touch
    def update(self, dt):
        # update the angle based on rotational velocity
        da = self.dangle * dt
        if da != 0.0: # don't bother updating if we don't have to
            self.rotate( da )
            
        # flicker the flames
        # this should be a field of the object
        if self.flicker and self.countdown > 0:
            if self.countdown % self.flickertime < self.flickertime/2:
                self.vis[1].setFill( 'yellow' )
            else:
                self.vis[1].setFill( 'orange' )
            self.countdown -= 1
        else:
            self.vis[1].setFill( 'white' )

        # call the parent update for the rest of it
        pho.Thing.update(self, dt)

bullets = []

def useKey(key, ship, win):
    '''
      Performs a specific action based upon the value of key
    '''
    delta = .5
    gamma = 1
    
    if(key == "Left"):
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
    elif(key == "space"):
        shoot(win,ship) 
    
        
def testWrap(ship): 
    '''
      Wraps ship around screen
    '''
    winWidth = 50 
    winHeight = 50
    
    moveIt = False
    p = list(ship.getPosition())
         
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
        ship.setPosition(p)
        ship.draw()
        moveIt = False
            
def shoot(win, ship):
    '''
      Shoots a ball from the ship!
    '''
    pos = ship.getPosition()
    ball = pho.Ball(win, pos[0], pos[1], radius = .25)
    ball.colorItem("pink")
    ball.setElasticity(0.9)
    ball.setVelocity((ship.getVelocity()[0] *15, ship.getVelocity()[1] *15))
    ball.draw()
    bullets.append(ball)

def updateMap(dt, ship):
    ship.update(dt)
    for item in obstacles:
        item.update(dt)   
    for item in bullets:
        item.update(dt) 

def main():
    win = gr.GraphWin('Ship', 500, 500, False)

    ship = Ship(win, 25, 25)
    ship.draw()
    
    frame = 0
    dt = 0.01
    key = ""
    
    while(key != "q"):
        key = win.checkKey()
        useKey(key, ship, win)
        testWrap(ship)
               
        if(frame % 10 == 0):
            win.update()
            time.sleep(dt * 0.5)
        if(frame % 1000 == 0 and bullets != []):
            bullets[0].undraw()
            bullets.remove(bullets[0])
            
        updateMap(dt, ship)
        frame += 1
    # all done
    win.close()

if __name__ == "__main__":
    main()