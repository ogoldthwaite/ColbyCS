package project5;
/*
 * Cashier.java
 * Owen Goldthwaite
 * 3/18/2018
 */

import java.awt.Color;
import java.awt.Graphics;

public class Cashier extends Agent //Cashier is CheckoutAgent
{	
	private MyQueue<Customer> line; //Currently using a customer type queue, NOT AGENT.

	public Cashier(double x0, double y0) 
	{
		super(x0, y0);
		line = new MyQueue<Customer>();
	}

	public int queueLength() //returns the length of the queue, each item that an agent has adds 1 to the queue length
	{
		int toReturn = line.size();
		for(Customer c : line)
			toReturn += c.getItems();
		return toReturn;
	}
	
	public void addCustomer(Customer c) //adds customer c to the line
	{
		c.enterLine();
		c.setX(this.xPos  + 5);
		c.setY(this.yPos - 5*line.size());
		line.offer(c);
	}
	
	public void draw(Graphics g) //Should probably draw a rectangle for the line also!!
	{
		g.setColor(new Color(226,70,80));
		g.fillRect((int)this.xPos, (int)this.yPos-15, 5, 25);
	}
	
	public void updateState(Landscape scape) 
	{
		if(line.size() == 0)
			return;
		
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
	
		for(Customer c : line) //Every tick a customer is waiting for adds 1 time to their total time.
			c.addTime();
	}
	
}