
/*
 * BSTMap.java for doing all that fun Map stuff, in BinarySearchTree ways!
 * Owen Goldthwaite
 * April 2nd, 2017
 */

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;



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
	
	public V put(K key, V value) //puts a value into the map
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
		size++; //should only really run when very first node is added
		return null;	
	}
	
	public V get(K key) //gets value with key from the map
	{
		if(this.root == null)
			return null;
		else
			return root.get(key, comp); //should return null if not found
		
		//return null;
	}

	public boolean containsKey(K key) //returns true if key is in map, false otherwise
	{
		if(root == null)
			return false;
		
		if(root.get(key, comp) != null)
			return true;
		else
			return false;
	}
		
    public String preOrder() //Just prints out in preorder
    {
    	String stuff = "";
    	root.preOrder(root, stuff);
    	return stuff;
    }
    
    public ArrayList<KeyValuePair<K, V>> entrySet() //saves to arraylist in preorder and returns it
    {
    	ArrayList<KeyValuePair<K,V>> toReturn = new ArrayList<KeyValuePair<K,V>>();
    	entrySet(root, toReturn);
    	return toReturn;
    	
    }
    
    private void entrySet(TNode<K, V> node, ArrayList<KeyValuePair<K,V>> list) //entryset recursive helper
    {
    	list.add(node.entry);
    	
    	if(node.left != null)
    		entrySet(node.left, list);
    	
    	if(node.right != null)
    		entrySet(node.right, list);	
    }
    
	public void saveToFile(String fileName) throws FileNotFoundException //Writes this tree to the given file, here mainly for me/testing
	{
		File saveFile = new File(fileName);
		PrintWriter out = new PrintWriter(saveFile);
		ArrayList<KeyValuePair<K, V>> list = this.entrySet();

		for (KeyValuePair<K, V> keyValuePair : list) 
			out.println(keyValuePair);		

		out.close();
	}
	
	public List<TNode<K,V>> levelOrder(boolean printNulls) //Level order print, if printNulls is true it will print null values in tree as well
	{
    	List<TNode<K,V>> nodes = new LinkedList<TNode<K,V>>();
    	Queue<TNode<K,V>> nodeQ = new LinkedList<TNode<K,V>>();
    	TNode<K,V> tempNode = new TNode<K,V>(null,null);

    	nodeQ.offer(this.root);

    	while(nodeQ.size() != 0)
    	{
    		tempNode = nodeQ.poll();

    		if(printNulls)
    		{
    			if(tempNode == null)
    				nodes.add(null);
    			else
    			{
    				nodes.add(tempNode);
    				nodeQ.offer(tempNode.left);
    				nodeQ.offer(tempNode.right);
    			}
    		}
    		else
    		{
    			if(tempNode != null)
    			{
	    			nodes.add(tempNode);
	    			if(tempNode.left != null)
	    				nodeQ.offer(tempNode.left);
	    			if(tempNode.left != null)
	    				nodeQ.offer(tempNode.right);
    			}

    		}
    	}
    	return nodes;       	    
    }
	
	@SuppressWarnings("unchecked")
	public boolean remove(String key) //remove method that you call!
	{
		boolean isPresent = this.containsKey((K)key);
		root = remove(root, (K)key);
		return isPresent;
	}

	private TNode<K,V> remove(TNode<K,V> node, K key) //private recursive remove helper method
	{
		if(node == null)
			return null;
		
		int compResult = comp.compare(key, node.entry.getKey());

		//finding location of node, then setting node.left/right back up the recursive stack so it has the proper value
		if(compResult < 0)
			node.left = remove(node.left, key);
		else if(compResult > 0)
			node.right = remove(node.right, key);
		else //Stuff for one/no children
		{
			if(node.left == null)
			{
				if(node.right != null)
				{
					return node.right;
				}
				else
					return null;
					
			}
			else if(node.right == null) //left node cannot be null here, so return left
			{
				return node.left;
			}
			else //Two Children
			{
				TNode<K,V> swapNode = node.right;
				KeyValuePair<K,V> storeVal = new KeyValuePair<K,V>(node.entry.getKey(), node.entry.getValue());
				
				//finds leftmost node on the right subtree
				while(swapNode.left != null)
				{
					swapNode = swapNode.left;
				}
				
				//swaps the values of the two nodes
				node.entry = swapNode.entry; 
				swapNode.entry = storeVal;		
				
				//goes and removes the node with key again, which will hopefully now be a leaf
				node.right = remove(node.right, key);
			}
			
		}
		//if nothing else is returned
		return node;
	}
	
	
	
	public ArrayList<K> keySet() {
		// TODO Auto-generated method stub
		return null;
	}

	public ArrayList<V> values() {
		// TODO Auto-generated method stub
		return null;
	}

	public int size() {
		return this.entrySet().size();
	}

	public void clear() {
		// TODO Auto-generated method stub
		
	}
	
	public static void main( String[] argv ) 
	{
		// create a BSTMap
		BSTMap<String, Integer> bst = new BSTMap<String, Integer>( new StringAscending() );

		bst.put( "d", 8);
		bst.put( "b", 10 );
		bst.put( "a", 11 );
		bst.put( "c", 5 );
		bst.put( "f", 6 );
		bst.put( "e", 7 );
		bst.put("j", 15);

		System.out.println(bst.levelOrder(false));
		
		bst.remove("c");
		
		System.out.println(bst.levelOrder(false));
		
		bst.remove("f");
		
		System.out.println(bst.levelOrder(false));
		
	}
	
}




