package project2;

import java.util.Random;
import java.util.Scanner;

/*
*LifeSimulation.java
* Owen Goldthwaite
* 02/25/18
*/
public class LifeSimulation 
{
	public static void main(String[] args) throws InterruptedException
	{
	 	Scanner scan = new Scanner(System.in);
	 	
	 	System.out.println("Enter X size of grid: ");
	 	int x = scan.nextInt();
	 	System.out.println("Enter Y size of grid: ");
	 	int y = scan.nextInt();
	 	System.out.println("How many iterations do you want?");
	 	int iter = scan.nextInt();
	 	
	 	System.out.println("Do you want to use the the cool artsy rule set instead of default? Enter 1 for yes, 0 for no: ");
	 	int input = scan.nextInt();
	 	if(input == 1)
		{
			runSimulation(x,y,iter,false,true, 0);
		}
		else if(input == 0)
		{
			System.out.println("Do you want to see pre-set shapes? Enter 1/0: ");
			input = scan.nextInt();
			if(input == 1)
			{
				runSimulation(x,y,iter,false,false,0);
			}
			else
			{
				System.out.println("Ok, random game will be generated. Input density double: ");
				double density = scan.nextDouble();
				runSimulation(x,y,iter,true,false,density);
			}		
		}

		
		scan.close();
    }
	
	public static void runSimulation(int x, int y, int iter, boolean random, boolean artsy, double density) throws InterruptedException
	{
	 	
		Landscape scape = new Landscape(x,y);
	 	LandscapeDisplay display = new LandscapeDisplay(scape, 4);
	 	
	 	if(random)
	 	{	
	 		Random gen = new Random();
	 		for (int i = 0; i < scape.getRows(); i++) 
	 			for (int j = 0; j < scape.getCols(); j++ )  
	 				scape.getCell( i, j ).setAlive( gen.nextDouble() <= density );
	 	}
	 	else if (artsy)
	 	{
	 		scape.square();
	 	}
	 	else
	 		scape.shapes();
	 	
	 	Thread.sleep(250);
	        	
	 	for(int i = 0; i < iter; i++)
	 	{
	 		scape.advance(artsy);
	 		display.repaint();
	 		Thread.sleep(150);
	 	}
	}
	
	
}
