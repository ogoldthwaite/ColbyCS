
/*
* Cell.java for suduko
* Owen Goldthwaite
* 2/26/18
*/

import java.awt.Color;
import java.awt.Graphics;
import java.util.Random;


public class Cell
{
	private int row;
	private int col;
	private int value;
	private boolean locked;
	private int numSols;
	private int index;

	public Cell() //constructors
	{
		this.row = 0;
		this.col = 0;
		this.value = 0;
		this.locked = false;
		this.index = 0;
	}

	public Cell(int row, int col, int value)
	{
		this.row = row;
		this.col = col;
		this.value = value;
		this.locked = false;
		this.numSols = 0;
		this.index = 0;
	}
	
	public Cell(int row, int col, int value, int numSols)
	{
		this.row = row;
		this.col = col;
		this.value = value;
		this.locked = false;
		this.numSols = numSols;
		this.index = 0;
	}
	
	public Cell(int row, int col, int value, boolean locked) 
	{
		this.row = row;
		this.col = col;
		this.value = value;
		this.locked = locked;
		this.numSols = 0;
		this.index = 0;
	}

	//Accessors
	public int getNumSols()
	{
		return this.numSols;
	}
	
	public void setNumSols(int sols)
	{
		this.numSols = sols;
	}
	
	public int getRow()
	{
		return this.row;
	}

	public int getCol()
	{
		return this.col;
	}
	
	public void setRow(int row)
	{
		this.row = row;
	}
	
	public void setCol(int col)
	{
		this.col = col;
	}

	public int getValue()
	{
		return this.value;
	}

	public void setValue(int newVal)
	{
		this.value = newVal;
	}
	
	public int getIndex()
	{
		return this.index;
	}

	public void setIndex(int index)
	{
		this.index = index;
	}
	
	public boolean isLocked()
	{
		return this.locked;
	}

	public void setLocked(boolean lock)
	{
		this.locked = lock;
	}

	public Cell clone() //returns a new cell this the same values as this
	{
		Cell newCell = new Cell(this.row, this.col, this.value, this.locked);
		return newCell;
	}
	
	public void draw(Graphics g, int x0, int y0, int scale) //draws the cells value!
	{
		Random rand = new Random();
		char[] c = new char[] {(char) ('0' + this.value)};
		g.setColor(new Color(rand.nextInt(255), rand.nextInt(255), rand.nextInt(255)));
		g.drawChars(c, 0, 1, this.getCol()*scale + 10, this.getRow()*scale+10);
	}

	public String toString()
	{
		return "" + this.row + ", " + this.col + ", " + this.value + ", " + this.numSols+ ", " + this.locked;
	}

	public static void main(String[] args) 
	{
		Cell c = new Cell(3,3,8);
		System.out.println(c);
		c.setLocked(true);
		c.setValue(5);
		System.out.println(c);


	}

}
