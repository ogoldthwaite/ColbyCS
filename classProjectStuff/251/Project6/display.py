# Owen Goldthwaite
# CS 251
# Spring 2018

import tkinter.filedialog as fd
import tkinter as tk
import tkinter.font
import numpy as np
import view
import time
import math
import random
import data
import analysis
import copy
import webbrowser
#from PIL import Image, ImageGrab

class DisplayApp:

    def __init__(self, width, height):
        self.pastPlots = []
        self.dostuff = -1
        self.pcaAnalyses = []
        self.pcaNames = []
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
        self.root.title("CHAD")

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

        self.lines = []
        self.distlines = []

        self.buildAxes()

        self.regressLines = []
        self.regressEndPts = None

        self.rotationstuffXCoord = self.canvas.winfo_width() - 100

        self.canvas.create_text(self.rotationstuffXCoord,20, text="Scale Factor: 1.0", font="Times 15", tag="scale_display")
        self.canvas.create_text(self.rotationstuffXCoord,40, text="X Angle: 0.0", font="Times 15", tag="rotation_display")
        self.canvas.create_text(self.rotationstuffXCoord,60, text="Y Angle: 0.0", font="Times 15", tag="rotation_display")

        self.delta0 = 0.0
        self.delta1 = 0.0
        self.scalefact = 1.0
        self.litTunes = True

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
                     ['Linear Regression', 'Generate PCA Analysis', 'Plot Generated PCA', 'Display PCA Info', 'Open Previous' ],
                     [ 'Range', 'Mean', 'Stdev' ] ]

        # menu callback functions (note that some are left blank,
        # so that you can add functions there if you want).
        # the first sublist is the set of callback functions for the file menu
        # the second sublist is the set of callback functions for the option menu
        menucmd = [ [None, None, self.handleQuit, self.handleClear],
                    [self.handleLinearRegression, self.handleCreatePCA, self.handlePlotPCA, self.handleDisplayPcaInfo, self.handleReOpen], 
                    [self.handleMouseMotion, self.handleMouseMotion, self.handleMouseMotion]]
        
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
        self.root.bind( '<Control-p>', self.screenShotCanvas)
        self.root.bind( '<Control-x>', self.toggleDoStuff )

    def handleCreatePCA(self, normalize=True):
        if(self.data == None):
            print("Please select data first")
            self.handlePlotData()

        colbox = ListBoxDialog(self.root, self.origData.getNumericHeaders(), browsetype = tk.EXTENDED, title="Select Feature for PCA Analysis :) Ctrl-Click for Multiple")
        self.headerIndexes = colbox.getFinalVal()

        normbox = ListBoxDialog(self.root, ["Normalize", "Dont Normalize"])
        normchoice = normbox.getFinalVal()
        if(normchoice[0] == 0):
            normalize = True
        else:
            normalize = False

        namebox = TextEntryDialog(self.root, title="Enter a name for the PCA")
        name = namebox.getFinalVal()
        if(name in self.pcaNames):
            name = "New " + name

        cols = self.handleChooseAxes()
        self.pcaData = analysis.pca(self.origData, cols, normalize)
        self.pcaAnalyses.append(self.pcaData)
        self.data = self.pcaData
        self.pcaNames.append(name)

    def handlePlotPCA(self):
        if(self.pcaAnalyses == []):
            print("No PCAs have been made yet")
            self.handleCreatePCA()

        colbox = ListBoxDialog(self.root, self.pcaNames, deletebutton=True, title="Pick PCA to plot ;)")
        result = colbox.getFinalVal()
        if(result[0] == 'del'):
            for idx in result[1]:
                del self.pcaAnalyses[idx]
                del self.pcaNames[idx]
        else:
            self.data = self.pcaAnalyses[result[0]]
            box = ListBoxDialog(self.root, self.data.getNumericHeaders(), browsetype=tk.EXTENDED, title="What Eigenvectors do you want to project to? :)")
            self.headerIndexes = box.getFinalVal()
            usedcols = self.handleChooseAxes(useOrig=False)
            self.buildPoints(usedcols)

    def handleDisplayPcaInfo(self):
        if(self.data == None):
            print("No data object yet lol wut are you doing silly!")
            self.handleCreatePCA()
        dispbox = PCADialog(self.root, self.data)

    def handleLinearRegression(self):
        if(self.data == None):
            print("Please select data first")
            self.handlePlotData()
        dialog = ListBoxDialog(self.root, self.data.getNumericHeaders(), 2, title="Select Linear Regression Columns :)")
        self.headerIndexes = dialog.getFinalVal()
        self.handleClear(addtopast=False)
        self.buildLinearRegression()

    def buildLinearRegression(self, rebuilt=False):
        if(rebuilt):
            cols = self.cols
        else:
            cols = self.handleChooseAxes()
        
        twoVarData = self.data.getColVals(cols)
        normedTwoVar = analysis.normalize_columns_seperately(self.data, cols)
        normedTwoVar = np.hstack( (normedTwoVar, np.zeros((normedTwoVar.shape[0], 1))) )
        self.data_matrix = np.hstack( (normedTwoVar, np.ones((normedTwoVar.shape[0], 1))) )

        vtm = self.view.build()
        points = (vtm * self.data_matrix.T).T
        self.buildPoints(cols)
        
        #regress tupe is (slope, yInt, rVal, pVal, stderr)
        regressTupe, xMinMax, yMinMax = analysis.single_linear_regression(self.data, cols[0], cols[1])

        xstart = 0.0
        xend = 1.0
        ystart = ((xMinMax[0] * regressTupe[0] + regressTupe[1]) - yMinMax[0])/(yMinMax[1] - yMinMax[0])
        yend = ((xMinMax[1] * regressTupe[0] + regressTupe[1]) - yMinMax[0])/(yMinMax[1] - yMinMax[0])
        
        self.regressPoints = np.matrix([[xstart, ystart, 0, 1], [xend, yend, 0, 1]]).T
        points = (vtm * self.regressPoints)
        points = points.tolist()

        regressLine = self.canvas.create_line(points[0][0], points[0][1], points[1][0], points[1][1], fill="blue", width=3, tag="regress_line")
        self.regressLines.append(regressLine)

        self.canvas.delete("regress_display")
        self.canvas.create_text(950,100, text="Slope: %.4f" %regressTupe[0], font="Times 15", tag="regress_display")
        self.canvas.create_text(950,120, text="Intercept: %.4f" %regressTupe[1], font="Times 15", tag="regress_display")
        self.canvas.create_text(950,140, text="R-Val: %.4f" %regressTupe[2], font="Times 15", tag="regress_display")
        self.updateFits()

    def handlePlotData(self, event=None):
       self.handleOpen()
       self.canvas.delete("regress_line")
       self.cols = self.handleChooseAxes()
       self.buildPoints(self.cols)

    def handleChooseAxes(self, useOrig=True):
        if(useOrig):
            columns = self.origData.getNumericHeaders()
        else:
            columns = self.data.getNumericHeaders()
        usedCols = []
        for idx in self.headerIndexes:
            usedCols.append(columns[idx])
        
        return usedCols

    def buildPoints(self, headerlist):
        self.canvas.delete('data_point')
        self.objects = []
        self.markedObjs = {}
        self.rawObjData = {}
        self.usedHeaders = headerlist
        rawData = self.data.getNumericMatrix()
        
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
            
            rawDataList = []
            for j in range(len(headerlist)):
                rawDataList.append(headerlist[j] + ": "+ str(rawData[i, j]))

            self.rawObjData.update( {pt : rawDataList} )
            self.objects.append(pt)
            self.markedObjs.update( {pt : False} )

    def handleOpen(self, event=None):
        if(not(len(self.pastPlots) == 0) or (not(len(self.objects) == 0))):
            self.pastPlots.append( [self.data, self.objects, self.view.clone(), self.lines, self.regressLines, self.cols] )

        fn = fd.askopenfilename(parent=self.root, title='Choose a data file', initialdir='.')
        self.data = data.Data(fn)
        self.origData = copy.deepcopy(self.data)

        dialog = ModalDialog(self.root, minval=2, maxval=5, title="How Many Columns (2-5)")
        if(dialog.cancelled):
            return
        boxcount = dialog.getFinalVal()

        dialog = ListBoxDialog(self.root, self.data.getNumericHeaders(), boxcount, title="Select Columns :)")
        self.headerIndexes = dialog.getFinalVal()

    def handleReOpen(self, event=None):
        if(len(self.pastPlots) == 0 ):
            print("No past plots to open")
            return

        pastNums = [i+1 for i in range(len(self.pastPlots))]
        dialog = ListBoxDialog(self.root, pastNums, 1)

        toOpenIndex = dialog.getFinalVal()[0]

        toOpenData = self.pastPlots[toOpenIndex]
        self.data = toOpenData[0]
        self.objects = toOpenData[1]
        self.view = toOpenData[2]
        self.lines = toOpenData[3]
        self.regressLines = toOpenData[4]
        self.cols = toOpenData[5]

        self.buildPoints(self.cols)
        self.updateAxes()
        print(len(self.regressLines))
        if(not(len(self.regressLines) == 0)):
            self.buildLinearRegression(rebuilt=True)

    def handleClear(self, event=None, addtopast=True):
        if(addtopast):
            self.pastPlots.append( [self.data, self.objects, self.view.clone(), self.lines, self.regressLines, self.cols] )

        
        self.canvas.delete('all')
        self.objects.clear()
        self.view.reset()
        self.lines.clear()
        self.regressLines.clear()
        self.canvas.create_text(self.rotationstuffXCoord,20, text="Scale Factor: 1.0", font="Times 15", tag="scale_display")
        self.canvas.create_text(self.rotationstuffXCoord,40, text="X Angle: 0.0", font="Times 15", tag="rotation_display")
        self.canvas.create_text(self.rotationstuffXCoord,60, text="Y Angle: 0.0", font="Times 15", tag="rotation_display")
        self.buildAxes()

    def handleQuit(self, event=None):
        print( 'Terminating')
        self.root.destroy()

    def handleMarking(self, event=None):
        if(self.markedObjs[self.closestObj] == True):
            self.markedObjs[self.closestObj] = False
        elif(not(self.closestObj == None)):
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

    # Finding nearest datapoint
    def handleMouseMotion(self, event):
        self.rotationstuffXCoord = self.canvas.winfo_width() - 100 
        self.canvas.delete("rotation_display")
        self.canvas.create_text(self.rotationstuffXCoord,40, text="X Angle: %.2f" %self.delta0, font="Times 15", tag="rotation_display")
        self.canvas.create_text(self.rotationstuffXCoord,60, text="Y Angle: %.2f" %self.delta1, font="Times 15", tag="rotation_display")
        self.canvas.delete("scale_display")
        self.canvas.create_text(self.rotationstuffXCoord,20, text="Scale Factor: %.2f" %self.scalefact, font="Times 15", tag="scale_display")


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

        if(self.dostuff == 1):
            self.strobeParty()

        self.updatePoints()

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
       
        if(self.dostuff == 1):
            self.strobeParty()

        self.updateAxes()

    def handleMouseButton2Motion(self, event):
        (delta0,delta1) = ( ((event.x - self.baseClick2[0])/200)*math.pi, -((event.y - self.baseClick2[1])/200)*math.pi )
        self.view = self.orginalView.clone()
        self.rotateVRC(delta0*self.rotationScale.get(), delta1*self.rotationScale.get())
        self.updateAxes()

        self.delta0 = delta0
        self.delta1 = delta1

        self.canvas.delete("rotation_display")
        self.canvas.create_text(self.rotationstuffXCoord,40, text="X Angle: %.2f" %self.delta0, font="Times 15", tag="rotation_display")
        self.canvas.create_text(self.rotationstuffXCoord,60, text="Y Angle: %.2f" %self.delta1, font="Times 15", tag="rotation_display")

        if(self.dostuff == 1):
            self.strobeParty()

    def handleMouseButton3Motion(self, event):
        (dx,dy) = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
        scaleconst = self.scalingScale.get()
        scalefact = 1.0 + scaleconst*dy
        if(scalefact < 0.1): scalefact = 0.1
        if(scalefact > 3.0): scalefact = 3.0
        self.view.extent = [scalefact*val for val in self.baseExtent]
        self.scalefact = scalefact
        self.canvas.delete("scale_display")
        self.canvas.create_text(self.rotationstuffXCoord,20, text="Scale Factor: %.2f" %scalefact, font="Times 15", tag="scale_display")
        
        if(self.dostuff == 1):
            self.strobeParty()
        
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
        if(not(self.regressLines == [])):
            self.updateFits()

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

            if(not(self.closestObj == None)):
                self.canvas.itemconfig(self.closestObj, fill='green')
                text = self.rawObjData[self.closestObj]
                self.canvas.delete("objData")
                self.canvas.create_text(10,15, text=text, font="Times 11", anchor=tk.W, tag="objData")
            else:
                self.canvas.delete("objData")

    def updateFits(self):
        vtm = self.view.build()
        points = vtm * self.regressPoints
        for i in range(len(self.regressLines)):
            p1 = (points[0:2, 0].tolist())
            p2 = (points[0:2, 1].tolist())
            self.canvas.coords(self.regressLines[i], p1[0], p1[1], p2[0], p2[1])
            
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

    def toggleDoStuff(self, event=None):
        self.litTunes = True
        self.dostuff = self.dostuff * -1
        if(self.dostuff == -1):
            self.strobeParty(reset=True)

    def strobeParty(self, reset=False):
        if(reset):
            self.canvas.config(background="white")
            self.root.config(background="white")     
            self.rightcntlframe.config(background="white")      
            self.canvas.delete("LITtext")   
        else:
            self.canvas.config(background=random.sample(COLORS, 1)[0])
            self.root.config(background=random.sample(COLORS, 1)[0])
            self.rightcntlframe.config(background=random.sample(COLORS, 1)[0])
            x = random.randint(0, self.canvas.winfo_width())
            y = random.randint(0, self.canvas.winfo_height())
            size = random.randint(10,50)
            self.canvas.create_text(x, y, text="LIT", font=("Times New Roman", size, "bold"), fill=random.sample(COLORS, 1)[0], tag="LITtext")           
            
            if(self.litTunes):
                webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                self.litTunes = False

    def screenShotCanvas(self, event=None):
        print("Saving Image..")
        x=self.root.winfo_rootx()
        y=self.root.winfo_rooty()
        x1=x+self.root.winfo_width()
        y1=y+self.root.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("CanvasPic.jpg")

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
        Dialog.__init__(self, parent, title)

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
    def __init__(self, parent, entries, boxcount=1, title = None, browsetype = tk.BROWSE, deletebutton = False):
        self.entries = entries
        self.boxcount = boxcount
        self.boxes = []
        self.labels = []
        self.cancelled = True
        self.browsetype = browsetype
        self.deletebutton = deletebutton
        Dialog.__init__(self, parent, title)

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
            
            headerlb = tk.Listbox(self, exportselection=0, selectmode=self.browsetype, height=6)
            headerlb.pack(side=tk.LEFT)

            for item in self.entries:
                headerlb.insert(tk.END, item)
                
            headerlb.selection_set(0)
            self.boxes.append(headerlb)
        return headerlb

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

        if(self.deletebutton):
            w = tk.Button(box, text="Delete", width=10, command=self.delete)
            w.pack(side=tk.LEFT, padx=5, pady=5)

        box.pack()

    def validate(self):
            return 1
    
    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def delete(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()
        self.final_val = ('del', self.final_val)

        self.cancel()
    
    def userCancelled(self):
        return self.cancelled

    def apply(self):
        self.final_val = []
        if( not(self.browsetype == tk.BROWSE) and (len(self.boxes) == 1) ):
            self.final_val = self.boxes[0].curselection()
        else:
            self.final_val = [box.curselection()[0] for box in self.boxes]
        self.cancelled = False
        print(f"Value {self.final_val} taken from dialog box")

    def getFinalVal(self):
        return self.final_val

class PCADialog(Dialog):
    def __init__(self, parent, pcaOBJ):
        self.pcaOBJ = pcaOBJ
        Dialog.__init__(self, parent)
    
    def body(self, master):
        tk.Label(self, text="Eiegenvectors").grid(row=0, column=0)
        tk.Label(self, text="Eigenvalues").grid(row=0, column=1)
        tk.Label(self, text="Cumulative PCA Distr. %").grid(row=0, column=2)
        count = 3
        for label in self.pcaOBJ.getOriginalHeaders():
            tk.Label(self, text=label).grid(row=0, column=count)
            count += 1
        
        count = 1
        for label in self.pcaOBJ.getNumericHeaders():
            tk.Label(self, text=label).grid(row=count, column=0)
            count+=1

        count = 1
        for val in self.pcaOBJ.getEigenvalues()[0]:
            tk.Label(self, text="%.3f" %val).grid(row=count, column=1)
            count+=1

        total = sum(self.pcaOBJ.getEigenvalues()[0])
        count = 1
        pastVal = 0
        for val in self.pcaOBJ.getEigenvalues()[0]:
            pastVal = (val/total) + pastVal
            tk.Label(self, text="%.3f" %pastVal).grid(row=count, column=2)
            count+=1

        print(self.pcaOBJ.getEigenvectors()[0])
        rowval = 1
        evecs = self.pcaOBJ.getEigenvectors()
        for row in range(evecs.shape[0]):
            colval = 3
            for col in range(evecs.shape[1]):
                val = evecs[row,col]
                tk.Label(self, text="%.3f" %val).grid(row=rowval, column=colval)
                colval += 1
            rowval += 1

class TextEntryDialog(Dialog):
    pastVal = "Name Here"
    def __init__(self, parent, title = None):
        self.cancelled = True
        Dialog.__init__(self, parent, title)

    def body(self, master):
        str_val = tk.StringVar()
        entry = tk.Entry(self, textvariable=str_val)
        entry.pack(padx=5)
        str_val.set(TextEntryDialog.pastVal)

        entry.select_range(0,tk.END)
        return entry

    def validate(self):
        if(len(self.initial_focus.get()) == 0):
            print(f"Enter an actual string silly!")
        else:
            return 1
    
    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()
    
    def userCancelled(self):
        return self.cancelled

    def apply(self):
        self.final_val = self.initial_focus.get()
        self.cancelled = False
        print(f"Value {self.final_val} taken from dialog box")
        ModalDialog.pastVal = self.final_val

    def getFinalVal(self):
        return self.final_val

COLORS  =['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

if __name__ == "__main__":
    dapp = DisplayApp(1200, 675)
    dapp.main()



