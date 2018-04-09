package project7;

import java.util.ArrayList;
import java.util.Comparator;

public class HashMap<K,V> implements MapSet<K,V> 
{
	private Object[] table;
	private int collisions;
	
	@SuppressWarnings("unchecked")
	public HashMap() //100 default size
	{
		collisions = 0;
		table = new Object[100];
		Comparator<String> comp = new StringAscending();
		for (int i = 0; i < table.length; i++) 
		{
			table[i] = new BSTMap<K,V>((Comparator<K>) comp);
		}
	}
	
	@SuppressWarnings("unchecked")
	public HashMap(int initSize) //Custom initial size
	{
		collisions = 0;
		table = new Object[initSize];
		Comparator<String> comp = new StringAscending();
		for (int i = 0; i < table.length; i++) 
		{
			table[i] = new BSTMap<K,V>((Comparator<K>) comp);
		}
	}

	@SuppressWarnings("unchecked")
	@Override
	public V put(K key, V value) //May change this!
	{
		int index = key.hashCode() % table.length; //generating index
		BSTMap<K,V> map = (BSTMap<K,V>) table[index];
		V toReturn = map.get(key);
		if(map.size() > 0) //Incrementing collisions if there is something at the spot already
			collisions++;
		
		map.put(key, value);
		
		return toReturn;
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
		int index = key.hashCode() % table.length; //generating index
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
		map.put("Aa", 5);
		map.put("BB", 6);
		map.put("Aa", 8);
		
		System.out.println(map);
		System.out.println(map.get("Aa"));
		System.out.println(map.values());
		
		System.out.println("Collisions: " + map.collisions);
		
		
	}
	
	
}

