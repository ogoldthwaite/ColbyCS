This folder contains the culmination of one of my CS classes from Spring 2018. It's a gui for data analysis and visualization. 
The GUI itself is pretty ugly and not very user friendly but it does what it's supposed to do if you know how to use it.
Code wise it's really not that readable just coming into it, and there's a lot of different files, some being pretty large.
It needs a .csv with labelled columns of data. Header as row 1, data type as row 2, "numeric" being the important one. I added functionality
for this typing not be necessary for some aspects of it, but overall it's safer to have them.

Anyway, I'll go through how to run K-Means with the iris_all.csv thats in the folder just so you can see some pieces of the GUI.

1. first run display.py with some version of: python display.py
2. Open the iris_all.csv with the "Plot Data" button or ctrl-O. Select the correct .csv. A dialog box will pop up asking for number of 
columns to plot on, I would recommend doing 3 or more for this, 4 would probably be best and 5 is the max. Hit okay and another box will
pop up asking what each column represents on the axes, doesn't really matter what you do here as long as each is different. Just changes
the visuals. I would do 4 columns and select all but class for this. Hit okay and this should plot the data on the axes.
You can move the data around with left click drag to move, middle mouse button + mouse movement to rotate and right click drag to
zoom in and out. Hovering over a data point will display information on it in the top left corner of the GUI.
3. Next hit the command drop down menu in the top left and select generate k-means, a dialog box will pop up asking what features to use
for clustering, I would do all but class. Hit okay and then just pick if you want to whiten or not. Next for number of clusters put in 3.
And for a name just put whatever you want.
4. After that the K-means should be done and the 3 different clusters will be displayed with different colors to denote their group.
You can hit ctrl-c to see where the cluster centers are located. And thats it for that really!

There is a lot more you can do with this but as I said it's not to user friendly so it's not the easiest to figure out, but it's one of my
favorite projects so I thought I would send it in! Feel free to play around with it more and expose all my bugs :). 

Also don't hit ctrl-x if you have epilepsy, but otherwise feel free too! ctrl-x again toggles the fun to turn it off.