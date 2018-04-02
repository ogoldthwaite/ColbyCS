package project6;
/*
 * BSTMap.java Does the stuff using a BSTMap!
 * Owen Goldthwaite
 * April 2nd, 2017
 */

import java.io.*;
import java.util.Comparator;

public class WordCounter<K,V> 
{
	private BSTMap<K,V> map;
	private int wordCount;
	
	@SuppressWarnings("unchecked")
	public WordCounter()
	{
		Comparator<String> comp = new StringAscending(); //May wanna check out this
		map = new BSTMap<K,V>((Comparator<K>) comp); //May wanna check out this
		wordCount = 0;
		
	}
	
	@SuppressWarnings("unchecked")
	public boolean analyze(String filename)
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
					
					Integer stuff = new Integer((int)map.get((K) word) + 1);
					
					if(map.containsKey((K) word)) //Check all this casting stuff!
						map.put( (K)word, (V) stuff);
					else
						map.put( (K)word, (V) new Integer(1));
					
					
						
					wordCount++;	
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
		
}
	
	
	
	

