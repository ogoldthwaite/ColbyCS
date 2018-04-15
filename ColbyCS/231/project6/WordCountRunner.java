package project6;

import java.io.FileNotFoundException;
import java.util.Scanner;

public class WordCountRunner
{
	private static WordCounter<String, Integer> wc = new WordCounter<String, Integer>();
	
	public static void main(String[] args) throws FileNotFoundException 
	{		
		Scanner scan = new Scanner(System.in);
		System.out.println("Are you analyzing a new file or reading in an old wordCountFile? Enter 0/1 respectively");
		int choice = Integer.parseInt(scan.nextLine());

		
		if(choice == 0)
			analyse(scan);
		else
			readOld(scan);
		
		scan.close();
		
	}
	
	public static void analyse(Scanner scan) throws FileNotFoundException 
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
