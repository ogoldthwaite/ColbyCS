
/*
 * Owen Goldthwaite
 * HashMap, it's like a map but it likes to smoke hash
 */

import java.util.ArrayList;
import java.util.Comparator;

public class HashMap<K,V> implements MapSet<K,V> 
{
	private Object[] table;
	private int collisions;
	private int tableSize;
	
	public HashMap() //100 default size
	{
		collisions = 0;
		table = new Object[100];
		tableSize = 0;
		initTable();
	}
	
	public HashMap(int initSize) //Custom initial size
	{
		collisions = 0;
		table = new Object[initSize];
		tableSize = 0;
		initTable();
	}
	
	@SuppressWarnings("unchecked")
	private void initTable() //Just fills every table spot with an empty BSTMap
	{
		Comparator<String> comp = new StringAscending();
		for (int i = 0; i < table.length; i++) 
		{
			table[i] = new BSTMap<K,V>((Comparator<K>) comp);
		}
	}
	
	private int getIndex(K key) //returns index of key inside array
	{
		return Math.abs(key.hashCode()) % table.length;
	}
	

	@SuppressWarnings("unchecked")
	@Override
	public V put(K key, V value) //May change this!
	{
		tableSize++;
		int index = getIndex(key); //generating index
		BSTMap<K,V> map = (BSTMap<K,V>) table[index];
		V toReturn = map.get(key);
		
		if(map.size() > 0) //Incrementing collisions if there is something at the spot already
		{
			collisions++;
			tableSize--; //decreasing table size by one because it's incremented at beginning of code, silly way to do this but W/E
		}
		map.put(key, value);
		
		if(tableSize > table.length/2) //enlarge if over half array slots are filled
		{
			tableSize = 0;
			enlarge();
		}
		return toReturn;
	}

	@SuppressWarnings("unchecked")
	private void enlarge() //double array table size
	{
		Object[] oldMap = table;
		table = new Object[oldMap.length*2];
		initTable();
		
		for (int i = 0; i < oldMap.length; i++) 
		{
			BSTMap<K, V> map = (BSTMap<K, V>)oldMap[i];
			ArrayList<KeyValuePair<K, V>> sets = map.entrySet();
			
			if(sets != null)
			{
				for(KeyValuePair<K, V> entry : sets)	
				{
					if (entry != null) 
						put(entry.getKey(), entry.getValue());
				}
			}
		}
	}
	
	
	@Override
	public boolean containsKey(K key) 
	{
		if(this.get(key) != null)
			return true;
		else
			return false;
	}

	@SuppressWarnings("unchecked")
	@Override
	public V get(K key) //May change this!
	{
		int index = getIndex(key); //generating index
		
		BSTMap<K,V> map = (BSTMap<K,V>) table[index];
		V toReturn = map.get(key);
		
		return toReturn;
	}

	@Override
	public ArrayList<K> keySet() 
	{
		ArrayList<K> keys = new ArrayList<K>();
		for (KeyValuePair<K,V> entry : this.entrySet()) 
		{
			keys.add(entry.getKey());
		}
		
		return keys;
	}

	@Override
	public ArrayList<V> values() //Pretty inefficient
	{
		ArrayList<V> values = new ArrayList<V>();
		for (KeyValuePair<K,V> entry : this.entrySet()) 
		{
			values.add(entry.getValue());
		}
		
		return values;
	}

	@SuppressWarnings("unchecked")
	@Override
	public ArrayList<KeyValuePair<K, V>> entrySet() 
	{
		ArrayList<KeyValuePair<K, V>> list = new ArrayList<KeyValuePair<K, V>>();
		for (int i = 0; i < table.length; i++) 
		{
			BSTMap<K,V> map = (BSTMap<K,V>) table[i];
			
			if(map.size() > 0) //making sure map isn't empty/null
				list.addAll(map.entrySet());
		}
		return list;
	}

	@SuppressWarnings("unchecked")
	@Override
	public int size() 
	{
		int size = 0;
		for (int i = 0; i < table.length; i++) 
		{
			BSTMap<K,V> map = (BSTMap<K,V>) table[i];
			size += map.size();
		}
		return size;
	}

	@Override
	public void clear() 
	{
		// TODO Auto-generated method stub
		
	}
	
	public int getEfficiency() //returns collisions
	{
		return this.collisions;
	}
	
	@SuppressWarnings("unchecked")
	public String toString()
	{
		String toReturn = "";
		for (int i = 0; i < table.length; i++) 
		{
			BSTMap<K,V> map = (BSTMap<K,V>) table[i];
			
			if(map.size() != 0)
				toReturn += map.entrySet() + "\n";
		}
		
		return toReturn;
	}
	
	public static void main(String[] args) 
	{
		HashMap<String, Integer> map = new HashMap<String, Integer>(10);
		
		map.put("a", 1);
		map.put("b", 2);
		map.put("c", 1);
		map.put("d", 1);
		map.put("e", 1);
		map.put("f", 2);
		map.put("g", 1);
		map.put("h", 1);
		map.put("i", 1);
		map.put("j", 2);
		map.put("k", 1);
		map.put("l", 1);
		map.put("Aa", 5);
		map.put("BB", 6);
		map.put("Aa", 8);
		
		System.out.println(map);
		System.out.println(map.get("Aa"));
		System.out.println(map.values());
		
		System.out.println(map.containsKey("z"));
		System.out.println("Collisions: " + map.collisions);
		
		
	}
	
	
}

