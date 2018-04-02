package project6;
/*
 * BSTMap.java for doing all that fun Map stuff, in BinarySearchTree ways!
 * Owen Goldthwaite
 * April 2nd, 2017
 */

import java.util.ArrayList;
import java.util.Comparator;

public class BSTMap<K,V> implements MapSet<K,V>
{
	private TNode<K,V> root;
	private Comparator<K> comp;
	private int size; //Implement size if put returns null
	
	public BSTMap(Comparator<K> comp)
	{
		this.comp = comp;
		root = null;
		size = 0;
	}
	
	public V put(K key, V value)
	{
		if(this.root == null)
			root = new TNode<K,V>(key, value, null, null);
		else
		{
			V toReturn = root.put(key, value, comp); //Just did this so size increments properly
			if(toReturn == null)
				size++;
			return toReturn;
		
		}
		size++;
		return null;	
	}
	
	public V get(K key) 
	{
		if(this.root == null)
			return null;
		else
			return root.get(key, comp); //should return null if not found
		
		//return null;
	}

	
	@Override
	public boolean containsKey(K key) 
	{
		if(root.get(key, comp) != null)
			return true;
		else
			return false;
	}

	@Override
	public ArrayList<K> keySet() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public ArrayList<V> values() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public ArrayList<KeyValuePair<K, V>> entrySet() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public int size() {
		return size;
	}

	@Override
	public void clear() {
		// TODO Auto-generated method stub
		
	}
	
	public static void main( String[] argv ) 
	{
		// create a BSTMap
		BSTMap<String, Integer> bst = new BSTMap<String, Integer>( new StringAscending() );

		bst.put( "twenty", 20 );
		bst.put( "ten", 10 );
		bst.put( "eleven", 11 );
		bst.put( "five", 5 );
		bst.put( "six", 6 );
		bst.put( "seven", 7 );

		System.out.println(bst.put( "twenty", 25 ));
		
		System.out.println( bst.get( "eleven" ) );
		
		bst.put("eleven", 326);
		System.out.println( bst.get( "eleven" ) );
		System.out.println( bst.get( "twenty" ) );
		System.out.println( bst.containsKey("twenty"));
		System.out.println(bst.size());

		// put more test code here
	}
	
}




