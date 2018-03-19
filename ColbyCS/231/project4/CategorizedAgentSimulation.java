package project4;

import java.util.Random;
import java.util.Scanner;

/*
 * CategorizedAgentSimulation.java
 * Owen Goldthwaite
 * 3/11/2018
 */
public class CategorizedAgentSimulation 
{
	public static void main(String[] args) throws InterruptedException 
	{
	 	Scanner scan = new Scanner(System.in);
	 	
	 	System.out.println("Enter X size of grid: ");
	 	int x = scan.nextInt();
	 	System.out.println("Enter Y size of grid: ");
	 	int y = scan.nextInt();
	 	System.out.println("Enter number of agents: ");
	 	int n = scan.nextInt();
	 	System.out.println("Enter the number of iterations: ");
	 	int i = scan.nextInt();
	 	System.out.println("Enter 1 for Categorized Simulation, 0 for normal Social Simulation.");
	 	int type = scan.nextInt();
	 	
	 	if(type == 0)
	 		runSocSimulation(x,y,n,i);
	 	else if(type == 1)
	 		runCatSimulation(x,y,n,i);
	}
	
	public static void runCatSimulation(int x, int y, int n, int iter) throws InterruptedException //Runs categorized simulation!
	{
		Landscape scape = new Landscape(x,y);
		LandscapeDisplay display = new LandscapeDisplay(scape); //Change this line when taking out of eclipse
		Random rand = new Random();
		
		for(int i = 0; i < n; i++) 
		{
			
			scape.addAgent( new CategorizedSocialAgent( rand.nextDouble() * scape.getWidth(),
											 			rand.nextDouble() * scape.getHeight(), 
											 			i%2 ) );
		}
		
		for(int i = 0; i < iter; i++)
		{
			scape.updateAgents(25);
			display.repaint();
			Thread.sleep(10);
		}
	}
	
	public static void runSocSimulation(int x, int y, int n, int iter) throws InterruptedException //Runs the simulation!
	{
		Landscape scape = new Landscape(x,y);
		LandscapeDisplay display = new LandscapeDisplay(scape); //Change this line when taking out of eclipse
		Random rand = new Random();
		
		for(int i = 0; i < n; i++) 
		{
			scape.addAgent( new SocialAgent( rand.nextDouble() * scape.getWidth(),
											 rand.nextDouble() * scape.getHeight() ) );
		}
		
		for(int i = 0; i < iter; i++)
		{
			scape.updateAgents(15);
			display.repaint();
			Thread.sleep(10);
		}
	}
}
