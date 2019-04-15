package project1;

import java.util.*;

/**
 * File: Blackjack.java
 * Author: Owen Goldthwaite
 * Date: 02/18/2018
 */
public class Blackjack 
{
	private Deck deck;
	private Hand pHand;
	private Hand dHand;
	private int pScore; //I'm assuming these count the number of wins?
	private int dScore;
	private int bet;
	private int cash;
	
	public Blackjack()
	{
		deck = new Deck();
		pHand = new Hand();
		dHand = new Hand();
		pScore = 0;
		dScore = 0;
		bet = 0;
		cash = 1000;
		reset(true);
	}
	
	public void reset(boolean newDeck) //Resets the game if newDeck is true, Hand if false. My understanding.
	{
		if(newDeck)
		{
			pHand.reset();
			dHand.reset();
			deck.build();
		}
		else
		{
			pHand.reset();
			dHand.reset();
		}		
		
		deck.shuffle();	
		deal();
	}
	
	public void deal()
	{
		pHand.add(deck.deal()); //player
		dHand.add(deck.deal()); //dealer
		pHand.add(deck.deal()); //player
		dHand.add(deck.deal()); //dealer
	}
	
	public boolean playerTurn()
	{
		while(pHand.getTotalValue() < 14)
		{
			pHand.add(deck.deal());
		}
		
		if(pHand.getTotalValue() <= 21)
			return true;
		else
			return false;
		
	}
	
	public boolean dealerTurn()
	{
		while(dHand.getTotalValue() < 17)
		{
			dHand.add(deck.deal());
		}
		
		if(dHand.getTotalValue() <= 21)
			return true;
		else
			return false;
	}
	
	public Hand getDealer()
	{
		return dHand;
	}
	
	public Hand getPlayer()
	{
		return pHand;
	}
	
	public String toString()
	{
		String toReturn = "";
		toReturn += "pScore: " + pScore + " || " + "dScore: " + dScore + "\n" 
					+ "pHand: " + pHand.getTotalValue() + " || " + "dHand: " + dHand.getTotalValue();	
		return toReturn;
	}
	
	public void playAutoGame()
	{
		boolean pDead = this.playerTurn(); //True is alive, False is busted
		boolean dDead = this.dealerTurn();
		
		if(deck.getDeck().size() < 26)
			deck.shuffle();
		
		if( (pDead == dDead) && (!pDead) )
			System.out.print(""); //Push
		else if( (pDead) && (!dDead) )
			pScore++;
		else if( (!pDead) && (dDead) )
			dScore++;
		else if(pHand.getTotalValue() == dHand.getTotalValue())
			System.out.print(""); //Push
		else 
		{
			boolean pWin;
			pWin = (pHand.getTotalValue() > dHand.getTotalValue() ? true : false);
			if(pWin)
				pScore++;
			else
				dScore++;
		}
	}
	
	public int simulationGame()
	{
		this.playAutoGame();	
		
		if(pScore == dScore)
			return 0;
		else
			return (pScore > dScore ? 1 : -1);
	}
	
	public int readInput()
	{
		Scanner scan = new Scanner(System.in);
		System.out.println("----------");
		System.out.println("Your Move: Enter 1 for hit, 2 for Stand, 3 for Double Down");
		
		String val = scan.nextLine();
		scan.close();
		if(val.equals("1"))
			return 1;
		else if(val.equals("2"))
			return 0;
		else
			return -1;
	}
	
	public boolean valueCards()
	{
		int pVal = pHand.getTotalValue();
		int dVal = dHand.getTotalValue();
		
		if(pVal > dVal)
			return true;
		else
			return false;		
	}
	
	public boolean considerContinue(int action)
	{
		int pVal = pHand.getTotalValue();
		int dVal = dHand.getTotalValue();
		
		if( (pVal > 21 && dVal > 21) )
		{
			System.out.println("Push! You win nothing!");
			return true;
		}
		else if( (pVal < 21 && dVal > 21) )
		{
			System.out.println("Player Win! You win "+ bet*2);
			cash += bet*2;
			return true;
		}
		else if( (pVal > 21 && dVal <21) )
		{
			System.out.println("You lose! Lost " + bet + " dollars!");
			return true;
		}
		else if( action == 0)
		{
			boolean x;
			x = valueCards();
			if(x)
			{
				System.out.println("Player Win! You win $"+ bet*2);
				cash += bet*2;
				return true;
			}
			else
			{
				System.out.println("You lose! Lost " + bet + " dollars!");
				return true;
			}
		}
		
		return false;
	}
	
	public boolean manageCards(int action)
	{
		if(action == 1)
			pHand.add(deck.deal());
		else if(action == 0)
			dealerTurn();
			
		else
		{
			bet = bet * 2;
			pHand.add(deck.deal());
			return considerContinue(action);
		}
		
		return considerContinue(action);	
	
	}
		
	public void playNormalGame()
	{
		bet = 0;
		boolean end = false;
		boolean haveBet = false;
		Scanner scan = new Scanner(System.in);
		
		while(!end)
		{
			if(!haveBet)
			{
			System.out.println("You have $" + cash + " How much do you want to bet? Enter Amount: ");
			int num = scan.nextInt();
			cash -= num;
			bet = num;
			haveBet = true;
			}
			
			System.out.print("Your Cards: ");
			for( Card c : this.getPlayer().getHand())
				System.out.print(c +" ");
			
			System.out.println();
			System.out.println("Dealers Face-up Card: " + this.getDealer().getHand().get(0));

			end = manageCards(readInput());
		}
		System.out.println("You now have $" + cash);
		System.out.println("----------");
		System.out.println("Play Again? Enter Y for yes, Anything else for no");
		String input = scan.nextLine();
		System.out.println(input);
		
			scan.close();
			this.playNormalGame();
				
	}
	
	public static void main(String[] args) 
	{
		Blackjack game = new Blackjack();
		System.out.println(game);
		System.out.println("------------");
		game.playAutoGame();
		System.out.println(game);
		//game.playNormalGame();
	
	}
	
	
}
