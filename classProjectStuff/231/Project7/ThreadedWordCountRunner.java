
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class ThreadedWordCountRunner 
{
	private static boolean useHashTable;
	private static WordCounter wc;
	
	public static void main(String[] args) throws IOException, InterruptedException
	 {
		Scanner scan = new Scanner(System.in);
		
		System.out.println("Do you want to use a HashMap for this or not? Enter 1 for yes, 0 for no.");
		int choice1 = Integer.parseInt(scan.nextLine());
		
		if(choice1 == 1)
			useHashTable = true;
		else
			useHashTable = false;
		
		 wc = new WordCounter(useHashTable);
		
		System.out.println("Enter 0 for normal single run or 1 for middle three of five analyze run! ");
		int choice = Integer.parseInt(scan.nextLine());
		
		if(choice == 0)
			SingleExec();
		else
			MultipleExec();
	 
		scan.close();
	 }
	
	
	public static void MultipleExec() throws IOException, InterruptedException
	{
		//User Input
		Scanner scan = new Scanner(System.in); 
		System.out.println("Enter the input file name: ");		
		String inputFile = scan.nextLine();
		
		ArrayList<Long> times = new ArrayList<Long>();
		
		for(int i = 0; i < 5; i++)
		{
			wc.resetMap(useHashTable); //resetting the map each time!
			
			//Getting current time
			long time = System.currentTimeMillis();
			//Getting names of all files
			ArrayList<String> fileNames = FileSplit.splitFile(new File(inputFile));
		
			ArrayList<Thread> threads = new ArrayList<Thread>();
			
		    //Making and starting all the threads
			for (int k=0; k < fileNames.size(); k++)
		     {
		         Thread t = new Thread(new WordCountThread(k, fileNames.get(k)));
		         threads.add(t);
		         t.start();
		     }
		     
			 //Waiting for all the threads to finish
		     for (Thread t : threads) //Joining every thread so nothing executes until all threads are done
				t.join();
		     
		     //Adding up all the word count files!
		     for (int j = 0; j < fileNames.size(); j++) 
				wc.appendWordCountFile(fileNames.get(j)+"_result_"+j);
		     
		     time = System.currentTimeMillis() - time;	
			 System.out.println("Analyse Time Taken for Analyze " + i +": " + time);
		     times.add(time);
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
			     
	     scan.close();
	}
	
	public static void SingleExec() throws IOException, InterruptedException
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
		for (int i=0; i < fileNames.size(); i++)
	     {
	         Thread t = new Thread(new WordCountThread(i, fileNames.get(i)));
	         threads.add(t);
	         t.start();
	     }
	     
		 //Waiting for all the threads to finish
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
