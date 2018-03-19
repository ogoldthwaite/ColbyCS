package project5;
/*
*LinkedList.java
* Owen Goldthwaite
* 3/5/18
*/
import java.util.*;

public class DoublyLinkedList<T> implements Iterable<T>
{
	private class Node
	{
		private Node next;
		private Node prev;
		private T value;

		public Node()
		{
			this.next = null;
			this.prev = null;
			this.value = null;
		}

		public Node(T val)
		{
			this.value = val;
			next = null;
		}
		
		@SuppressWarnings("unused")
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
		
		public void setPrev(Node n)
		{
			this.prev = n;
		}
		
		public Node getPrev()
		{
			return this.prev;
		}
		
		@SuppressWarnings("unused")
		public void setVal(T val)
		{
			this.value = val;
		}
	}

	private class LLIterator implements Iterator<T>
	{
		private Node n;
		private boolean backwards;

		public LLIterator(Node start) //Will go backwards if you start on tail, foward if you start on head
		{
			if(start == tail)
			{
				this.n = start.getPrev(); //Starting on first thing after tail
				backwards = true;
			}
			else
			{
				this.n = start.getNext();
				backwards = false;
			}
		}

		public boolean hasNext()
		{
			return (n != null);
		}

		@SuppressWarnings("unchecked")
		public T next() 
		{
			if(n == null) 
				return null;
			
			T val = n.getVal();
			
			if(backwards)
				n = n.getPrev();
			else
				n = n.getNext();
			
			if(val == null) //When going backwards reaches head and returns a null value for some reason
				return (T) new Integer(-1);
			
			return val;
		}

		public void remove()
		{
			//Does nothing
		}
	}

	private Node head;
	private Node tail;
	private int size;

	public DoublyLinkedList()
	{
		this.size = 0;
		this.head = new Node();
		this.tail = new Node();
	}

	public void clear()
	{
		this.head.setNext(null);
		this.tail.setPrev(null);
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
    
    public T getVal(int index) //returns the value of node at given index
    {
    	return this.getNode(index).getVal();
    }
    
	public void addFirst(T item)
	{			
			this.add(0, item);
	}
	
    public void addLast(T item)
	{
		this.add(size, item);
	}
	 
	public void add(int index, T item)
	{
	    if(index < 0 || index > size)
	        throw new IndexOutOfBoundsException();
	    
	    Node prevNode = getNode(index - 1);
	    Node nextNode = getNode(index);
	    
	    Node addNode = new Node(item);
	        
	    addNode.setNext(nextNode);
	    prevNode.setNext(addNode);
	    addNode.setPrev(prevNode);
	    if(size != 0 && index != size)
	    	nextNode.setPrev(addNode);
	    else
	    	tail.setPrev(addNode);

			
		this.size++;
	 }

	 public T remove(int index)
	 {
		 if(index < 0 || index > size)
		     throw new IndexOutOfBoundsException();
		 
		 Node tempNode = this.getNode(index - 1);
		 Node nextNode = this.getNode(index + 1);
		 Node toRemove = this.getNode(index);
		 T val = toRemove.getVal();
		 
		 tempNode.setNext(nextNode);
		 if(nextNode != null)
		    nextNode.setPrev(tempNode);
		 else
			 tail.setPrev(tempNode);
		 toRemove.setNext(null);
		 toRemove.setPrev(null);
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
		DoublyLinkedList<Integer> list = new DoublyLinkedList<Integer>();
		
		list.addLast(5);
		list.addLast(10);
		list.addLast(20);
		list.add(1, 25);

		System.out.printf("\nAfter setup %d\n", list.size());
		for(Integer item: list) {
			System.out.printf("thing %d\n", item);
		}
		


	}


}