package project9;

import java.awt.Color;
import java.awt.Graphics;

/*
 * Wumpus.java
 * Owen Goldthwaite
 * 5/6/2018
 */

public class Wumpus extends Agent
{
	private Vertex homeVert;
	private int state; //value representing state of wumpus. -1 for dead, 0 for alive and hiding, 1 for victorious
	
	public Wumpus()
	{
		super();
		homeVert = new Vertex();
		state = 0;
	}
	
	public Wumpus(double xPos, double yPos)
	{
		super(xPos, yPos);
		homeVert = new Vertex(xPos, yPos);
		state = 0;
	}
	
	public void updateCurrentVertex(Vertex v) //Changes curVert to v
	{		
		homeVert = v;
		//homeVert.setVisible(true); //making it visible?
		this.xPos = homeVert.getX(); //updating the position of this, may change
		this.yPos = homeVert.getY();
	}
	
	public void setState(int state)
	{
		this.state = state;
	}
	
	public Vertex getVert()
	{
		return this.homeVert;
	}
	
	public void draw(Graphics g)
	{
		if(state == 1) //wumpus victory
		{
			g.setColor(Color.DARK_GRAY);
			g.fillOval((int)this.homeVert.getX()+40, (int)this.homeVert.getY()+20, 20, 20);
		}
		
		if(state == -1) //loss
		{
			g.setColor(Color.RED);
			g.fillOval((int)this.homeVert.getX()+40, (int)this.homeVert.getY()+20, 20, 20);
		}
		
	}

	
	
	
}
