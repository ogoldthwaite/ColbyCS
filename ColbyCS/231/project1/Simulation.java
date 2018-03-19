package project1;
/**
 * File: Simulation.java
 * Author: Owen Goldthwaite
 * Date: 02/18/2018
 */
public class Simulation 
{
	
	public static void main(String[] args)
	{
		double pWins = 0.0, dWins = 0.0, pushes = 0.0;
		int numGames = 10000000;
		
		for (int i = 0; i < numGames; i++) 
		{
			Blackjack game = new Blackjack();
			int val = game.simulationGame();
			
			if(val == 1)
				pWins++;
			else if (val == 0)
				pushes++;
			else
				dWins++;
		}
	
		System.out.println("Player Wins: " + pWins + " or " + pWins/numGames*100 + "%");
		System.out.println("Dealer Wins:" + dWins + " or " + dWins/numGames*100 + "%");
		System.out.println("Pushes: " + pushes + " or " + pushes/numGames*100 + "%");
		
	
	}
	
}
