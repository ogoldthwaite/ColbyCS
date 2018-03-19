package project5;

import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class Customer extends Agent
{
	private int items;
	private boolean inLine;
	private int time; //amount of time this agent took to perform operations, returned and added to total at end of sim.
	public static int method; // which line selection method is used
	
	public Customer(double x0, double y0)
	{
		super(x0,y0);
		this.items = 1;
		this.inLine = false;
		this.time = 0;
		
	}
	
	public Customer(double x0, double y0, int items)
	{
		super(x0,y0);
		this.items = items;
		this.inLine = false;
		this.time = 0;
	}
		
	//Some setter/getter type things
	public void addItem() //Adds 1 to item count
	{
		this.items++;
	}
	
	public void takeItem() //removes 1 item from item count
	{
		this.items--;
	}
	
	public int getTime()
	{
		return this.time;
	}
	
	public void setTime(int t)
	{
		this.time = t;
	}
	
	public void addTime() //adds one time tick to the customer
	{
		this.time++;
	}
	
	public void enterLine() //Sets inLine boolean to true (called from Cashier addCustomer method)
	{
		this.inLine = true;
	}
	
	public void setItems(int val)
	{
		this.items = val;
	}
	
	public int getItems()
	{
		return this.items;
	}
	
	public void updateState(Landscape scape)
	{
		ArrayList<Cashier> counters = scape.getCashiers(); //Array list of Cashiers/Counters
		
		if(!(inLine))
			this.selectLine(counters);
	}
	
	private void selectLine(ArrayList<Cashier> counters) //Currently line selection method is random!
	{
		Random rand = new Random();
		int met;
		if(method == -1)
			met = rand.nextInt(3);
		else
			met = method;
		
		
		if(met == 0) //totally random line selection
		{
			counters.get(rand.nextInt(counters.size())).addCustomer(this);
			this.time += 1;
		}
		else if(met == 1) //Two random lines, pick shortest of two
		{
			Cashier c1 = counters.get(rand.nextInt(counters.size()));
			Cashier c2 = counters.get(rand.nextInt(counters.size()));
			
			if(c1.queueLength() < c2.queueLength())
				c1.addCustomer(this);
			else
				c2.addCustomer(this);
			
			this.time += 2;
		}
		else if(met == 2) //Pick shortest of all lines. EXTENSION - Time increase is proportional to number of possible lines
		{
			Cashier shortest = counters.get(0);
			
			for(Cashier c : counters)
				if(c.queueLength() < shortest.queueLength())
					shortest = c;
		
			shortest.addCustomer(this);
			time += counters.size();
		}
		
	}
	
	public void draw(Graphics g)
	{
		//should draw a circle in a 5x5 box at agents pos. Pos must be casted to int?
		g.setColor(Color.cyan);
		g.fillOval((int)this.xPos, (int)this.yPos, 5, 5);
	}

}