

import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Random;

/*
 * CategorizedSocialAgent.java
 * Owen Goldthwaite
 * 3/11/2018
 */

public class CategorizedSocialAgent extends SocialAgent implements Comparable<Agent>
{
	protected int category;
	
	public CategorizedSocialAgent(double x0, double y0, int cat)
	{
		super(x0,y0);
		this.category = cat;
	}
	
	public int getCategory()
	{
		return this.category;
	}
	
	public void draw(Graphics g)
	{
		if(this.category == 0)
			g.setColor(Color.MAGENTA);
		else if(this.category == 1)
			g.setColor(Color.ORANGE);
		
			
		g.fillOval((int)this.xPos, (int)this.yPos, 5, 5);
	}
	
	public void updateState(Landscape scape) //update scape for CategorizedSocialAgent
	{		
		ArrayList<Agent> neighbors = scape.getNeighbors(this.xPos, this.yPos, 20);
		Random rand = new Random();
		int same = 0;
		
		for(Agent a : neighbors)
			if(this.compareTo(a) == 0)
				same++;
		
		if(same > 4) //If there is at least 3 other of the same category
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
	
	public void updateState(Landscape scape, double radius) //overriding for better radius control
	{		
		ArrayList<Agent> neighbors = scape.getNeighbors(this.xPos, this.yPos, radius);
		Random rand = new Random();
		int same = 0;
		
		for(Agent a : neighbors)
			if(this.compareTo(a) == 0)
				same++;
		
		if(same > 4) //If there is at least 3 other of the same category
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
	
	public String toString()
	{
		return "" + this.category;
	}

	@Override
	public int compareTo(Agent o) 
	{
		if(o.getCategory() == this.getCategory())
			return 0;
		else
			return this.getCategory() > o.getCategory() ? 1 : -1;
	}
}
