package project4;

import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Random;

/*
 * SocialAgent.java
 * Owen Goldthwaite
 * 3/11/2018
 */
public class SocialAgent extends Agent
{

	public SocialAgent(double x0, double y0) 
	{
		super(x0, y0);
	}

	public void draw(Graphics g) //Overrides inherited draw
	{
		//should draw a circle in a 5x5 box at agents pos. Pos must be casted to int?
		g.setColor(Color.cyan);
		g.fillOval((int)this.xPos, (int)this.yPos, 5, 5);
	}
	
	public void updateState(Landscape scape) //updates the location of this based on neighbor conditions
	{
		ArrayList<Agent> neighbors = scape.getNeighbors(this.xPos, this.yPos, 15);
		Random rand = new Random();
		if(neighbors.size() > 4) //Using 4 because this agent does not count for the 3 needed
		{
			if(rand.nextInt(100) == 1)
			{
				if(rand.nextFloat() < .5)
					this.xPos += rand.nextDouble() * -5;
				else
					this.xPos += rand.nextDouble() * 5;
				
				if(rand.nextFloat() < .5)
					this.yPos += rand.nextDouble() * -5;
				else
					this.yPos += rand.nextDouble() * 5;
			}
		}
		else
		{
			if(rand.nextFloat() < .5)
				this.xPos += rand.nextDouble() * -5;
			else
				this.xPos += rand.nextDouble() * 5;
			
			if(rand.nextFloat() < .5)
				this.yPos += rand.nextDouble() * -5;
			else
				this.yPos += rand.nextDouble() * 5;
		}
				
	}
	
	public void updateState(Landscape scape, double radius) //Overriding to allow more direct control over radius
	{
		ArrayList<Agent> neighbors = scape.getNeighbors(this.xPos, this.yPos, radius);
		Random rand = new Random();
		if(neighbors.size() > 8) //Using 4 because this agent does not count for the 3 needed
		{
			if(rand.nextInt(100) == 1)
			{
				if(rand.nextFloat() < .5)
					this.xPos += rand.nextDouble() * -5;
				else
					this.xPos += rand.nextDouble() * 5;
				
				if(rand.nextFloat() < .5)
					this.yPos += rand.nextDouble() * -5;
				else
					this.yPos += rand.nextDouble() * 5;
			}
		}
		else
		{
			if(rand.nextFloat() < .5)
				this.xPos += rand.nextDouble() * -5;
			else
				this.xPos += rand.nextDouble() * 5;
			
			if(rand.nextFloat() < .5)
				this.yPos += rand.nextDouble() * -5;
			else
				this.yPos += rand.nextDouble() * 5;
		}
				
	}
	
	public static void main(String[] args) 
	{
		Agent jeff = new Agent(0,0);
		System.out.println(jeff);
		jeff.setX(4.51);
		jeff.setY(5.56);
		System.out.println(jeff);
		System.out.println(jeff.getX() + jeff.getY());
	}


}
