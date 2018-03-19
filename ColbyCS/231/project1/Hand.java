package project1;
/**
 * File: Hand.java
 * Author: Owen Goldthwaite
 * Date: 02/12/2018
 */

import java.util.*;

public class Hand
{
	private ArrayList<Card> hand;

	public Hand()
	{
		hand = new ArrayList<Card>();
	}

	public void reset()
	{
		hand.clear();
	}

	public void add(Card card)
	{
		hand.add(card);
	}

	public int size()
	{
		return hand.size();
	}
	
	public ArrayList<Card> getHand()
	{
		return hand;
	}

	public Card getCard(int i)
	{
		return hand.get(i);
	}

	public int getTotalValue()
	{
		int sum = 0;
		for (Card c : hand) 
		{
			sum += c.getValue();
		}

		return sum;
	}

	public String toString()
	{
		String toReturn = "";
		for (Card c : hand) 
		{
			toReturn += (c.getValue() + " ");
		}
	
		return toReturn;
	}

	public static void main(String[] args) 
	{
		Hand handTest = new Hand();
		Card testCardA = new Card(10);
		Card testCardB = new Card(6);
		
		handTest.add(testCardA);
		handTest.add(testCardB);

		System.out.println(handTest.getCard(1));
	}

}