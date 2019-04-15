

import java.awt.Color;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;

/*
 * Landscape.java
 * Owen Goldthwaite
 * 3/18/2018
 */
public class Landscape 
{
	private int width;
	private int height;
	private LinkedList<Agent> list;
	private int totalTime; //Total time steps taken by all customers
	private ArrayList<Double> timeList;
	public static boolean clearingLines = false;
	
	public Landscape() //Default constructor Just cuz ;)
	{
		this.width = 500;
		this.height = 500;
		this.list = new LinkedList<Agent>();
		this.totalTime = 0;
		this.timeList = new ArrayList<Double>();
	}
	
	public Landscape(int w, int h)
	{
		this.width = w;
		this.height = h;
		this.list = new LinkedList<Agent>();
		this.totalTime = 0;
		this.timeList = new ArrayList<Double>();
	}
	
	//get set fun magic woo woo
	public int getWidth()
	{
		return this.width;
	}
	
	public void addTime(int t) //Adds time t to totalTime
	{
		this.totalTime += t;
		this.timeList.add((double) t);
	}
	
	public void addTime(Customer c) //Adds Customer c's time value to total time, not sure which of these I will use
	{
		this.totalTime += c.getTime();
	}
	
	public int getTotalTime()
	{
		return this.totalTime;
	}
	
	public ArrayList<Double> getTimeList()
	{
		ArrayList<Double> toReturn = new ArrayList<Double>();
		
		for (Double double1 : timeList) {
			toReturn.add(double1);
		}
		return toReturn;
	}
	
	public int getHeight()
	{
		return this.height;
	}
	
	public void addAgent(Agent a) //Adds agent a to front of list
	{
		list.addFirst(a);
	}
	
	public void draw(Graphics g) //Calls each agents draw method
	{
		for (Agent a : list) 
			a.draw(g);
		
		if(clearingLines)
		{
			g.setColor(Color.black);
			g.drawString("--CLEARING LINES--", width/2 - 75, height/2);
			g.drawString("--THIS COULD TAKE A SECOND--", width/2 - 115, height/2 + 25);
		}
	}	
	
	public ArrayList<Cashier> getCashiers()
	{
		ArrayList<Cashier> toReturn = new ArrayList<Cashier>();
		
		for(Agent a : this.list)
		{
			if(a.getClass().equals(Cashier.class)) //Checking if agent a is a cashier or not
				toReturn.add((Cashier) a);
			else if(a.getClass().equals(SlowCashier.class))
				toReturn.add((SlowCashier)a);
		}		
		return toReturn;
	}
	
	public void updateAgents() //calls update method of each agent in random order
	{
		Collections.shuffle(list);
		ArrayList<Agent> aList = new ArrayList<Agent>();
		aList.addAll(list);
		
		for(Agent a : aList)
			a.updateState(this);
	}
	
	public void updateAgents(double radius) //Overriding to allow more direct control over radius
	{
		Collections.shuffle(list);
		ArrayList<Agent> aList = new ArrayList<Agent>();
		aList.addAll(list);
		
		for(Agent a : aList)
			a.updateState(this, radius);	
	}
	
	public String toString()
	{
		return "There are " + list.size() +" Agents in the landscape.";
	}
	
	public static void main(String[] args) 
	{
		Landscape scape = new Landscape(500,500);

		
//		Agent a = new Agent(51,51);
//		Agent b = new Agent(53,53);
//		scape.addAgent(a);
//		scape.addAgent(b);
//		System.out.println(scape);
//		System.out.println(scape.getNeighbors(48, 50, 3));
		
	}

}