package project8;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

/*FindCommondWords.java finds common words.java
 * Owen Goldthwaite
 * April 22, 2018
 */

public class FindCommonWords 
{
	private PQHeap<KeyValuePair<String, Integer>> heap;
	private MapSet<String, Integer> map;
	private int wordCount;
	
	public FindCommonWords()
	{
		heap = new PQHeap<KeyValuePair<String, Integer>>(new ValueComparator()); //Sorts by values of KV pairs
		map = new HashMap<String, Integer>(); // Hashmap for getting specific words for FindTrends, probably a better way of doing this
		wordCount = 0;
	}
	
	public void readWordCountFile(String fileName) //Only really use when map is empty, reads a word count file into this map
	{
		try
		{
			FileReader file = new FileReader(fileName);
			BufferedReader buff = new BufferedReader(file);
			
			String line1 = buff.readLine();
			
			String[] firstLine = line1.split(":");
						
			wordCount = Integer.parseInt(firstLine[1]);
			
			while(true)
			{
				String line = buff.readLine();
				
				if(line == null)
					break;

				String[] words = line.split(" ");				
				String word = words[0].trim().toLowerCase(); //Assuming that each line will only ever have 2 things
					
				Integer val = new Integer(words[1]);
				KeyValuePair<String, Integer> entry = new KeyValuePair<String, Integer>(word, val);
					
				map.put(word, val);
				heap.add(entry);
			}

			buff.close();
		}
		catch(FileNotFoundException ex) 
		{	
      		System.out.println("WordCounter.analyze():: unable to open file " + fileName );
    	}
    	catch(IOException ex) 
    	{
      		System.out.println("WordCounter.analyze():: error reading file " + fileName);
    	}
	}
	
	public PQHeap<KeyValuePair<String, Integer>> getHeap()
	{
		return this.heap;
	}
	
	public MapSet<String, Integer> getMap()
	{
		return this.map;
	}
	
	public int getTotalWords()
	{
		return this.wordCount;
	}

	
	public static void main(String[] args) 
	{
		FindCommonWords test = new FindCommonWords();
		
		test.readWordCountFile("wordCount2015.txt");
		
		System.out.println(test.getHeap().otherFirst(10));
	}
	
	
}
