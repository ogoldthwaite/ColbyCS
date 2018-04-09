package project7;


/*
 * KeyValuePair.java for storing a map entry of data
 * Owen Goldthwaite
 * April 8nd, 2017
 */


public class KeyValuePair<K,V> 
{
	private K key;
	private V value;
	
	public KeyValuePair(K key, V value)
	{
		this.key = key;
		this.value = value;
	}
	
	public K getKey()
	{
		return this.key;
	}
	
	public V getValue()
	{
		return this.value;
	}
	
	public void setValue(V newVal)
	{
		this.value = newVal;
	}
	
	public String toString()
	{
		return "" + this.key + " " + this.value + "";
	}
	
	
}

