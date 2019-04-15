'''
Created on Nov 28, 2017

@author: Owen
'''
import graphics as gr
import time
import math


class RotatingLine:
    def __init__(self, win, x0, y0, length, Ax = None, Ay = None):
        self.win = win
        self.pos = [x0, y0]
        self.length = length
        self.angle = 0.0
        self.rvel = 0.0
        self.scale = 10
        self.drawn = False
        self.vis = []
        self.points = [ [-length/2.0, 0.0], [length/2.0, 0.0] ]
        if((Ax != None) and (Ay != None)):
            self.anchor = [Ax, Ay]
        else:
            self.anchor = [x0, y0]
            
    def toRadians(self, value):
        return (value*math.pi/180.0)
    
    def render(self):
        theta = self.toRadians(self.angle)
        cth = math.cos(theta)
        sth =  math.sin(theta)
        pts = []
        
        for vertex in self.points:
            x = self.pos[0] + vertex[0] - self.anchor[0]
            y = self.pos[1] + vertex[1] - self.anchor[1]

            xt = (x * cth) - (y * sth)
            yt = (x + sth) + (y * cth) 

            x = xt + self.anchor[0]
            y = yt + self.anchor[1]

            pts.append(gr.Point(self.scale * x, self.win.getHeight() - self.scale * y))

        self.vis = [ gr.Line(pts[0], pts[1]) ]
        
    def rotate(self, val):   
        self.angle += val
        
        if self.drawn:
            self.draw()
        
    def draw(self):
        for item in self.vis:
            item.undraw()
        
        self.render()
        
        for item in self.vis:
            item.draw(self.win)
        
        self.drawn = True
        
    def getAngle(self):
        return self.angle
    
    def setAngle(self, val):
        self.angle = val
        
        if self.drawn:
            self.draw()
            
    def setAnchor(self, x0, y0):
        self.anchor = [x0,y0]          
        
def test1():
    win = gr.GraphWin('line thingy', 500, 500, False)

    line = RotatingLine(win, 25, 25, 10)
    line.draw()
    #line.setAnchor(20, 25)
    
    while win.checkMouse() == None:
        line.rotate(3)
        time.sleep(0.008)
        win.update()

    win.getMouse()
    win.close()

if __name__ == "__main__":
    test1()