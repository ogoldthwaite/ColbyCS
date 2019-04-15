
/*
* Cell.java
* Owen Goldthwaite
* 02/19/18
*/

import java.awt.Graphics;
import java.util.ArrayList;

public class Cell
{
	private boolean alive;

	public Cell()
	{
		alive = false;
	}

	public Cell( boolean alive )
	{
		this.alive = alive;
	}

	public void kill()
	{
		this.alive = false;
	}

	public boolean getAlive()
	{
		return this.alive;
	}

	public void setAlive() //Overriding the normal one cuz this makes more sense to me.
	{
		this.alive = true;
	}

	public void setAlive( boolean alive )
	{
		this.alive = alive;
	}

	public void draw( Graphics g, int x, int y, int scale)
	{
		if(this.alive)
		{
			g.drawRect(x, y, scale, scale);
			//g.fillRect(x, y, scale, scale);
		}
	}
	
	public void updateState(ArrayList<Cell> neighbors, boolean artsy) 
	{
		int liveNeigh = this.countLivingCells(neighbors);
		
		if(!artsy)
		{
		
			if( (liveNeigh ==  2) && (this.alive) ) //Default rule set!
				this.setAlive();
			else if(liveNeigh == 3)
				this.setAlive();
			else
				this.kill();
		}
		else
		{
			if(liveNeigh == 2 || liveNeigh == 3) //Cool Shapes!
				this.setAlive();
			else
			this.kill();
		}
	}
	
	private int countLivingCells(ArrayList<Cell> toCount) //returns an int value of living cells in given array
	{
		int toReturn = 0;	
		for(Cell c : toCount)
			toReturn += (c.getAlive() ? 1 : 0);	
		return toReturn;
			
	}

	public String toString() //Returns "0" if dead, "1" if alive
	{
		return (this.alive ? "1" : "0");
	}

	public static void main(String[] args) 
	{
		Cell c = new Cell(true);
		System.out.println(c);
		System.out.println(c.getAlive());
		c.setAlive(false);
		System.out.println(c.getAlive());
		System.out.println(c);


	}

}