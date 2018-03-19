package project4;

import java.util.Random;
import java.util.Scanner;

/*
 * AgentSimulation.java has user input to decide which simulation to run
 * Owen Goldthwaite
 * 3/11/2018
 */
public class AgentSimulation 
{
	private static final int delay = 10; //in case you want to change the delay
	
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
	 	System.out.println("Enter a radius to be used for the simulation: ");
	 	double r = scan.nextDouble();
	 	System.out.println("Enter 0 for normal sim, 1 for categorized, 2 for antisocial, 3 for bully, 4 for mixed, 5 for normal social+categorized.");
	 	int type = scan.nextInt();
	 	
	 	switch(type)
	 	{
	 	case 0:
	 		runSocSimulation(x,y,n,i,r);
	 	case 1:
	 		runCatSimulation(x,y,n,i,r);
	 	case 2:
	 		runAntiSocSimulation(x,y,n,i,r);
	 	case 3:
	 		runBullySimulation(x,y,n,i,r);
	 	case 4:
	 		runMixedSimulation(x,y,n,i,r);
	 	case 5:
	 		runSocAndCatSimulation(x,y,n,i,r);
	 	}
	 	
	 	scan.close();
	}
	
	public static void runCatSimulation(int x, int y, int n, int iter, double r) throws InterruptedException //Runs categorized simulation!
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
			scape.updateAgents(r);
			display.repaint();
			Thread.sleep(delay);
		}
	}
	
	public static void runSocSimulation(int x, int y, int n, int iter, double r) throws InterruptedException //Runs the simulation with all normal social agents!
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
			scape.updateAgents(r);
			display.repaint();
			Thread.sleep(delay);
		}
	}

	public static void runAntiSocSimulation(int x, int y, int n, int iter, double r) throws InterruptedException //Runs the simulation with all antisocial agents!
	{
		Landscape scape = new Landscape(x,y);
		LandscapeDisplay display = new LandscapeDisplay(scape); //Change this line when taking out of eclipse
		Random rand = new Random();
		
		for(int i = 0; i < n; i++) 
		{
			scape.addAgent( new AntiSocialAgent( rand.nextDouble() * scape.getWidth(),
											     rand.nextDouble() * scape.getHeight() ) );
		}
		
		for(int i = 0; i < iter; i++)
		{
			scape.updateAgents(r);
			display.repaint();
			Thread.sleep(delay);
		}
	}

	public static void runBullySimulation(int x, int y, int n, int iter, double r) throws InterruptedException //Runs a simulation of bullies and normal social agents to demonstrate the interaction
	{
		Landscape scape = new Landscape(x,y);
		LandscapeDisplay display = new LandscapeDisplay(scape); //Change this line when taking out of eclipse
		Random rand = new Random();
		
		for(int i = 0; i < n; i++) 
		{		
			scape.addAgent( new BullyAgent( rand.nextDouble() * scape.getWidth(),
											 			rand.nextDouble() * scape.getHeight(), 
											 			1337 ) );
			if(i%2 == 0)
				scape.addAgent( new SocialAgent( rand.nextDouble() * scape.getWidth(),
			 									rand.nextDouble() * scape.getHeight() ) );	
		}
		
		for(int i = 0; i < iter; i++)
		{
			scape.updateAgents(r);
			display.repaint();
			Thread.sleep(delay);
		}
	}

	public static void runMixedSimulation(int x, int y, int n, int iter, double r) throws InterruptedException //Runs the simulation with a random selection of agent types!
	{
		Landscape scape = new Landscape(x,y);
		LandscapeDisplay display = new LandscapeDisplay(scape); //Change this line when taking out of eclipse
		Random rand = new Random();
		
		for(int i = 0; i < n; i++) 
		{
			int type = rand.nextInt(4);
			
			switch(type)
			{
			case 0: scape.addAgent( new SocialAgent( rand.nextDouble() * scape.getWidth(),
				     									rand.nextDouble() * scape.getHeight() ) );
			
			case 1: scape.addAgent( new CategorizedSocialAgent( rand.nextDouble() * scape.getWidth(),
				     									 rand.nextDouble() * scape.getHeight(), i%2 ) );
			
			case 2: scape.addAgent( new AntiSocialAgent( rand.nextDouble() * scape.getWidth(),
				     									 rand.nextDouble() * scape.getHeight() ) );
			
			case 3: scape.addAgent( new BullyAgent( rand.nextDouble() * scape.getWidth(),
				     									 rand.nextDouble() * scape.getHeight(), 1337 ) );		
			}
					
		}
		
		for(int i = 0; i < iter; i++)
		{
			scape.updateAgents(r);
			display.repaint();
			Thread.sleep(delay);
		}
	}

	public static void runSocAndCatSimulation(int x, int y, int n, int iter, double r) throws InterruptedException //Runs the simulation with a random selection of agent types!
	{
		Landscape scape = new Landscape(x,y);
		LandscapeDisplay display = new LandscapeDisplay(scape); //Change this line when taking out of eclipse
		Random rand = new Random();
		
		for(int i = 0; i < n; i++) 
		{
			int type = rand.nextInt(2);
			
			switch(type)
			{
			case 0: scape.addAgent( new SocialAgent( rand.nextDouble() * scape.getWidth(),
				     									rand.nextDouble() * scape.getHeight() ) );
			
			case 1: scape.addAgent( new CategorizedSocialAgent( rand.nextDouble() * scape.getWidth(),
				     									 rand.nextDouble() * scape.getHeight(), i%2 ) );					
			}
					
		}
		
		for(int i = 0; i < iter; i++)
		{
			scape.updateAgents(r);
			display.repaint();
			Thread.sleep(delay);
		}
	}
}

