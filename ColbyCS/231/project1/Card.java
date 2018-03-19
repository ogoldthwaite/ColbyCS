package project1;
/*
 * File: Card.java
 * Author: Owen Goldthwaite
 * Date: 02/12/2018
 */

public class Card
{
	private int value;

	public Card()
	{
		value = (int)(Math.random()*10) + 1; //Maybe change to 11 if we use dem aces
	}

	public Card(int v)
	{
		if((v >= 1) && (v <= 10)) //Assuming Aces can be 1 not 11
			{ value = v; }
		else
			System.out.println("Card does not have correct value!"); //Do something
	}

	public int getValue()
	{
		return value;
	}
	
	public String toString()
	{
		String toReturn = "";
		toReturn += this.value;
		return toReturn;
	}

	public static void main(String[] args) 
	{
		Card testCardA = new Card(10);
		System.out.println(testCardA.getValue());

		Card testCardB = new Card();
		System.out.println(testCardB.getValue());

	}

}