package project5;

import java.awt.Color;
import java.awt.Graphics;

public class SlowCashier extends Cashier
{

	public SlowCashier(double x0, double y0) 
	{
		super(x0, y0);
	}
	
	public void updateState(Landscape scape) 
	{
		if(line.size() == 0)
			return;
		
		if(CheckoutSimulation.tick % 3 == 0) //Slow Cashier only works every 3rd tick
		{
			if(line.peek().getItems() > 0)
				line.peek().takeItem();
			
			if(line.peek().getItems() == 0)
			{
				Customer cDone = line.poll();
				scape.addTime(cDone.getTime()); //adds cDone's time to total time
				cDone = null;
					
				for(Customer c : line) //Moving each customer in line by +5 y, may want to change amount moved
					c.setY(c.getY()+5);	
			}
		}
	
		for(Customer c : line) //Every tick a customer is waiting for adds 1 time to their total time.
			c.addTime();
	}
	
	public void draw(Graphics g) //Should probably draw a rectangle for the line also!!
	{
		g.setColor(new Color(242,33,210));
		g.fillRect((int)this.xPos, (int)this.yPos-15, 5, 25);
	}
	
}
