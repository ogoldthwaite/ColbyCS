package project7;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class WordCountRunner
{
	private static WordCounter wc;
	private static boolean useHashTable;
	
	public static void main(String[] args) throws FileNotFoundException 
	{		
		Scanner scan = new Scanner(System.in);
		System.out.println("Do you want to use a HashMap for this or not? Enter 1 for yes, 0 for no.");
		int choice1 = Integer.parseInt(scan.nextLine());
		
		if(choice1 == 1)
			useHashTable = true;
		else
			useHashTable = false;
		
		wc = new WordCounter(useHashTable);
		
		System.out.println("Are you analyzing a new file, analyzing a file 5 times, or reading in an old wordCountFile? Enter 0/1/2 respectively");
		int choice = Integer.parseInt(scan.nextLine());

		
		if(choice == 0)
			analyze(scan);
		else if(choice == 1)
			multAnalyze(scan);
		else
			readOld(scan);
		
		scan.close();
		
	}
	
	public static void multAnalyze(Scanner scan) throws FileNotFoundException //like analyze but runs 5 times and averages time to 3 middle ones
	{
		System.out.println("Enter the input file name: ");
		String inputFile = scan.nextLine();
	
		ArrayList<Long> times = new ArrayList<Long>();
		
		System.out.println("Analyzing 5 times...");
		System.out.println();
		
		for(int i = 0; i < 5; i++)
		{
			wc.resetMap(useHashTable); //resetting the map each time!
			
			long time = System.currentTimeMillis();	
			
			wc.analyze(inputFile);		
			time = System.currentTimeMillis() - time;	
			
			times.add(time);
			System.out.println("Analyse Time Taken for Analyze " + i +": " + time);
			
		}
		
		long maxT = times.get(0);
		long minT = times.get(0);
		
		System.out.println(times);
		
		for(int i = 0; i < times.size(); i++)
		{
			long time = times.get(i);						
			
			if(time > maxT)
				maxT = time;
			if(time < minT)
				minT = time;	
		}
		
		times.remove(maxT);
		times.remove(minT);
		System.out.println(times);
		
		long timeSum = 0;
		for (Long time : times) 
			timeSum += time;
		
		timeSum = timeSum / times.size();
		System.out.println("Average Time of Middle 3 Analyse Times: " + timeSum);
		System.out.println("Efficiency (Collisions or Height): " + wc.getMap().getEfficiency());
	}
	
	
	public static void analyze(Scanner scan) throws FileNotFoundException 
	{
		System.out.println("Enter the input file name: ");
		String inputFile = scan.nextLine();
		System.out.println("Enter the output file name: ");
		String outputFile = scan.nextLine();
		
		long time = System.currentTimeMillis();
		
		wc.analyze(inputFile);
		wc.writeWordCountFile(outputFile);
		System.out.println("Unique Word Count: " + wc.getMap().size());
		
		time = System.currentTimeMillis() - time;	
		System.out.println("Time Taken: " + time);
		
	}
	
	public static void readOld(Scanner scan) throws FileNotFoundException
	{
		System.out.println("Enter the input file name: ");
		String inputFile = scan.nextLine();
		System.out.println("Enter the output file name: ");
		String outputFile = scan.nextLine();
		
		long time = System.currentTimeMillis();
		
		wc.readWordCountFile(inputFile);
		wc.writeWordCountFile(outputFile);
		System.out.println("Unique Word Count: " + wc.getMap().size());
		
		time = System.currentTimeMillis() - time;		
		System.out.println("Time Taken: " + time);
	}
	
}
