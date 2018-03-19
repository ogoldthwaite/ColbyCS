package project5;
/*
 * Spawner.java
 * Owen Goldthwaite
 * 3/18/2018
 */
import java.util.Random;

public class Spawner extends Agent
{		
	public static boolean spawn = true; //used for clearing lines later
	public static int count = 5;
	
	public Spawner(double x0, double y0)
	{
		super(x0,y0);
	}
	
	public void updateState(Landscape scape) //loop dictates how many customers are made
	{
		Random rand = new Random();
		
		if(spawn)
		{
			for (int i = 0; i < count; i++) 			
				scape.addAgent(new Customer( rand.nextDouble() * scape.getWidth(), rand.nextDouble()*scape.getHeight() ) );	
		}
	}
	
	

}