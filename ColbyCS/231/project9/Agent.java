package project9;

import java.awt.Graphics;

/*
 * Agent.java
 * Owen Goldthwaite
 * 3/11/2018
 */
public class Agent 
{
	protected double xPos;
	protected double yPos;
	
	public Agent(double x0, double y0)
	{
		this.xPos = x0;
		this.yPos = y0;
	}
	
	public Agent()
	{
		this.xPos = 0;
		this.yPos = 0;
	}
	
	//Mutators/Accesors and all that fun
	public double getX()
	{
		return this.xPos;
	}
	
	public double getY()
	{
		return this.yPos;
	}
	
	public void setX(double x)
	{
		this.xPos = x;
	}
	
	public void setY(double y)
	{
		this.yPos = y;
	}
	
	public void updateState(Landscape scape)
	{
		//Nothing for now
	}
	
	public void updateState(Landscape scape, double radius)
	{
		//Nothing for now
	}
	
	public void draw(Graphics g)
	{
		//Nothing for now
	}
	
	public String toString()
	{
		return "(" + this.xPos +", " + this.yPos + ")";
	}
	
	public static void main(String[] args) 
	{
		Agent jeff = new Agent(0,0);
		System.out.println(jeff);
		jeff.setX(4.51);
		jeff.setY(5.56);
		System.out.println(jeff);
		System.out.println(jeff.getX() + jeff.getY());
	}

	public int getCategory() 
	{
		return 0;
	}
}