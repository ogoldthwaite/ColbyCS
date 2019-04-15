# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
# Updated for python 3
#
# Used macports to install
#  python36
#  py36-numpy
#  py36-readline
#  py36-tkinter
#
# CS 251
# Spring 2018

import tkinter.filedialog as fd
import tkinter as tk
import numpy as np
import view
import math
import random
import data
import analysis

# create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a tk object, which is the root window
        self.root = tk.Tk()
        self.view = view.View()
        self.baseVRP = self.view.vrp
        # width and height of the window
        self.initDx = width
        self.initDy = height

        # set up the geometry for the window
        self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

        # set the title of the window
        self.root.title("Owen's Totally Radical Window")

        # set the maximum size of the window for resizing
        self.root.maxsize( 1600, 900 )

        # setup the menus
        self.buildMenus()

        # build the controls
        self.buildControls()

        # build the Canvas
        self.buildCanvas()

        # bring the window to the front
        self.root.lift()

        # - do idle events here to get actual canvas size
        self.root.update_idletasks()

        # now we can ask the size of the canvas
        print(self.canvas.winfo_geometry())

        # set up the key bindings
        self.setBindings()

        # set up the application state
        self.objects = [] # list of data objects that will be drawn in the canvas
        self.data = None # will hold the raw data someday.
        self.baseClick = None # used to keep track of mouse movement
        self.showsize = False

        self.lastdialogval = 50 #value entered into the most recent dialog box
        
        # Weird axes matrix, not sure if this is how you're supposed to build it! 
        self.axes = np.matrix([[0,0,0,1],
                               [1,0,0,1],
                               [0,0,0,1],
                               [0,1,0,1],
                               [0,0,0,1],
                               [0,0,1,1]])     

        # self.axes = np.matrix([[0,1,0,0,0,0],
        #                        [0,0,0,1,0,0],
        #                        [0,0,0,0,0,1],
        #                        [1,1,1,1,1,0]])        

        # Stores actual graphical lines
        self.lines = []
        self.distlines = []

        self.buildAxes()

        self.canvas.create_text(950,20, text="Scale Factor: 1.0", font="Times 15", tag="scale_display")
        self.canvas.create_text(950,40, text="X Angle: 0.0", font="Times 15", tag="rotation_display")
        self.canvas.create_text(950,60, text="Y Angle: 0.0", font="Times 15", tag="rotation_display")

    def buildMenus(self):
        
        # create a new menu
        menu = tk.Menu(self.root)

        # set the root menu to our new menu
        self.root.config(menu = menu)

        # create a variable to hold the individual menus
        menulist = []

        # create a file menu
        filemenu = tk.Menu( menu )
        menu.add_cascade( label = "File", menu = filemenu )
        menulist.append(filemenu)

        # create another menu for kicks
        cmdmenu = tk.Menu( menu )
        menu.add_cascade( label = "Command", menu = cmdmenu )
        menulist.append(cmdmenu)

        mathsmenu = tk.Menu( menu )
        menu.add_cascade( label = "Math!", menu = mathsmenu )
        menulist.append(mathsmenu)

        # menu text for the elements
        # the first sublist is the set of items for the file menu
        # the second sublist is the set of items for the option menu
        menutext = [ [ '-', '-', 'Quit  Ctrl-Q', 'Clear  Ctrl-N' ],
                     [ 'Command 1', '-', '-' ],
                     [ 'Range', 'Mean', 'Stdev' ] ]

        # menu callback functions (note that some are left blank,
        # so that you can add functions there if you want).
        # the first sublist is the set of callback functions for the file menu
        # the second sublist is the set of callback functions for the option menu
        menucmd = [ [None, None, self.handleQuit, self.handleClear],
                    [self.handleMenuCmd1, None, None], 
                    [self.handleRange, self.handleMean, self.handleStdev]]
        
        # build the menu elements and callbacks
        for i in range( len( menulist ) ):
            for j in range( len( menutext[i]) ):
                if menutext[i][j] != '-':
                    menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
                else:
                    menulist[i].add_separator()

    # create the canvas object
    def buildCanvas(self):
        self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
        self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
        return

    # build a frame and put controls in it
    def buildControls(self):

        ### Control ###
        # make a control frame on the right
        self.rightcntlframe = tk.Frame(self.root)
        self.rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # make a separator frame
        sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
        sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

        # use a label to set the size of the right panel
        label = tk.Label( self.rightcntlframe, text="Control Panel", width=20 )
        label.pack( side=tk.TOP, pady=10 )

        # make a menubutton
        self.colorOption = tk.StringVar( self.root )
        self.colorOption.set("black")
        colorMenu = tk.OptionMenu( self.rightcntlframe, self.colorOption, 
                                        "black", "blue", "red", "green" ) # can add a command to the menu
        colorMenu.pack(side=tk.TOP)

        # make a button in the frame
        # and tell it to call the handleButton method when it is pressed.
        button = tk.Button( self.rightcntlframe, text="Update Color", 
                               command=self.handleButton1 )
        button.pack(side=tk.TOP)  # default side is top
        
        #Owen's cool data point button! SICK!
        button = tk.Button(self.rightcntlframe, text = "Plot Data", 	
							 command=self.handlePlotData)
        button.pack(side=tk.TOP)

        # Making a list box
        shapelb = tk.Listbox(self.rightcntlframe, exportselection=0, selectmode=tk.BROWSE, height=3)
        shapelb.pack(side=tk.TOP)

        for item in ["Circle", "Square"]:
            shapelb.insert(tk.END, item)

        shapelb.selection_set(0)
        self.shape_lb = shapelb

        self.scalingScale = tk.Scale(self.rightcntlframe, from_=.001, to=.02, orient=tk.HORIZONTAL, resolution=-1, sliderlength=15, label="Scale Constant")
        self.scalingScale.pack(side=tk.TOP)

        self.rotationScale = tk.Scale(self.rightcntlframe, from_=.1, to=1, orient=tk.HORIZONTAL, resolution=-1, sliderlength=15, label="Rotation Constant")
        self.rotationScale.pack(side=tk.TOP)
           
        return

    def setBindings(self):
        # bind mouse motions to the canvas
        self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
        self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
        self.canvas.bind( '<Shift-Button-1>', self.handleMouseButton3 )
        self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
        self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
        self.canvas.bind( '<Shift-B1-Motion>', self.handleMouseButton3Motion )
        self.canvas.bind( '<Button-3>', self.handleMouseButton3)
        self.canvas.bind( '<B3-Motion>', self.handleMouseButton3Motion)
        self.canvas.bind( '<Button-2>', self.handleMouseButton2)
        self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion)
        self.canvas.bind( '<Motion>', self.handleMouseMotion )



        # bind command sequences to the root window
        self.root.bind( '<Control-q>', self.handleQuit )
        self.root.bind( '<Control-n>', self.handleClear)
        self.root.bind( '<Control-o>', self.handlePlotData)
        self.root.bind( '<Control-m>', self.handleMarking )
        self.root.bind( '<Control-d>', self.handleDistLines )
        self.root.bind( '<Control-s>', self.handleShowSize )


    def handlePlotData(self, event=None):
       self.handleOpen()
       cols = self.handleChooseAxes()
       self.buildPoints(cols)

    def handleChooseAxes(self):
        columns = self.data.getNumericHeaders()
        usedCols = []
        for idx in self.HeaderIndexes:
            usedCols.append(columns[idx])
        
        return usedCols

    def buildPoints(self, headerlist):
        self.canvas.delete('data_point')
        self.objects = []
        self.markedObjs = {}
        self.usedHeaders = headerlist
        
        if(len(headerlist) < 2):
            print("Not Enough Values Selected For Some Reason.")
            return
               
        if(len(headerlist) == 2):
            self.data_matrix = analysis.normalize_columns_seperately(self.data, headerlist)
            numeric_data = [[0] for item in range(self.data_matrix.shape[0])]
            self.data_matrix = np.hstack((self.data_matrix, numeric_data))
            numeric_data = [[1] for item in range(self.data_matrix.shape[0])]
            self.data_matrix = np.hstack((self.data_matrix, numeric_data))
        elif(len(headerlist) >= 3):
            self.data_matrix = analysis.normalize_columns_seperately(self.data, headerlist[0:3])
            numeric_data = [[1] for item in range(self.data_matrix.shape[0])]
            self.data_matrix = np.hstack((self.data_matrix, numeric_data))

        if(len(headerlist) > 3):
            self.color_matrix = analysis.normalize_columns_seperately(self.data, [headerlist[3]])
        else:
            self.color_matrix = np.matrix([ [1] for i in range(self.data_matrix.shape[0]) ])
       
        if(len(headerlist) > 4):
            self.size_matrix = analysis.normalize_columns_seperately(self.data, [headerlist[4]])
        else:
            self.size_matrix = np.matrix([ [1] for i in range(self.data_matrix.shape[0]) ])

        vtm = self.view.build()
        points = (vtm * self.data_matrix.T).T

        shapeID = self.shape_lb.curselection()[0]

        for i in range(self.data_matrix.shape[0]):
            x = points[i, 0] 
            y = points[i, 1]
            size = self.size_matrix[i, 0]
            color = self.color_matrix[i, 0]
            pt = None
            self.rad = 5*size
            if(shapeID == 0):
                pt = self.canvas.create_oval(x-self.rad, y-self.rad, x+self.rad, y+self.rad, fill=self.generateColor(color), outline='', tag="data_point")
            elif(shapeID == 1):
                pt = self.canvas.create_rectangle(x-self.rad, y-self.rad, x+self.rad, y+self.rad, fill=self.generateColor(color), outline='', tag="data_point")
            self.objects.append(pt)
            self.markedObjs.update( {pt : False} )

    def handleRange(self):
        ranges = []
        for header in self.usedHeaders:
            ranges.append(analysis.data_range(self.data, header))
        print(ranges)
    
    def handleStdev(self):
        pass

    def handleMean(self):
        pass

    def handleOpen(self, event=None):
        fn = fd.askopenfilename(parent=self.root, title='Choose a data file', initialdir='.')
        self.data = data.Data(fn)

        dialog = ModalDialog(self.root, minval=2, maxval=5, title="How Many Columns (2-5)")
        if(dialog.cancelled):
            return
        boxcount = dialog.getFinalVal()

        dialog = ListBoxDialog(self.root, self.data.getNumericHeaders(), boxcount)
        self.HeaderIndexes = dialog.getFinalVal()

    #Owen's handle clear method
    def handleClear(self, event=None):
        print("Clearing")
        self.canvas.delete('all')
        self.objects.clear()
        self.view.reset()
        self.lines.clear()
        self.canvas.create_text(950,20, text="Scale Factor: 1.0", font="Times 15", tag="scale_display")
        self.canvas.create_text(950,40, text="X Angle: 0.0", font="Times 15", tag="rotation_display")
        self.canvas.create_text(950,60, text="Y Angle: 0.0", font="Times 15", tag="rotation_display")
        self.buildAxes()

    def handleQuit(self, event=None):
        print( 'Terminating')
        self.root.destroy()

    def handleButton1(self):
        print( 'handling command button:', self.colorOption.get())
        for obj in self.objects:
            self.canvas.itemconfig(obj, fill=self.colorOption.get() )

    def handleMenuCmd1(self):
        print( 'handling menu command 1')

    def handleMarking(self, event=None):
        if(self.markedObjs[self.closestObj] == True):
            print("RAN1")
            self.markedObjs[self.closestObj] = False
        elif(not(self.closestObj == None)):
            print("RAN2")
            self.markedObjs[self.closestObj] = True
        
        self.updatePoints()

    def handleDistLines(self, event=None, hotkey=True):
        marked = []

        if(not(len(self.distlines) == 0) and (hotkey == True)):
            self.canvas.delete("distline")
            self.distlines.clear()
            return

        for obj in self.objects:
            if(self.markedObjs[obj] == True):
                marked.append(obj)
        
        for i in range(len(marked)):
            obj1 = marked[i]
            obj1_X, obj1_Y = self.canvas.coords(obj1)[0], self.canvas.coords(obj1)[1]
            for j in range(len(marked)-1):
                obj2 = marked[j]
                if(obj1 == obj2):
                    continue

                obj2_X, obj2_Y = self.canvas.coords(obj2)[0], self.canvas.coords(obj2)[1]
                self.distlines.append(self.canvas.create_line(obj1_X, obj1_Y, obj2_X, obj2_Y, fill='red', tag="distline"))

    def handleShowSize(self, event=None):
        print(self.showsize)
        if(self.showsize == True):
            self.showsize = False
        else:
            self.showsize = True

        self.updatePoints()

    def handleMouseMotion(self, event):
        click = (event.x, event.y)
        minDist = 10000
        self.closestObj = None
        for obj in self.objects:
            objX, objY = self.canvas.coords(obj)[0], self.canvas.coords(obj)[1]
            rad = 50
            if( ((objX > event.x-rad) and (objX < event.x+rad)) and ((objY > event.y-rad) and (objY < event.y+rad)) ):
                dist = math.sqrt((objX-event.x)**2 + (objY-event.y)**2)
                if(dist < minDist):
                    minDist = dist
                    self.closestObj = obj

    def handleMouseButton1(self, event):
        self.baseClick = (event.x, event.y)
        self.baseVRP = self.view.vrp

    def handleMouseButton2(self, event):
        self.baseClick2 = (event.x, event.y)
        self.orginalView = self.view.clone()

    def handleMouseButton3(self, event):
        self.baseClick = (event.x, event.y)
        self.baseExtent = self.view.clone().extent

    # This is called if the first mouse button is being moved
    def handleMouseButton1Motion(self, event):
        # calculate the difference
        (dx,dy) = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
        delta0 = dx * (self.view.extent[0] / self.view.screen[0])
        delta1 = dy * (self.view.extent[1] / self.view.screen[1])

        self.view.vrp = self.baseVRP + (delta0 * self.view.u) + (delta1 * self.view.vup)
        self.updateAxes()

    def handleMouseButton2Motion(self, event):
        (delta0,delta1) = ( ((event.x - self.baseClick2[0])/200)*math.pi, -((event.y - self.baseClick2[1])/200)*math.pi )
        self.view = self.orginalView.clone()
        self.rotateVRC(delta0*self.rotationScale.get(), delta1*self.rotationScale.get())
        self.updateAxes()
        self.canvas.delete("rotation_display")
        self.canvas.create_text(950,40, text="X Angle: %.2f" %delta0, font="Times 15", tag="rotation_display")
        self.canvas.create_text(950,60, text="Y Angle: %.2f" %delta1, font="Times 15", tag="rotation_display")

    def handleMouseButton3Motion(self, event):
        (dx,dy) = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
        scaleconst = self.scalingScale.get()
        scalefact = 1.0 + scaleconst*dy
        if(scalefact < 0.1): scalefact = 0.1
        if(scalefact > 3.0): scalefact = 3.0
        self.view.extent = [scalefact*val for val in self.baseExtent]
        self.canvas.delete("scale_display")
        self.canvas.create_text(950,20, text="Scale Factor: %.2f" %scalefact, font="Times 15", tag="scale_display")
        
        
        self.updateAxes()
        
    def rotateVRC(self, vupAngle, uAngle):
        u = self.view.u[0,:].tolist()[0]
        vrp = self.view.vrp[0,:].tolist()[0]
        vpn = self.view.vpn[0,:].tolist()[0]
        vup = self.view.vup[0,:].tolist()[0]
        # These may use + instead of -
        xtranval = vrp[0] - vpn[0] * self.view.extent[2]*0.5
        ytranval = vrp[1] - vpn[1] * self.view.extent[2]*0.5
        ztranval = vrp[2] - vpn[2] * self.view.extent[2]*0.5
        t1 = np.matrix([[1,0,0,-xtranval],
                        [0,1,0,-ytranval],
                        [0,0,1,-ztranval],
                        [0,0,0,1]])
       
        Rxyz = np.matrix([[u[0], u[1], u[2], 0],
                        [vup[0], vup[1], vup[2], 0],
                        [vpn[0], vpn[1], vpn[2], 0],
                        [0, 0, 0, 1]])
       
        r1 = np.matrix([[np.cos(vupAngle), 0, np.sin(vupAngle), 0],
                        [0, 1, 0, 0],
                        [-np.sin(vupAngle), 0, np.cos(vupAngle), 0], 
                        [0, 0, 0, 1]])
        
        r2 = np.matrix([[1, 0, 0, 0],
                        [0, np.cos(uAngle), -np.sin(uAngle), 0],
                        [0, np.sin(uAngle),  np.cos(uAngle), 0],
                        [0, 0, 0, 1]])
        
        xtranval = vrp[0] + vpn[0] * self.view.extent[2]*0.5
        ytranval = vrp[1] + vpn[1] * self.view.extent[2]*0.5
        ztranval = vrp[2] + vpn[2] * self.view.extent[2]*0.5        
        t2 = np.matrix([[1, 0, 0, xtranval],
                        [0, 1, 0, ytranval],
                        [0, 0, 1, ztranval],
                        [0, 0, 0, 1]])

        tvrc = np.matrix([ [vrp[0], vrp[1], vrp[2], 1],
                           [u[0], u[1], u[2], 0],
                           [vup[0], vup[1], vup[2], 0],
                           [vpn[0], vpn[1], vpn[2], 0]])
            
        tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T

        self.view.vpr = np.matrix(self.normalizeVector(tvrc[0, 0:3].tolist()[0]))
        self.view.u = np.matrix(self.normalizeVector(tvrc[1, 0:3].tolist()[0]))
        self.view.vup = np.matrix(self.normalizeVector(tvrc[2, 0:3].tolist()[0]))
        self.view.vpn = np.matrix(self.normalizeVector(tvrc[3, 0:3].tolist()[0]))

    def buildAxes(self):
        vtm = self.view.build()
        points = (vtm * self.axes.T).T
        names = ["x", "y", "z"]
        for i in range(0, points.shape[0], 2):
            p1 = (points[i, 0:2].tolist()[0])
            p2 = (points[i+1, 0:2].tolist()[0])
            self.lines.append(self.canvas.create_line(p1,p2))
            self.lines.append(self.canvas.create_text(p2[0]+10, p2[1]+10, font="Times 20", text=names[i//2]))

    def updateAxes(self):
        vtm = self.view.build()
        points = (vtm * self.axes.T).T
        for i in range(0, points.shape[0]):
            if(i%2 == 0):
                p1 = (points[i, 0:2].tolist()[0])
                p2 = (points[(i)+1, 0:2].tolist()[0])
                self.canvas.coords(self.lines[i], p1[0], p1[1], p2[0], p2[1])
            else:
                self.canvas.coords(self.lines[i], p2[0]+10, p2[1]+10)
        
        self.updatePoints()

    def updatePoints(self):
        if(len(self.objects)==0):
            return
        
        vtm = self.view.build()
        points = (vtm * self.data_matrix.T).T

        if(self.showsize == True):
            self.canvas.delete("size")
        
        for i in range(points.shape[0]):
            x = points[i, 0] 
            y = points[i, 1]
            size = self.size_matrix[i, 0]
            self.rad = 5*size
            self.canvas.coords(self.objects[i], x-self.rad, y-self.rad, x+self.rad, y+self.rad)
            if(self.markedObjs[self.objects[i]] == True):
                self.canvas.itemconfig(self.objects[i], fill='firebrick1')
                if(not(len(self.distlines) == 0)):
                    self.canvas.delete("distline")
                    self.handleDistLines(hotkey=False)
            else:
                color = self.color_matrix[i, 0]
                self.canvas.itemconfig(self.objects[i], fill=self.generateColor(color))

            if(self.showsize == True):
                objX, objY = self.canvas.coords(self.objects[i])[0], self.canvas.coords(self.objects[i])[1]
                self.canvas.create_text(objX, objY-5, text="%.3f" %size, font="Times 11", tag="size")
            else:
                self.canvas.delete("size")
            
    def normalizeVector(self, vector):
        magnitude = 0.0
        for val in vector:
            magnitude += val**2
        magnitude = math.sqrt(magnitude)
        returnVec = [val / magnitude for val in vector]
        return returnVec

    def generateColor(self, value):
        if(value < .2):
            return "deep sky blue"
        elif(value < .4):
            return "gold"
        elif(value < .6):
            return "SlateBlue2"
        elif(value < .8):
            return "saddle brown"
        elif(value < 1.1):
            return "gray8"       


    def main(self):
        print( 'Entering main loop')
        self.root.mainloop()

class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()


        self.wait_window(self)
    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

class ModalDialog(Dialog):
    pastVal = 0
    def __init__(self, parent, title = None, minval = 0, maxval = 100):
        self.minval = minval
        self.maxval = maxval  
        self.cancelled = True
        Dialog.__init__(self, parent)

    def body(self, master):
        str_val = tk.StringVar()
        entry = tk.Entry(self, textvariable=str_val)
        entry.pack(padx=5)
        str_val.set(ModalDialog.pastVal)

        entry.select_range(0,tk.END)
        return entry

    def validate(self):
        if(int(self.initial_focus.get()) < self.minval or int(self.initial_focus.get()) > self.maxval):
            print(f"Value out of range! Enter number between {self.minval} and {self.maxval}")
        else:
            return 1
    
    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()
    
    def userCancelled(self):
        return self.cancelled

    def apply(self):
        self.final_val = int(self.initial_focus.get())
        self.cancelled = False
        print(f"Value {self.final_val} taken from dialog box")
        ModalDialog.pastVal = self.final_val

    def getFinalVal(self):
        return self.final_val
    
class ListBoxDialog(Dialog):
    def __init__(self, parent, entries, boxcount=1, title = None):
        self.entries = entries
        self.boxcount = boxcount
        self.boxes = []
        self.labels = []
        self.cancelled = True
        Dialog.__init__(self, parent)

    def body(self, master):
        for i in range(self.boxcount):
            if(i==0):
                label = tk.Label(self, text="X")
            elif(i==1):
                label = tk.Label(self, text="Y")
            elif(i==2):
                label = tk.Label(self, text="Z")
            elif(i==3):
                label = tk.Label(self, text="Color")
            elif(i==4):
                label = tk.Label(self, text="Size")     
            label.pack(side=tk.LEFT)
            self.labels.append(label)
            
            headerlb = tk.Listbox(self, exportselection=0, selectmode=tk.BROWSE, height=6)
            headerlb.pack(side=tk.LEFT)

            for item in self.entries:
                headerlb.insert(tk.END, item)
                
            headerlb.selection_set(0)
            self.boxes.append(headerlb)
        return headerlb

    def validate(self):
            return 1
    
    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()
    
    def userCancelled(self):
        return self.cancelled

    def apply(self):
        self.final_val = []
        self.final_val = [box.curselection()[0] for box in self.boxes]
        self.cancelled = False
        print(f"Value {self.final_val} taken from dialog box")

    def getFinalVal(self):
        return self.final_val

        

if __name__ == "__main__":
    dapp = DisplayApp(1200, 675)
    dapp.main()



