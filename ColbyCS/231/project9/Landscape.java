package project9;

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
	private LinkedList<Agent> foreList;
	private LinkedList<Agent> backList;
	
	public Landscape() //Default constructor Just cuz ;)
	{
		this.width = 500;
		this.height = 500;
		this.foreList = new LinkedList<Agent>();
		this.backList = new LinkedList<Agent>();
	}
	
	public Landscape(int w, int h)
	{
		this.width = w;
		this.height = h;
		this.foreList = new LinkedList<Agent>();
		this.backList = new LinkedList<Agent>();
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
	
	public void addAgent(Agent a) //Currently adds an agent to both lists, possible change later
	{
		foreList.addFirst(a);
		backList.addFirst(a);
	}
	
	public void addForeAgent(Agent a) 
	{
		foreList.addFirst(a);
	}
	
	public void addBackAgent(Agent a) 
	{
		backList.addFirst(a);
	}
	
	public void draw(Graphics g) //Calls each agents draw method
	{
		for (Agent a : foreList) 
			a.draw(g);
		
		for (Agent a : backList) 
			a.draw(g);
	}	
	
	public void clearVertices()
	{
		for (Agent agent : foreList) 
		{
			if(agent.getClass().equals(Vertex.class))
				foreList.remove(agent);
		}
	}
	
	
	public void updateAgents() //calls update method of each agent in random order
	{
		Collections.shuffle(foreList);
		Collections.shuffle(backList);
		
		ArrayList<Agent> aList = new ArrayList<Agent>();
		aList.addAll(foreList);
		aList.addAll(backList);
		
		for(Agent a : aList)
			a.updateState(this);
	}
	
	public void updateAgents(double radius) //Overriding to allow more direct control over radius
	{
		Collections.shuffle(foreList);
		Collections.shuffle(backList);
		
		ArrayList<Agent> aList = new ArrayList<Agent>();
		aList.addAll(foreList);
		aList.addAll(backList);
		
		
		for(Agent a : aList)
			a.updateState(this, radius);	
	}
	
	public String toString()
	{
		return "There are " + foreList.size() +" foreground Agents in the landscape." + "\n" + "There are " + backList.size() +" background Agents in the landscape.";
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