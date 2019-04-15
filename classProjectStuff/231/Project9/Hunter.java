

import java.awt.Color;
import java.awt.Graphics;

/*
 * Hunter.java
 * Owen Goldthwaite
 * 5/6/2018
 */

public class Hunter extends Agent
{
	private Vertex curVert;
	private boolean armed;
	
	public Hunter()
	{
		super();
		curVert = new Vertex();
	}
	
	public Hunter(double xPos, double yPos)
	{
		super(xPos, yPos);
		curVert = new Vertex(xPos, yPos);
		armed = false;
	}

	public void updateCurrentVertex(Vertex v) //Changes curVert to v
	{		
		curVert = v;
		curVert.setVisible(true); //making it visible?
		this.xPos = curVert.getX(); //updating the position of this, may change
		this.yPos = curVert.getY();
		armed = false;
	}
	
	public Vertex getVert()
	{
		return curVert;
	}
	
	public void setArmed(boolean newVal)
	{
		armed = newVal;
	}
	
	public boolean isArmed()
	{
		return armed;
	}

	public void draw(Graphics g)
	{
		if(armed)
			g.setColor(Color.PINK);
		else
			g.setColor(Color.cyan);
		
		g.fillOval((int)this.curVert.getX()+40, (int)this.curVert.getY()+40, 20, 20);
	}
	


}
