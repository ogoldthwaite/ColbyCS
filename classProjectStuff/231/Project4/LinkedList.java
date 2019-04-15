
/*
*LinkedList.java
* Owen Goldthwaite
* 3/5/18
*/
import java.util.*;

public class LinkedList<T> implements Iterable<T>
{
	private class Node
	{
		private Node next;
		private T value;

		public Node()
		{
			this.next = null;
			this.value = null;
		}

		public Node(T val)
		{
			this.value = val;
			next = null;
		}
		
		public Node(Node next)
		{
			this.next = next;
			this.value = null;
		}

		public T getVal()
		{
			return this.value;
		}

		public void setNext(Node n)
		{
			this.next = n;
		}

		public Node getNext()
		{
			return this.next;
		}
		
		public void setVal(T val)
		{
			this.value = val;
		}
	}

	private class LLIterator implements Iterator<T>
	{
		private Node n;

		public LLIterator(Node head)
		{
			this.n = head.getNext(); //Starting on first thing after head
		}

		public boolean hasNext()
		{
			return (n != null);
		}

		public T next() 
		{
			if(n == null) 
				return null;
			
			T val = n.getVal();
			n = n.getNext();
			return val;
		}

		public void remove()
		{
			//Does nothing
		}
	}

	private Node head;
	private int size;

	public LinkedList()
	{
		this.size = 0;
		this.head = new Node();
	}

	public void clear()
	{
		this.head.setNext(null);
		this.size = 0;
	}

	public int size()
	{
		return this.size;
	}

	public boolean isEmpty()
	{
		return this.head.getNext() == null;
	}
	
    private Node getNode(int index) //returns the node at the given index to help other methods
    {
    	 if(index < 0)
    		 return head;
    	 Node tempNode = head;
         for(int i = 0; i <= index; i++)
         	tempNode=tempNode.next;	 
    	 
         return tempNode;
    }
    
	public void addFirst(T item)
	{			
			this.add(0, item);
	}
	
	public void addLast(T item)
	{
		this.add(size, item);
	}

	//RECURSIVE ADD LAST, Extension?
	 public void addLast(T item, boolean recur) //method that you call, recursive addLast
	 {
	 	this.addLast(item, this.head);
	 	size++;
	 }

	 private Node addLast(T item, Node node) //recursive addLast helper method
	 {
	 	if(node == null)
	 		node = new Node(item);
	 	else
	 		node.setNext(this.addLast(item, node.getNext()));

	 	return node;
	 }
	 
	 public void add(int index, T item)
	 {
	    if(index < 0 || index > size)
	        throw new IndexOutOfBoundsException();
	    
	    Node addNode = new Node(item);
	    addNode.setNext(this.getNode(index));
	    getNode(index - 1).setNext(addNode); 	
			
		this.size++;
	 }

	 public T remove(int index)
	 {
		 if(index < 0 || index > size)
		     throw new IndexOutOfBoundsException();
		 
		 Node tempNode = this.getNode(index - 1);
		 Node toRemove = this.getNode(index);
		 T val = toRemove.getVal();
		 tempNode.setNext(toRemove.getNext());
		 toRemove.setNext(null);
		 this.size--;
		 
		 return val;
	 }
	 
	 public ArrayList<T> toArrayList()
	 {
		 ArrayList<T> toReturn = new ArrayList<T>();
		 for (T val : this) 
			toReturn.add(val);
		 return toReturn;	
	 }
	 
	 public ArrayList<T> toShuffledList()
	 {
		 ArrayList<T> toReturn = this.toArrayList();
		 Collections.shuffle(toReturn);
		 return toReturn;
	 }
	 
	public Iterator<T> iterator()
	{
		return new LLIterator(this.head);
	}


	public static void main(String[] args) 
	{
		LinkedList<Integer> list = new LinkedList<Integer>();
		
		list.addFirst(5);
		list.addFirst(10);
		list.addFirst(20);

		System.out.printf("\nAfter setup %d\n", list.size());
		for(Integer item: list) {
			System.out.printf("thing %d\n", item);
		}


	}


}