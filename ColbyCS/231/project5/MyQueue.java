package project5;
/*
 * MyQueue.java
 * Owen Goldthwaite
 * 3/18/2018
 */
import java.util.Iterator;


public class MyQueue<T> implements Iterable<T>
{
	private DoublyLinkedList<T> queue;
	
	public MyQueue()
	{
		this.queue = new DoublyLinkedList<T>();
	}
	
	public int size()
	{
		return queue.size();
	}
	
	public boolean offer(T item) //Currently Doesn't take null
	{
		if(item == null)
			throw new IllegalArgumentException();
		
		queue.addLast(item);
		return true;
	}
	
	public T poll()
	{
		if(queue.size() == 0)
			return null;
		else
			return queue.remove(0);
	}
	
	public T peek()
	{
		return queue.getVal(0);
	}

	@Override
	public Iterator<T> iterator() 
	{
		return queue.iterator();
	}
	
	public static void main(String[] args) 
	{
		MyQueue<Integer> queue = new MyQueue<Integer>();
		queue.offer(1);
		queue.offer(2);
		queue.offer(3);
		System.out.println(queue.poll());
		System.out.println(queue.poll());
		queue.offer(4);
		System.out.println("peek!" + queue.peek());
		
		for(Integer item : queue)
			System.out.println("thing " + item);			
	}

}