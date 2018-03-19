package project3;

import java.util.EmptyStackException;

/*
* CellStack.java for suduko
* Owen Goldthwaite
* 2/26/18
*/

public class CellStack
{
	private Cell[] stack;
	private int maxSize;
	private int top;

	public CellStack() //Constructors
	{
		stack = new Cell[10];
		maxSize = 10;
		top = 0;
	}

	public CellStack(int length)
	{
		stack = new Cell[length];
		maxSize = 10;
		top = 0;
	}

	public void push(Cell c)
	{
		if(this.top == this.maxSize)
		{
			Cell[] newStack = new Cell[ (this.stack.length * 2)+1 ];
			
			for (int i = 0; i < this.stack.length; i++ ) 
				newStack[i] = this.stack[i];

			this.stack = newStack;
		}

//		if(!(this.contains(c)))   //Uncomment if you dont want duplicates
			this.stack[top++] = c;
	}

	public Cell pop() //pops top!
	{
		if(isEmpty())
			throw new EmptyStackException();
		else
			return this.stack[--top];
	}

	public Cell peek() //peeks top!
	{
		if(isEmpty())
			throw new EmptyStackException();
		else
			return this.stack[top - 1];
	}

	public int size() //returns size!
	{
		return top;
	}

	public boolean isEmpty() //returns true if empty, false if not!
	{
		return (top == 0);
	}
	
	public boolean contains(Cell c) //returns true if cell is in stack, false if not
	{
		for (int i = 0; i < stack.length; i++)
		{
			if(stack[i] == c)
				return true;
		}
		
		return false;
	}

	public static void main(String[] args) 
	{
		CellStack testStack = new CellStack();
		
		for (int i = 0; i < 5; i++) 
		{
			Cell c = new Cell(0,0,i);
			testStack.push(c);	
		}
		System.out.println(testStack.isEmpty());
		System.out.println(testStack.size());
		System.out.println(testStack.pop());
		System.out.println(testStack.pop());
		System.out.println(testStack.peek());
		System.out.println(testStack.isEmpty());
		System.out.println(testStack.pop());
		System.out.println(testStack.pop());
		System.out.println(testStack.pop());
		System.out.println(testStack.isEmpty());
	}

}