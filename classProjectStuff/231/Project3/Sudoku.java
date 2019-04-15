
import java.util.Comparator;
/*
* Sudoku.java for suduko
* Owen Goldthwaite
* 2/26/18
*/
import java.util.Random;
import java.util.Scanner;

public class Sudoku 
{
	private Board board;
	private int curRow;
	private int curCol;
	private LandscapeDisplay display;
	

	public Sudoku()
	{
		board = new Board();
		curRow = 0;
		curCol = 0;
		display = new LandscapeDisplay(this.board, 30); //scale is second parameter
	}
	
	public Sudoku(int num) //Constructor for random board with N locked values
	{
		board = new Board();
		curRow = 0;
		curCol = 0;
		Random rand = new Random();
		int r,c,val;
		
		for (int i = 0; i < num; i++) 
		{
			 r = rand.nextInt(8);
			 c = rand.nextInt(8);
			 val = rand.nextInt(8) + 1;
			
			 if( (board.getCell(r, c).getValue() == 0) && (board.validValue(r, c, val)) )
			 {
				 board.getCell(r, c).setValue(val);
				 board.getCell(r, c).setLocked(true);
			 }
			 else
			 {
				 i--;
				 continue;
			 }
			 
		}
		display = new LandscapeDisplay(this.board, 30);
	}
	
	public Board getBoard()
	{
		return this.board;
	}
	
	private void updateLoc() //updates curCol and curRow to location of next cell
	{
		if(curCol < 8) //This whole if stuff could be done wrong.
			curCol++;
		else if(curRow < 8)
		{
			curCol = 0;
			curRow++;
		}
		else
			System.out.println("Reached end of board! Probably");
	}
	
	private void delay(int delay) //delays and repaints display
	{
	    if( delay > 0 ) {
	        try {
	            Thread.sleep(delay);
	        }
	        catch(InterruptedException ex) {
	            System.out.println("Interrupted");
	        }
	        display.repaint();
	    }
	}
	
	public boolean solve(int delay)
	{
		CellStack stack = new CellStack(100);
		int curVal, time;
		curRow = 0;
		curCol = 0;
		curVal = 0;
		time = 1;
		board.generateRowCol();
		
		while(stack.size() < Board.size * Board.size)
		{
			time++;
			this.delay(delay);
			
			if(board.getCell(curRow, curCol).isLocked())
			{
				stack.push(board.getCell(curRow, curCol));
				
				this.updateLoc();
				
				continue;
			}
			
			for (int i = curVal; i <= 9; i++) 
			{
				if(board.validValue(curRow, curCol, curVal))
					break;

				curVal++;
			}
			
			if(board.validValue(curRow, curCol, curVal))
			{
				Cell c = new Cell(curRow, curCol, curVal);
				board.setValue(curRow, curCol, curVal);
				stack.push(c);
				this.updateLoc();
				curVal = 1;
			}
			else
			{
				if(stack.size() > 0)
				{
					Cell c = stack.pop();
					while(c.isLocked())
					{
						if(stack.size() > 0)
							c = stack.pop();
						else
						{
							System.out.println("Steps: " +time);
							return false;
						}
					}
					curRow = c.getRow();
					curCol = c.getCol();
					curVal = c.getValue() + 1;
					board.setValue(curRow, curCol, 0);
				}
				else
				{
					System.out.println("Steps: " +time);
					return false;
				}
					
			}
			
		} //end of while loop
		
		System.out.println("Steps: " +time);
		return true;
	}
		
	public boolean otherSolve(int delay) 
	{
		CellStack stack = new CellStack(100);
		int curVal, time, curInd;
		curRow = 0;
		curCol = 0;
		curVal = 0;
		curInd = 0;
		time = 1;
		
		board.generateNumSols();
		board.generateRowCol();
		
		Comparator<Cell> comp = new CellComparator();
		Cell[] cArray = new Cell[Board.size * Board.size];
		
		int index = 0;
		
		for (int i = 0; i < Board.size; i++) //creating array of all cells on board
			for (int j = 0; j < Board.size; j++)
				cArray[index++] = board.getCell(i, j);
		
		HeapSort.sort(cArray, comp);
		
		for (int i = 0; i < cArray.length; i++) //Setting each cells index field
			cArray[i].setIndex(i);
			
		
		while(stack.size() < Board.size * Board.size)
		{
			time++;
			this.delay(delay);
			
			if(cArray[curInd].isLocked())
			{
				stack.push(cArray[curInd]);
				curInd++;	
				continue;
			}
			
			for (int i = curVal; i <= 9; i++) 
			{
				if(board.validValue(cArray[curInd].getRow(), cArray[curInd].getCol(), curVal)) 
					break;
				
				curVal++;
			}
			
			if(board.validValue(cArray[curInd].getRow(), cArray[curInd].getCol(), curVal)) 
			{
				Cell c = new Cell(cArray[curInd].getRow(), cArray[curInd].getCol(), curVal);
				c.setIndex(board.getCell(cArray[curInd].getRow(), cArray[curInd].getCol()).getIndex());
				board.setValue(cArray[curInd].getRow(), cArray[curInd].getCol(), curVal);
				stack.push(c);
				curInd++;
				curVal = 1;
			}
			else
			{
				if(stack.size() > 0)
				{
					Cell c = stack.pop();
					while(c.isLocked())
					{
						if(stack.size() > 0) //pop till unlocked
							c = stack.pop();
						else
						{
							System.out.println("Steps: " +time);
							return false;
						}
					}
					curInd = c.getIndex();
					curVal = c.getValue() + 1;
					board.setValue(cArray[curInd].getRow(), cArray[curInd].getCol(), 0);
				}
				else
				{
					System.out.println("Steps: " + time);
					return false;
				}
					
			}
			
		} //end of while loop
		
		System.out.println("Steps: " +time);
		return true;
	}
			
	public static void main(String[] args) 
	{
		Scanner scan = new Scanner(System.in);
		System.out.println("How many random numbers do you want in the board? Enter: ");
		int n = scan.nextInt();
		Sudoku game = new Sudoku(n);
		System.out.println("Enter Delay in ms: ");
		int delay = scan.nextInt();
		//game.getBoard().read("board10.txt");
		System.out.println("--Initial Board--");
		System.out.println();
		System.out.println(game.getBoard());
		System.out.println();
		System.out.println("Enter 1 for default solve, 0 for other HeapSort solve.");
		int x = scan.nextInt();
		if(x == 1)
			game.solve(delay);
		else
			game.otherSolve(delay);
		
		System.out.println(game.getBoard());
		System.out.println(game.getBoard().validSolution());
		
		scan.close();
	}
	
	
	
}
