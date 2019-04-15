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

import tkinter as tk
import math
import random

# create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a tk object, which is the root window
        self.root = tk.Tk()

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

        self.lastdialogval = 50 #value entered into the most recent dialog box

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

        # menu text for the elements
        # the first sublist is the set of items for the file menu
        # the second sublist is the set of items for the option menu
        menutext = [ [ '-', '-', 'Quit  Ctrl-Q', 'Clear  Ctrl-N' ],
                     [ 'Command 1', '-', '-' ] ]

        # menu callback functions (note that some are left blank,
        # so that you can add functions there if you want).
        # the first sublist is the set of callback functions for the file menu
        # the second sublist is the set of callback functions for the option menu
        menucmd = [ [None, None, self.handleQuit, self.handleClear],
                    [self.handleMenuCmd1, None, None] ]
        
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
        rightcntlframe = tk.Frame(self.root)
        rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # make a separator frame
        sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
        sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

        # use a label to set the size of the right panel
        label = tk.Label( rightcntlframe, text="Control Panel", width=20 )
        label.pack( side=tk.TOP, pady=10 )

        # make a menubutton
        self.colorOption = tk.StringVar( self.root )
        self.colorOption.set("black")
        colorMenu = tk.OptionMenu( rightcntlframe, self.colorOption, 
                                        "black", "blue", "red", "green" ) # can add a command to the menu
        colorMenu.pack(side=tk.TOP)

        # make a button in the frame
        # and tell it to call the handleButton method when it is pressed.
        button = tk.Button( rightcntlframe, text="Update Color", 
                               command=self.handleButton1 )
        button.pack(side=tk.TOP)  # default side is top
        
        #Owen's cool data point button! SICK!
        button = tk.Button(rightcntlframe, text = "Data Points", 	
							 command=self.createRandomDataPoints)
        button.pack(side=tk.TOP)

        # Making a list box
        genstylelb = tk.Listbox(rightcntlframe, exportselection=0, selectmode=tk.BROWSE)
        genstylelb.pack(side=tk.TOP, pady=5)

        for item in ["Random", "Gaussian"]:
            genstylelb.insert(tk.END, item)

        genstylelb.selection_set(0)

        shapelb = tk.Listbox(rightcntlframe, exportselection=0, selectmode=tk.BROWSE)
        shapelb.pack(side=tk.TOP)

        for item in ["Circle", "Square"]:
            shapelb.insert(tk.END, item)

        shapelb.selection_set(0)

        self.genstyle_lb = genstylelb
        self.shape_lb = shapelb
        
        
        return

    def createRandomDataPoints(self, event=None):
        dia = ModalDialog(self.root, minval=0, maxval=1000)

        if(dia.cancelled == True):
            return
        
        pt_num = dia.getFinalVal()

        #Picking data point generation style
        genstyle = self.genstyle_lb.curselection()
        
        if(genstyle == ()):
            print("Please select distribution type")
            return
        genstyle = genstyle[0]

        #picking data point shape
        shape = self.shape_lb.curselection()
        
        if(shape == ()):
            print("Please select a shape")
            return
        shape = shape[0]

        #random generation
        if(genstyle == 0):
            for i in range(pt_num):
                x = random.randint(1,self.canvas.winfo_width())
                y = random.randint(1,self.canvas.winfo_height())
                radius = 3 #random.randint(1,5)
                if(shape == 0):
                    pt = self.canvas.create_oval( x-radius, y-radius, x+radius, y+radius,
                                fill=self.colorOption.get(), outline='') 
                elif(shape == 1):      
                    pt = self.canvas.create_rectangle( x-radius, y-radius, x+radius, y+radius,
                                fill=self.colorOption.get(), outline='')     
                self.objects.append(pt)
        #gaussian
        else:
            for i in range(pt_num):
                x = random.gauss(self.canvas.winfo_width()//2,self.canvas.winfo_width()//8)
                y = random.gauss(self.canvas.winfo_height()//2,self.canvas.winfo_height()//8)
                radius = 3 #random.randint(1,5)
                if(shape == 0):
                    pt = self.canvas.create_oval( x-radius, y-radius, x+radius, y+radius,
                                fill=self.colorOption.get(), outline='') 
                elif(shape == 1):      
                    pt = self.canvas.create_rectangle( x-radius, y-radius, x+radius, y+radius,
                                fill=self.colorOption.get(), outline='')                
                self.objects.append(pt)

    def setBindings(self):
        # bind mouse motions to the canvas
        self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
        self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
        self.canvas.bind( '<Shift-Button-1>', self.handleMouseButton3 )
        self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
        self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
        self.canvas.bind( '<Shift-B1-Motion>', self.handleMouseButton3Motion )

        # bind command sequences to the root window
        self.root.bind( '<Control-q>', self.handleQuit )
        self.root.bind( '<Control-n>', self.handleClear)

    #Owen's handle clear method
    def handleClear(self, event=None):
        print("Clearing")
        self.canvas.delete('all')
        self.objects.clear()

    def handleQuit(self, event=None):
        print( 'Terminating')
        self.root.destroy()

    def handleButton1(self):
        print( 'handling command button:', self.colorOption.get())
        for obj in self.objects:
            self.canvas.itemconfig(obj, fill=self.colorOption.get() )

    def handleMenuCmd1(self):
        print( 'handling menu command 1')

    def handleMouseButton1(self, event):
        print( 'handle mouse button 1: %d %d' % (event.x, event.y))
        self.baseClick = (event.x, event.y)

    def handleMouseButton2(self, event):
        self.baseClick = (event.x, event.y)
        print( 'handle mouse button 2: %d %d' % (event.x, event.y))
        shape = self.shape_lb.curselection()
        
        if(shape == ()):
            print("Please select a shape")
            return
        shape = shape[0]

        dx = 3
        rgb = "#%02x%02x%02x" % (random.randint(0, 100), 
                             random.randint(0, 100), 
                             random.randint(0, 100) )
        if(shape == 0):
            oval = self.canvas.create_oval( event.x - dx,
                                            event.y - dx, 
                                            event.x + dx, 
                                            event.y + dx,
                                            fill = rgb,
                                            outline='')
        elif(shape == 1):
            oval = self.canvas.create_rectangle( event.x - dx,
                                            event.y - dx, 
                                            event.x + dx, 
                                            event.y + dx,
                                            fill = rgb,
                                            outline='')
        self.objects.append( oval )

    def handleMouseButton3(self, event):
        self.baseClick = (event.x, event.y)
        print( 'handle mouse button 3: %d %d' % (event.x, event.y))

    # This is called if the first mouse button is being moved
    def handleMouseButton1Motion(self, event):
        # calculate the difference
        diff = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
        print("VALUE: ", ModalDialog.pastVal)
        # update base click
        self.baseClick = ( event.x, event.y )
        print( 'handle button1 motion %d %d' % (diff[0], diff[1]))

        for point in self.objects:
            loc = self.canvas.coords(point)
            self.canvas.coords(point, loc[0] + diff[0], loc[1] + diff[1], loc[2] + diff[0], loc[3] + diff[1] )

            
    # This is called if the second button of a real mouse has been pressed
    # and the mouse is moving. Or if the control key is held down while
    # a person moves their finger on the track pad.
    def handleMouseButton2Motion(self, event):
        print( 'handle button 2 motion %d %d' % (event.x, event.y) )
        
        diff = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
        if(diff[1] > 0): #moving mouse down
            change = -.35
        else:
            change = .35

        for point in self.objects:
            x0, y0, x1, y1 = self.canvas.coords(point)

            if(not(x1+change < x0+5 or y1+change < y0+5)):
                self.canvas.coords(point, x0, y0, x1+change, y1+change )

    def handleMouseButton3Motion(self, event):
        print( 'handle button 3 motion %d %d' % (event.x, event.y) )
        
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
    

        

if __name__ == "__main__":
    dapp = DisplayApp(1200, 675)
    dapp.main()



