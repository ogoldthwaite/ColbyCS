
/**
 * File: Deck.java
 * Author: Owen Goldthwaite
 * Date: 02/12/2018
 */

import java.util.*;

public class Deck
{
	private ArrayList<Card> deck;

	public Deck()
	{
		deck = new ArrayList<Card>();
		build();
	}

	public ArrayList<Card> getDeck()
	{
		return deck;
	}
 
 	public void build()
 	{
 		deck.clear();
 		for (int k = 0; k < 4; k++) 
 		{	
 			for (int i = 1; i <= 9; i++) 
 			{
 				Card c = new Card(i);
 				deck.add(c);	
 			}
 		}

 		for (int i = 0; i < 16; i++) 
 		{
 			Card c = new Card(10);
 			deck.add(c);	
 		}
 	}

 	public Card deal()
 	{
 		return deck.remove(0);
 	}

 	public Card pick(int i)
 	{
 		return deck.remove(i);
 	}

 	public void shuffle()
 	{
 		Random rand = new Random(System.currentTimeMillis());
 		List<Card> newList = new ArrayList<Card>(deck);
 		deck.clear();
 		
		while(newList.size() > 0)
			deck.add(newList.remove(rand.nextInt(newList.size())));
 	}
 	
 	public String toString()
 	{
 		String toReturn = "";
 		for(Card c : deck)
 			toReturn += c.getValue() + ",";
 		return toReturn;
 	}

 	public static void main(String[] args) 
 	{
 		Deck testDeck = new Deck();
 		System.out.println(testDeck);
 		testDeck.shuffle();
 		System.out.println(testDeck);

// 		for (Card c : testDeck.getDeck()) 
// 		{
// 			System.out.println(c.getValue());
// 		}
// 		System.out.println(testDeck.getDeck().size());
// 		System.out.println(testDeck.deal());
// 		System.out.println(testDeck.pick(0));


 	}
}