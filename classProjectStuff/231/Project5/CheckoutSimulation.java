
/*
 * CheckoutSimulation.java
 * Owen Goldthwaite
 * 3/18/2018
 */
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class CheckoutSimulation 
{
	public static int tick = 0; //tick variable incremented each run of main loop
	private static float slowCashChance; //Chance of a cashier being a slow cashier
	
	public static void main(String[] args) throws InterruptedException 
	{
	 	Scanner scan = new Scanner(System.in);
		
		System.out.println("Enter X size of grid: ");
	 	int x = scan.nextInt();
	 	System.out.println("Enter Y size of grid: ");
	 	int y = scan.nextInt();
	 	System.out.println("Enter number of checkout lines/cashiers: ");
	 	int c = scan.nextInt();
	 	System.out.println("Enter line selection method: 0 = random line, 1 = random of two, 2 = shortest of all, -1 = random method");
	 	Customer.method = scan.nextInt();
	 	System.out.println("How many new customers should there be each tick?");
	 	Spawner.count = scan.nextInt();
	 	System.out.println("Enter Decimal Value between 0 and 1 for chance of slow cashier (i.e. .2 for 20%): ");
	 	slowCashChance = scan.nextFloat();
	 	System.out.println("Enter Decimal Value between 0 and 1 for chance of Impatient Customer (i.e. .2 for 20%): ");
	 	System.out.println("A low value (< .1) is highly reccomended! Chance is only applied every 75 ticks" );
	 	Spawner.impChance = scan.nextFloat();
	 	
	 	runSimulation(x,y,c);
	 	
	 	scan.close();
	}
	
	public static void runSimulation(int x, int y, int c) throws InterruptedException
	{
		Landscape scape = new Landscape(x,y);
		LandscapeDisplay display = new LandscapeDisplay(scape);
		
		
		scape.addAgent(new Spawner(x/2, y/2));
		
		int spacing = x/c;
		Random rand = new Random();
		for (int i = 0; i < c; i++) 
		{
			if(rand.nextFloat() < slowCashChance) //Chance that cashier will be a slow cashier
				scape.addAgent(new SlowCashier(spacing*i, y-10));
			else
				scape.addAgent(new Cashier(spacing*i, y-10));
		}
		
		for(int i = 0; i < 500; i++)
		{
			scape.updateAgents();
			display.repaint();
			Thread.sleep(10);
			tick++;
			
			if(i%100 == 0)
			{
				System.out.println("Standard Deviation of Checkout Times: " + stDev(scape.getTimeList()));
				System.out.println("Average Deviation of Checkout Times: " + avgDev(scape.getTimeList()));
				System.out.println("Average Checkout Time: " + avg(scape.getTimeList()));
				System.out.println("Total Time: " + scape.getTotalTime());		
			}
		}
		
		System.out.println(scape.getTotalTime());
		System.out.println("--CLEARING LINES--");
		System.out.println("--THIS COULD TAKE A SECOND--");	
		Landscape.clearingLines = true;
		
		Spawner.spawn = false;
		ArrayList<Cashier> counters = scape.getCashiers();
		Cashier longest = counters.get(0);
		
		for(Cashier cash : counters)
		{
			for(Customer cust : cash.getLine())
				if(cust.getClass() == ImpatientCustomer.class) //Impatient customers leave
				{
					cust = null;
				}
			
			if(cash.queueLength() > longest.queueLength())
				longest = cash;
		}
		while(longest.queueLength() != 0)
		{
			scape.updateAgents();
			display.repaint();
			Thread.sleep(5);
			tick++;
		}
				
		System.out.println("Total Customers Satisfied: " + scape.getTimeList().size());
		System.out.println("Final Total Time: " + scape.getTotalTime());
		System.out.println("Standard Deviation of Checkout Times: " + stDev(scape.getTimeList()));
		System.out.println("Average Deviation of Checkout Times: " + avgDev(scape.getTimeList()));
		System.out.println("Average Checkout Time: " + avg(scape.getTimeList()));
		
	}
	
	public static double avgDev(ArrayList<Double> list)
	{
		double mean = 0.0;
		for(Double i : list)
			mean += i;
		mean = mean / list.size();
		
		double sum = 0.0;
		for(int i = 0; i < list.size(); i++)
		{
			list.set(i, Math.abs(list.get(i) - mean));
			sum += list.get(i);
		}
		return sum/list.size();
		
	}
	
	public static double avg(ArrayList<Double> list)
	{
		double mean = 0.0;
		for(Double i : list)
			mean += i;
		mean = mean / list.size();
		
		return mean;
	}
	
	public static double stDev(ArrayList<Double> list) //Population Standard Deviation
	{
		double mean = 0;
		for(Double i : list)
			mean += i;
		mean = mean / list.size();
		
		double sum = 0.0;
		for(int i = 0; i < list.size(); i++)
		{
			list.set(i, Math.pow((list.get(i)-mean),2));
			sum += list.get(i);
		}
		
		sum = sum/list.size();
		
		return Math.sqrt(sum);
	}
}
