package project5;

import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Random;

public class ImpatientCustomer extends Customer
{
	private int upsetCount; //When greater than 10 upset will be true and this will move to a different line
	private Cashier lastLine;
		
	public ImpatientCustomer(double x0, double y0) 
	{
		super(x0, y0);
		lastLine = null;
		upsetCount = 0;
		
	}

	public ImpatientCustomer(double x0, double y0, int items)
	{
		super(x0,y0, items);
		lastLine = null;
		upsetCount = 0;
	}
	
	@Override
	public void addTime()
	{
		this.time++;
		this.upsetCount++;
	}
	
	public void updateState(Landscape scape) //updates state!
	{
		ArrayList<Cashier> counters = scape.getCashiers(); //Array list of Cashiers/Counters
		
		if(this.upsetCount > 25)
		{
			upsetCount = 0;
			inLine = false;
		}
		
		if(!(inLine))
			this.selectLine(counters);
	}
	
	private void selectLine(ArrayList<Cashier> counters) //Line selected based on value of static int method
	{
		Random rand = new Random();
		int met;
		if(method == -1)
			met = rand.nextInt(3);
		else
			met = method;
		
		
		if(met == 0) //totally random line selection
		{
			int choice = rand.nextInt(counters.size());
			
			if(counters.get(choice) == this.lastLine && counters.size() > 1) //picks a new different line
				this.selectLine(counters);		
			else
			{
				counters.get(choice).addCustomer(this);							
				this.time += 1;
				upsetCount += 1;
				this.lastLine = counters.get(choice);
			}
		}
		else if(met == 1) //Two random lines, pick shortest of two
		{
			int choice1 = rand.nextInt(counters.size());
			int choice2 = rand.nextInt(counters.size());		
			Cashier c1 = counters.get(choice1);
			Cashier c2 = counters.get(choice2);
			
			if(counters.size() > 1 && counters.get(choice1) == this.lastLine) //switches to the other line
			{
				c2.addCustomer(this);
				this.lastLine = c2;
			}
			else
			{			
				this.time += 2;
				upsetCount += 2;
				if(c1.queueLength() < c2.queueLength())
				{
					c1.addCustomer(this);
					this.lastLine = c1;
				}
				else
				{
					c2.addCustomer(this);
					this.lastLine = c2;
				}
			}
			
		}
		else if(met == 2) //Pick shortest of all lines. EXTENSION - Time increase is proportional to number of possible lines
		{
			Cashier shortest = counters.get(0);
			
			for(Cashier c : counters)
				if(c.queueLength() < shortest.queueLength())
					shortest = c;
		
			if(shortest == this.lastLine && counters.size() > 1)
				this.selectLine(counters);
			else
			{
				shortest.addCustomer(this);
				time += counters.size();
				upsetCount += counters.size();
			}
		}
	}
	
	public void draw(Graphics g) //draws stuff
	{
		g.setColor(Color.DARK_GRAY);
		g.fillOval((int)this.xPos, (int)this.yPos, 5, 5);
	}
	
	
}
