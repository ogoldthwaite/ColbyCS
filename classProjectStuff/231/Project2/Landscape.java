
/*
* Landscape.java
* Owen Goldthwaite
* 02/19/18
*/
import java.util.*;
import java.awt.Color;
import java.awt.Graphics;

public class Landscape
{
	private int rows;
	private int cols;
	private Cell[][] cells;

	public Landscape( int rows, int cols)
	{
		this.rows = rows;
		this.cols = cols;
		cells = new Cell[rows][cols];
		this.makeTestCells();
	}

	public int getRows()
	{
		return this.rows;
	}

	public int getCols()
	{
		return this.cols;
	}

	public Cell getCell( int row, int col)
	{
		return cells[row][col];
	}

	public void reset()
	{
		for (int i = 0; i < this.rows; i++)
			for (int j = 0; j < this.cols; j++) 
			{
				if(cells[i][j].getAlive())
					cells[i][j].kill(); 	
			} 		
	}

	public void makeTestCells()
	{
		//Random rand = new Random();
		for (int i = 0; i < this.rows; i++)
			for (int j = 0; j < this.cols; j++) 
			{
				Cell c = new Cell();
				cells[i][j] = c;	
			} 
	}

	public boolean checkBound(int r, int c)
	{
		if(r < 0 || c < 0)
			return false;
		else if( (r > this.rows - 1) || (c > this.cols - 1) )
			return false;
		else
			return true;

	}

	public ArrayList<Cell> getNeighbors( int r, int c) //Currently returns all neighbors, alive or dead. Change possibly?
	{
		ArrayList<Cell> neighbors = new ArrayList<Cell>();

		if( checkBound(r-1, c-1) )
			neighbors.add(cells[r-1][c-1]);
		if( checkBound(r-1, c) )
			neighbors.add(cells[r-1][c]);
		if( checkBound(r-1, c+1) )
			neighbors.add(cells[r-1][c+1]);
		if( checkBound(r, c-1) )
			neighbors.add(cells[r][c-1]);
		//Center would go here
		if( checkBound(r, c+1) )
			neighbors.add(cells[r][c+1]);
		if( checkBound(r+1, c-1) )
			neighbors.add(cells[r+1][c-1]);
		if( checkBound(r+1, c) )
			neighbors.add(cells[r+1][c]);
		if( checkBound(r+1, c+1) )
			neighbors.add(cells[r+1][c+1]);

		return neighbors;
	}

	public void draw( Graphics g, int gridScale ) //draws all the cells
	{
		Random rand = new Random();
		g.setColor(new Color(rand.nextInt(255), rand.nextInt(255), rand.nextInt(255)));
		
		for (int i = 0; i < this.getRows(); i++) 
			for (int j = 0; j < this.getCols(); j++) 
				this.cells[i][j].draw(g, i*gridScale, j*gridScale, gridScale);
	}
	
	public void advance(boolean artsy)
	{
		Cell[][] tempCells =  new Cell[this.rows][this.cols];
		
		for (int i = 0; i < this.rows; i++)
			for (int j = 0; j < this.cols; j++) 
			{
				Cell c = new Cell(cells[i][j].getAlive());
				tempCells[i][j] = c;	
			} 
		
		for (int i = 0; i < this.rows; i++)
			for (int j = 0; j < this.cols; j++) 
			{
				tempCells[i][j].updateState(this.getNeighbors(i, j), artsy);	
			}
		
		cells = tempCells;
		
	}

	public void print()
	{
		for (int i = 0; i < this.rows; i++)
		{
			for (int j = 0; j < this.cols; j++) 
			{
				System.out.print(cells[i][j] + " ");	
			} 
			System.out.println();
		}

	}

	private void life(int r, int c) //Just sets cell at r c to alive so shapes is more readable
	{
		cells[r][c].setAlive();
	}
	
	public void shapes() //Makes a still life square, a rotating line thing, and a glider
	{
		int r = (this.rows / 3);
		int c = (this.cols / 3);
		if( (this.rows >= 100) && (this.cols >= 100) )
		{		
			life(r,c);
			life(r,c+1);
			life(r+1,c);
			life(r+1,c+1);
			
			r += 4;
			c += 3;
			
			life(r,c);
			life(r+1,c);
			life(r+2,c);
			
			c -= 3;
			r += 14;
			
			life(r+1, c);
			life(r+2, c+1);
			life(r, c+2);
			life(r+1, c+2);
			life(r+2, c+2);
		
		}
	}
	
	public void square() //Just makes a square to demonstrate "Artsy" conditions.
	{
		int r = (this.rows / 3);
		int c = (this.cols / 3);
		
		life(r,c);
		life(r,c+1);
		life(r+1,c);
		life(r+1,c+1);
		
	}
	
	public static void main(String[] args) 
	{
		Landscape test = new Landscape(5, 5);
		test.makeTestCells();
		test.getCell(1,1).setAlive();
		test.print();
		ArrayList<Cell> neigh =  test.getNeighbors(2, 0);
		//neigh.removeAll(Collections.singleton(0));
		System.out.println(neigh);
	}




}