package project8;
/*FindCommondWords.java finds trends.java
 * Owen Goldthwaite
 * April 22, 2018
 */

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;


public class FindTrends 
{
	
	public static void CreateTrends() throws InterruptedException, FileNotFoundException
	{
		Scanner scan = new Scanner(System.in);
		System.out.println("Enter Information in the following format!");
		System.out.println("<FileName> <FileBegin (i.e. 2008)> <FileEnd> <word1> <word2> ... <wordn>");
		String input = scan.nextLine();
		
		String[] words  = input.split(" ");
		String fileName = words[0];
		Integer fileBegin  = new Integer(words[1]);
		Integer fileEnd = new Integer(words[2]);
		
		ArrayList<String> toFind = new ArrayList<String>(); //Creating list of interesting words
		for (int i = 3; i < words.length; i++) 
			toFind.add(words[i]);
		
		ArrayList<WordCounter> wordCounters = new ArrayList<WordCounter>();
		for( int i = 0; i < fileEnd+1 - fileBegin; i++) //Creating a new wordcounter for difference in file num
		{
			int fileNum = fileBegin+i;
			wordCounters.add(new WordCounter(fileName+fileNum+".txt", true)); //creates a new wordcounter
		}
		
		ArrayList<Thread> threads = new ArrayList<Thread>();
		for (WordCounter wc : wordCounters) //Creating and running a thread for each file, analyzing all at once
		{
			Thread t = new Thread(wc);
			threads.add(t);
			t.start();
		}
		
		for (Thread t : threads) //joining every thread so doesnt continue until all are analyzed
			t.join();
			
		String toPrint = ""; //printing to console
		for (String word : toFind) 
		{
			toPrint += word + ", ";
			
			for (WordCounter wc : wordCounters) 
				toPrint += wc.getFreq(word) + ", ";
			
			toPrint += "\n";
		}
		
		System.out.println(toPrint);
		
		//Printing to a .csv!!
		File saveFile = new File("output.csv");
		PrintWriter out = new PrintWriter(saveFile);
		String header = " ,";
		
		for (int i = 0; i < fileEnd+1 - fileBegin; i++) 
		{
			int fileNum = fileBegin+i;
			header += fileNum + ",";
		}
		out.println(header);
		
		String line = "";
		for(String word: toFind)
		{
			line = "";
			line += word + ",";
			for (WordCounter wc : wordCounters) 
				line += wc.getFreq(word) + ",";
			out.println(line);
		}	

		out.close();
		
				
		scan.close();
	}
	
	
	public static void main(String[] args) throws InterruptedException, FileNotFoundException 
	{
		FindTrends.CreateTrends();
	}
}
