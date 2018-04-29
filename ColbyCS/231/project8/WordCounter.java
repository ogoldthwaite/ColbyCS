package project8;
/*
 * BSTMap.java Does the stuff using a BSTMap!
 * Owen Goldthwaite
 * April 2nd, 2017
 */

import java.io.*;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.concurrent.ConcurrentHashMap;

public class WordCounter implements Runnable
{
	private MapSet<String, Integer> map;
	public static ConcurrentHashMap<String, Integer> coolMap = new ConcurrentHashMap<String, Integer>();
	private int wordCount;
	private String fileString;
	
	public WordCounter(boolean useHashTable)
	{
		Comparator<String> comp = new StringAscending(); 
		
		if(useHashTable)
			map = new HashMap<String, Integer>(100); //10 initial size, could change
		else
			map = new BSTMap<String, Integer>((Comparator<String>) comp); 
		
		fileString = "";
		wordCount = 0;
		
	}
	
	public WordCounter(String fileString, boolean useHashTable)
	{
		Comparator<String> comp = new StringAscending(); 
		
		if(useHashTable)
			map = new HashMap<String, Integer>(100); //10 initial size, could change
		else
			map = new BSTMap<String, Integer>((Comparator<String>) comp); 
		
		this.fileString = fileString;
		wordCount = 0;
		
	}
	
	public void resetMap(boolean useHashTable) //just resets the map for multiple analyzes in on execution of program
	{
		Comparator<String> comp = new StringAscending(); 
		if(useHashTable)
			map = new HashMap<String, Integer>(100); //10 initial size, could change
		else
			map = new BSTMap<String, Integer>((Comparator<String>) comp); 
	}
	
	public boolean analyze(String filename) //reads in a text file and adds each word to the map with it's number of occurences
	{
		try
		{
			FileReader file = new FileReader(filename);
			BufferedReader buff = new BufferedReader(file);

			while(true)
			{
				String line = buff.readLine();
				
				if(line == null)
					break;

				String[] words = line.split("[^a-zA-Z0-9']");
				
				for (int i = 0; i < words.length; i++) //Updating map done here too
				{
					String word = words[i].trim().toLowerCase();
					
					if(word.length() > 0)
					{
						Integer getResult = map.get(word);
						
						if(getResult != null) //Check all this casting stuff! May want to change this contains key
							map.put( word,  new Integer(getResult + 1));
						else
							map.put( word,  new Integer(1));
					
					wordCount++;
					}
						
				}
			}

			buff.close();
			return true;
		}
		catch(FileNotFoundException ex) 
		{	
      		System.out.println("WordCounter.analyze():: unable to open file " + filename );
    	}
    	catch(IOException ex) 
    	{
      		System.out.println("WordCounter.analyze():: error reading file " + filename);
    	}

    	return false;
    } 
	
	public int getWordCount()
	{
		return this.wordCount;
	}
	
	public int getCount(String word)
	{
		Integer toReturn = (Integer)map.get(word);
		if(toReturn == null)
			return 0;
		else 
			return toReturn;
		
	}
	
	public double getFreq(String word) //returns a words freq
	{
		return (double)this.getCount(word)/wordCount;
	}
	
	public MapSet<String, Integer> getMap()
	{
		return this.map;
	}
	
	public void writeWordCountFile(String fileName) throws FileNotFoundException //writes and creates a word count file
	{
		File saveFile = new File(fileName);
		PrintWriter out = new PrintWriter(saveFile);
		ArrayList<KeyValuePair<String, Integer>> list = map.entrySet();

		out.println("totalWordCount:" + this.wordCount);
		for (KeyValuePair<String, Integer> keyValuePair : list) 
			out.println(keyValuePair);		

		out.close();
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
					
				map.put(word, val);
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
	
	public void appendWordCountFile(String fileName) throws FileNotFoundException //appends a word count file to the map of this instance
	{
		try
		{
			FileReader file = new FileReader(fileName);
			BufferedReader buff = new BufferedReader(file);
			
			String line1 = buff.readLine();
			
			String[] firstLine = line1.split(":");
						
			wordCount += Integer.parseInt(firstLine[1]);
			
			while(true)
			{
				String line = buff.readLine();
				
				if(line == null)
					break;

				String[] words = line.split(" ");				
				String key = words[0].trim().toLowerCase(); //Assuming that each line will only ever have 2 things
					
				Integer val = new Integer(words[1]);
				
				Integer getResult = map.get(key);
				
				if(getResult != null) //could change to contains key
				{
					Integer newVal = new Integer( getResult + val);
					map.put(key, newVal);
				}
				else
					map.put(key, val);
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
	
	public void appendMap(MapSet<String, Integer> m) //appends a map to this map
	{
		ArrayList<KeyValuePair<String, Integer>> list = m.entrySet();
		
		for (KeyValuePair<String, Integer> entry : list) 
		{
			String key = entry.getKey();
			Integer val = entry.getValue();
			Integer getResult = coolMap.get(key);
			
			wordCount += val;
			
			if(getResult != null) //could change to contains key
			{
				Integer newVal = new Integer( getResult + val);
				coolMap.put(key, newVal);
			}
			else
				coolMap.put(key, val);
		}
					
	}
		
	
	public static void main(String[] args) throws FileNotFoundException 
	{
		WordCounter wc = new WordCounter(true);
		//wc.analyze("counttest.txt");
		wc.analyze("counttest.txt");
		
		System.out.println(wc.getMap().entrySet());
		
		wc.writeWordCountFile("hey.txt");
		
	}

	@Override
	public void run() 
	{
		try
        {
            analyze(fileString);
        }
        catch (Exception e)
        {
            System.out.println ("Exception caught!");
        }
		
	}
	
	
}
	
	
	
	

