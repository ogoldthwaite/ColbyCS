
/*
 * BullyAgent.java Agent that will group together, but move away when an outside enters the group
 * Owen Goldthwaite
 * 3/11/2018
 */

import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Random;

public class BullyAgent extends CategorizedSocialAgent
{

	public BullyAgent(double x0, double y0, int cat) 
	{
		super(x0, y0, cat);
	}
	
	public void draw(Graphics g) //Overrides inherited draw
	{
		g.setColor(new Color(153,0,0));
		g.fillOval((int)this.xPos, (int)this.yPos, 5, 5);
	}
	
	public void updateState(Landscape scape) //update scape for Bully Agent that moves when an outsider comes in
	{		
		ArrayList<Agent> neighbors = scape.getNeighbors(this.xPos, this.yPos, 20);
		Random rand = new Random();
		int same = 0;
		int outsider = 0;
		
		for(Agent a : neighbors)
		{
			if(this.compareTo(a) == 0)
				same++;
			else if (this.compareTo(a) != 0)
				outsider++;
		}
		
		if(same > 4 && outsider == 0) //If there is at least 3 other of the same category and no outsiders
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
	
	public void updateState(Landscape scape, double radius) //overriding more more user control
	{		
		ArrayList<Agent> neighbors = scape.getNeighbors(this.xPos, this.yPos, radius);
		Random rand = new Random();
		int same = 0;
		int outsider = 0;
		
		for(Agent a : neighbors)
		{
			if(this.compareTo(a) == 0)
				same++;
			else if (this.compareTo(a) != 0)
				outsider++;
		}
		
		if(same > 4 && outsider == 0) //If there is at least 3 other of the same category and no outsiders
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


