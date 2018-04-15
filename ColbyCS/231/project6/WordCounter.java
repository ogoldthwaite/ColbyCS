package project6;
/*
 * BSTMap.java Does the stuff using a BSTMap!
 * Owen Goldthwaite
 * April 2nd, 2017
 */

import java.io.*;
import java.util.ArrayList;
import java.util.Comparator;

public class WordCounter<K,V> 
{
	private BSTMap<K,V> map;
	private int wordCount;
	
	@SuppressWarnings("unchecked")
	public WordCounter()
	{
		Comparator<String> comp = new StringAscending(); 
		map = new BSTMap<K,V>((Comparator<K>) comp); 
		wordCount = 0;
		
	}
	
	@SuppressWarnings("unchecked")
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
						if(map.containsKey((K)word)) //Check all this casting stuff! May want to change this contains key
							map.put( (K)word, (V) new Integer((int)map.get((K) word) + 1));
						else
							map.put( (K)word, (V) new Integer(1));
					
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
	
	@SuppressWarnings("unchecked")
	public int getCount(String word)
	{
		return (int) map.get((K) word);
	}
	
	public double getFreq(String word) //returns a words freq
	{
		return (float)this.getCount(word)/wordCount;
	}
	
	public BSTMap<K, V> getMap()
	{
		return this.map;
	}
	
	public void writeWordCountFile(String fileName) throws FileNotFoundException //writes and creates a word count file
	{
		File saveFile = new File(fileName);
		PrintWriter out = new PrintWriter(saveFile);
		ArrayList<KeyValuePair<K, V>> list = map.entrySet();

		out.println("totalWordCount:" + this.wordCount);
		for (KeyValuePair<K, V> keyValuePair : list) 
			out.println(keyValuePair);		

		out.close();
	}
	
	@SuppressWarnings("unchecked")
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
					
				map.put((K)word, (V)val);
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
	
	@SuppressWarnings("unchecked")
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
				
				if(map.containsKey((K)key))
				{
					Integer newVal = new Integer( (int)map.get((K)key) + val);
					map.put((K)key, (V)newVal);
				}
				else
					map.put((K)key, (V)val);
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
	
	public static void main(String[] args) throws FileNotFoundException 
	{
		WordCounter<String, Integer> wc = new WordCounter<String, Integer>();
		//wc.analyze("counttest.txt");
		wc.readWordCountFile("counts_ct.txt");
		
		System.out.println(wc.getMap().entrySet());
		
		wc.writeWordCountFile("counts_ct_v2.txt");
		
	}
	
	
}
	
	
	
	

