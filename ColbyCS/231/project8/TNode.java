package project8;
import java.util.Comparator;


/*
 * TNode.java A node of the Mappy tree!
 * Owen Goldthwaite
 * April 2nd, 2017
 */

public class TNode <K,V>
{
	public TNode<K, V> left;
	public TNode<K, V> right;
	public KeyValuePair<K,V> entry;
	
	public TNode(K key, V value)
	{
		entry = new KeyValuePair<K, V>(key, value);
		this.left = null;
		this.right = null;
	}
	
	public TNode(K key, V value, TNode<K, V> left, TNode<K, V> right)
	{
		entry = new KeyValuePair<K, V>(key, value);
		this.left = left;
		this.right = right;
	}
	
	public V put(K key, V value, Comparator<K> comp) //Does the put work! Recursively finds the place to put
	{
		int toCompare = comp.compare(key, this.entry.getKey());
		
		if (toCompare == 0)
		 {
			 V toReturn = this.entry.getValue(); //Returning previous value at this point
			 this.entry.setValue(value);
			 return toReturn;
		 }
		 else if (toCompare < 0) 
		 {
			 if (left == null) 
				 left = new TNode<K, V> (key, value, null, null);
			 else 
				 left.put(key, value, comp);
		 }
		 else 
		 {
			 if (right == null)
				 right = new TNode<K, V> (key, value, null, null);
			 else 
				 right.put(key, value, comp);
		 }
		
		return null;
		 
	}
	
	public V get(K key, Comparator<K> comp) //Does the get work! Recursively finds the node to get!
	{
		 int toCompare = comp.compare(key, this.entry.getKey());

		 if (toCompare == 0) 
			 return this.entry.getValue();
		 else if (toCompare < 0) 
		 {
			 if (left == null) 
				 return null;
			 else return left.get(key, comp);
		 }
		 else
		 {
			if (right == null) 
				return null;
			else
				return right.get(key, comp);
		 }
		 
	}
	
    public void preOrder(TNode<K,V> node, String stuff) //Just prints preorder, here for me
    {
    	//stuff += node.entry.getValue() +" ";
    	
    	System.out.println(node.entry.getKey() + ": " + node.entry.getValue());
    	
    	if(node.left != null)
    		preOrder(node.left, stuff);
    	
    	if(node.right != null)
    		preOrder(node.right, stuff);
    }
    
	public String toString()
	{
		return "(" + entry.getKey() + ", " + entry.getValue() + ")";
	}
	
}
