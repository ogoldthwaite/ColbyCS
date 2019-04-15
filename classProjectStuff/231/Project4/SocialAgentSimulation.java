
import java.util.Random;
import java.util.Scanner;

/*
 * SocialAgentSimulation.java
 * Owen Goldthwaite
 * 3/11/2018
 */
public class SocialAgentSimulation 
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
	 	
	 	runSimulation(x,y,n,i);
	 	
	}
	
	public static void runSimulation(int x, int y, int n, int iter) throws InterruptedException //Runs the simulation!
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
