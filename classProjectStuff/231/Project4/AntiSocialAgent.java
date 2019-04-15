
/*
 * AntiSocialAgent.java Agent that doesnt like being around other agents
 * Owen Goldthwaite
 * 3/11/2018
 */

import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Random;

public class AntiSocialAgent extends Agent
{

	public AntiSocialAgent(double x0, double y0) 
	{
		super(x0, y0);
	}
	
	public void draw(Graphics g) //Overrides inherited draw
	{
		g.setColor(new Color(0,255,0));
		g.fillOval((int)this.xPos, (int)this.yPos, 5, 5);
	}
	
	public void updateState(Landscape scape) //updates the location of this based on neighbor conditions, this one doesnt like groups.
	{
		ArrayList<Agent> neighbors = scape.getNeighbors(this.xPos, this.yPos, 15);
		Random rand = new Random();
		if(neighbors.size() < 4) //Using 4 because this agent does not count for the 3 needed
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
	
	public void updateState(Landscape scape, double radius) //Overriding for more user control
	{
		ArrayList<Agent> neighbors = scape.getNeighbors(this.xPos, this.yPos, radius);
		Random rand = new Random();
		if(neighbors.size() < 4) //Using 4 because this agent does not count for the 3 needed
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

}
