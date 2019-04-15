
/*
* Board.java for suduko
* Owen Goldthwaite
* 2/26/18
*/

import java.awt.Color;
import java.awt.Graphics;
import java.io.*;
import java.util.Random;


public class Board 
{
	
	private Cell[][] cells;
	public static int size = 9;

	public Board()
	{
		this.cells = new Cell[Board.size][Board.size];
		this.initializeBoard();
	}

	private void initializeBoard() //initializes cell values in the board
	{
		for (int i = 0; i < Board.size; i++) 
			for (int j = 0; j < Board.size; j++) 
			{
				Cell c = new Cell();
				cells[i][j] = c;
			}
	}

	public boolean read(String filename) //Reads the file and splits it based on format
	{
		int row = 0;
		try
		{
			FileReader file = new FileReader(filename);
			BufferedReader buff = new BufferedReader(file);

			while(true)
			{
				String line = buff.readLine();
				
				if(line == null)
					break;

				String[] words = line.split("[ ]+");
//				System.out.println(line);
//				System.out.println(words.length);
				
				for (int i = 0; i < words.length; i++)
				{
					cells[row][i].setValue(Integer.parseInt(words[i]));
					if(cells[row][i].getValue() != 0)
						cells[row][i].setLocked(true);
				}
				row++;
			}

			buff.close();
			return true;
		}
		catch(FileNotFoundException ex) 
		{	
      		System.out.println("Board.read():: unable to open file " + filename );
    	}
    	catch(IOException ex) 
    	{
      		System.out.println("Board.read():: error reading file " + filename);
    	}

    	return false;
    } 

    //Accessor things
    public int getCols()
    {
    	return Board.size;
    }

    public int getRows()
    {
    	return Board.size;
    }

    public Cell getCell(int r, int c)
    {
    	return cells[r][c];
    }

    public boolean isLocked(int r, int c)
    {
    	return cells[r][c].isLocked();
    }

    public int getValue(int r, int c)
    {
    	return cells[r][c].getValue();
    }

    public void setValue(int r, int c, int value)
    {
    	cells[r][c].setValue(value);
    }

    public void setValue(int r, int c, int value, boolean locked)
    {
    	cells[r][c].setValue(value);
    	cells[r][c].setLocked(locked);
    }

    public String toString() //returns a string of the board!
    {
    	String toReturn = "";

    	for (int i = 0; i < Board.size; i++) 
    	{
			for (int j = 0; j < Board.size; j++)
			{
				toReturn += cells[i][j].getValue() + " ";
				
				if( ((j + 1) % 3) == 0)
					toReturn += "  ";
			}
			toReturn += "\n";
			if( ((i + 1) % 3) == 0)
				toReturn += "\n";
    	}

    	return toReturn;
    }

    public boolean validValue(int row, int col, int value) //checks if value is valid in current spot
    {
    	if(value < 1 || value > 9)
    		return false;
    	
    	for (int i = 0; i < Board.size; i++) 
    	{
			if( (cells[row][i].getValue() == value) && (cells[row][i] != cells[row][col]) )
				return false;
			else if((cells[i][col].getValue() == value) && (cells[i][col] != cells[row][col]) )
				return false;
		}
    		 	
    	int rBooVar = (row/3) * 3;
    	int cBooVar = (col/3) * 3;
    	
    	for (int rVal = (row/3) * 3; rVal < (rBooVar + 3); rVal++) 
			for (int cVal = (col/3) * 3; cVal < (cBooVar + 3); cVal++) 
			{
				if( (cells[rVal][cVal].getValue() == value) && (cells[rVal][cVal] != cells[row][col]) )
					return false;
			}
    	
    	return true;
    }
    
    public boolean validSolution() //checks all board values and returns true/false depending on if board is valid
    {
    	for (int i = 0; i < Board.size; i++)
    		for (int j = 0; j < Board.size; j++) 
    		{
				if( (cells[i][j].getValue() == 0) || (this.validValue(i, j, cells[i][j].getValue()) == false) )
					return false;
			}
		return true;
    }
    
    public void draw(Graphics g, int scale) //calls every cells draw() method
    {	
    	for (int i = 0; i < Board.size; i++) 
    		for (int j = 0; j < Board.size; j++) 
				cells[i][j].draw(g, 10, 10, scale);//maybe change 10 and 10 to make it look better
    		
    		g.drawLine(0, 80, 260, 80);
    		g.drawLine(0, 170, 260, 170);
    		g.drawLine(87, 0, 87, 250);
    		g.drawLine(177, 0, 177, 250);
    
    }
    
    public int getNumSols(int row, int col) //Returns the number of valid solutions at location
    {										//Would be private but I may use it outside of this scope
    	int numSols = 0;
    	if(this.getCell(row, col).isLocked())
    		return 10000;
    	
    	for (int i = 1; i <= 9; i++)
    		if(validValue(row,col,i))
    			numSols++;
    	
    	return numSols;
    }
    
    public void generateNumSols() //Sets every cells numSols value for this board
    {
    	for (int i = 0; i < Board.size; i++) 
			for (int j = 0; j < Board.size; j++) 
				cells[i][j].setNumSols(this.getNumSols(i, j));
    }
    
    public void generateRowCol() //Sets row and col values of every cell.
    {
    	for (int i = 0; i < Board.size; i++) 
			for (int j = 0; j < Board.size; j++)
			{
				cells[i][j].setRow(i);
				cells[i][j].setCol(j);
			}
    }
    
    public static void main(String[] args)
    {
    	Board testBoard = new Board();
    	testBoard.read("board10Solved.txt");
    	System.out.println(testBoard);
    	
    	System.out.println(testBoard.validSolution());

//		testBoard.setValue(0,0,1);
//    	System.out.println(testBoard.getCell(0,0));
//    	testBoard.setValue(4,5,7, true);
//    	System.out.println(testBoard.getValue(4,5));
//
//    	System.out.println(testBoard);


    }

	
}

