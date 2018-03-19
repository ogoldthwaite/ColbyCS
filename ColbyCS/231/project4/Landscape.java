package project4;

import java.awt.Graphics;
import java.util.ArrayList;

/*
 * Landscape.java
 * Owen Goldthwaite
 * 3/11/2018
 */
public class Landscape 
{
	private int width;
	private int height;
	private LinkedList<Agent> list;
	
	public Landscape() //Default constructor Just cuz ;)
	{
		this.width = 500;
		this.height = 500;
		list = new LinkedList<Agent>();
	}
	
	public Landscape(int w, int h)
	{
		this.width = w;
		this.height = h;
		list = new LinkedList<Agent>();
	}
	
	//get set fun magic woo woo
	public int getWidth()
	{
		return this.width;
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
	}
	
	private boolean checkNeighbors(Agent a, double x0, double y0, double radius) //helper method for getNeighbors that just checks if a given agent is wihtin bounds
	{
		double xVal = a.getX();
		double yVal = a.getY();
		if( (xVal <= (x0 + radius)) && (xVal >= (x0 - radius)) )
			if( (yVal <= (y0 + radius)) && (yVal >= (y0 - radius)) )
				return true;
		
		return false;		
	}
	
	public ArrayList<Agent> getNeighbors(double x0, double y0, double radius) //returns arraylist of agents within radius at pos 
	{
		ArrayList<Agent> toReturn = new ArrayList<Agent>();
		
		for(Agent a : this.list)
		{
			if(this.checkNeighbors(a, x0, y0, radius))
				toReturn.add(a);
		}
		
		return toReturn;
	}
	
	public void updateAgents() //calls update method of each agent in random order
	{
		ArrayList<Agent> aList = list.toShuffledList();
		
		for(Agent a : aList)
			a.updateState(this);
	}
	
	public void updateAgents(double radius) //Overriding to allow more direct control over radius
	{
		ArrayList<Agent> aList = list.toShuffledList();
		
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
		
		Agent a = new SocialAgent(5,5);
		Agent b = new SocialAgent(10,10);
		Agent c = new SocialAgent(15,15);
		Agent d = new SocialAgent(20,20);
		scape.addAgent(a);
		scape.addAgent(b);
		scape.addAgent(c);
		scape.addAgent(d);
		a.updateState(scape);
		System.out.println(scape.getNeighbors(a.getX(), a.getX(), 20));
	}

}
