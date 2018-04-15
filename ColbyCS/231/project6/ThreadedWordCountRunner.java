package project6;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class ThreadedWordCountRunner 
{
	private static WordCounter<String, Integer> wc = new WordCounter<String, Integer>();
	
	public static void main(String[] args) throws IOException, InterruptedException
	 {
		//User Input
		Scanner scan = new Scanner(System.in); 
		System.out.println("Enter the input file name: ");		
		String inputFile = scan.nextLine();
		System.out.println("Enter the output file name: ");
		String outputFile = scan.nextLine();
		
		//Getting current time
		long time = System.currentTimeMillis();
		//Getting names of all files
		ArrayList<String> fileNames = FileSplit.splitFile(new File(inputFile));
	
		ArrayList<Thread> threads = new ArrayList<Thread>();
		
	    //Making and starting all the threads
		System.out.println("Generating Threads...");
		for (int i=0; i < fileNames.size(); i++)
	     {
	         Thread t = new Thread(new WordCountThread(i, fileNames.get(i)));
	         threads.add(t);
	         t.start();
	     }
	     
		 //Waiting for all the threads to finish
		 System.out.println("Waiting for Threads to finish...");
	     for (Thread t : threads) //Joining every thread so nothing executes until all threads are done
			t.join();
		 
	     //Adding up all the word count files!
	     for (int i = 0; i < fileNames.size(); i++) 
			wc.appendWordCountFile(fileNames.get(i)+"_result_"+i);
	     	
	     //Writing word count file
	     wc.writeWordCountFile(outputFile);
	     
		 System.out.println("Unique Word Count: " + wc.getMap().size());
	     time = System.currentTimeMillis() - time;	
		 System.out.println("Time Taken: " + time);
	     
	     scan.close();
	 
	 }
}
