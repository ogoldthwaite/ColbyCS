package project2;
/*
Originally written by Bruce A. Maxwell a long time ago.
Updated by Brian Eastwood and Stephanie Taylor more recently

Creates a window using the JFrame class.

Creates a drawable area in the window using the JPanel class.

The JPanel calls the Landscape's draw method to fill in content, so the
Landscape class needs a draw method.
*/

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Random;

import javax.imageio.ImageIO;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

/**
* Displays a Landscape graphically using Swing.  The Landscape
* can be displayed at any scale factor.
* @author bseastwo
*/
public class LandscapeDisplay extends JFrame
{
protected Landscape scape;
private LandscapePanel canvas;
private int gridScale; // width (and height) of each square in the grid

/**
 * Initializes a display window for a Landscape.
 * @param scape the Landscape to display
 * @param scale controls the relative size of the display
 */
public LandscapeDisplay(Landscape scape, int scale)
{
    // setup the window
    super("Game of Life");
    this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    this.scape = scape;
    this.gridScale = scale;

    // create a panel in which to display the Landscape
    this.canvas = new LandscapePanel( (int) this.scape.getCols() * this.gridScale,
                                    (int) this.scape.getRows() * this.gridScale);

    // add the panel to the window, layout, and display
    this.add(this.canvas, BorderLayout.CENTER);
    this.pack();
    this.setVisible(true);
}

/**
 * Saves an image of the display contents to a file.  The supplied
 * filename should have an extension supported by javax.imageio, e.g.
 * "png" or "jpg".
 *
 * @param filename  the name of the file to save
 */
public void saveImage(String filename)
{
    // get the file extension from the filename
    String ext = filename.substring(filename.lastIndexOf('.') + 1, filename.length());

    // create an image buffer to save this component
    Component tosave = this.getRootPane();
    BufferedImage image = new BufferedImage(tosave.getWidth(), tosave.getHeight(), 
                                            BufferedImage.TYPE_INT_RGB);

    // paint the component to the image buffer
    Graphics g = image.createGraphics();
    tosave.paint(g);
    g.dispose();

    // save the image
    try
            {
                    ImageIO.write(image, ext, new File(filename));
            }
    catch (IOException ioe)
            {
                    System.out.println(ioe.getMessage());
            }
}

/**
 * This inner class provides the panel on which Landscape elements
 * are drawn.
 */
private class LandscapePanel extends JPanel
{
    /**
     * Creates the panel.
     * @param width     the width of the panel in pixels
     * @param height        the height of the panel in pixels
     */
    public LandscapePanel(int width, int height)
    {
            super();
            this.setPreferredSize(new Dimension(width, height));
            this.setBackground(Color.white);
    }

    /**
     * Method overridden from JComponent that is responsible for
     * drawing components on the screen.  The supplied Graphics
     * object is used to draw.
     * 
     * @param g     the Graphics object used for drawing
     */
    public void paintComponent(Graphics g)
    {
        super.paintComponent(g);
        scape.draw( g, gridScale );    
    } // end paintComponent
    
} // end LandscapePanel

public void update() {
    Graphics g = canvas.getGraphics();
    this.requestFocus();
    canvas.paintComponent( g );
}


public static void main(String[] args) throws InterruptedException {
    Landscape scape = new Landscape(100,100);
    Random gen = new Random();
    double density = 0.3;  
    for (int i = 0; i < scape.getRows(); i++) {
        for (int j = 0; j < scape.getCols(); j++ ) { 
            scape.getCell( i, j ).setAlive( gen.nextDouble() <= density ); //makes some cells alive
        }
    }

    LandscapeDisplay display = new LandscapeDisplay(scape, 4);

    display.repaint();
    }
}