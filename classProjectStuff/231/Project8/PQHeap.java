

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.Random;

/*
 * PGHeap.java for storing a priority queue
 * Owen Goldthwaite
 * April 22nd, 2018
 */

public class PQHeap<T> //Currently a max heap
{
	private Object[] heap;
	private Comparator<T> comp;
	private int size;
	
	public PQHeap(Comparator<T> comp)
	{
		this.comp = comp;
		heap = new Object[10];
		size = 0;
	}
	
	private void enlarge() //double array heap size
	{
		Object[] oldHeap = heap;
		heap = new Object[oldHeap.length*2];
		
		for (int i = 0; i < oldHeap.length; i++) 
		{
			heap[i] = oldHeap[i];
			//maybe set oldHeap entry to null
		}
	}
	
	private int getParentIndex(int currentIndex) //returns parent index of the given node
	{
		return (currentIndex - 1) / 2;
	}
	
	private int getChildIndex(int currentIndex, boolean left) //returns child index of node, set left = to true for left child
	{
		return 2 * currentIndex + (left ? 1:2);
	}
	
	public void add(T val)
	{
		heap[size] = val; //adding at open spot
		size++;
		fixHeapUp();
		
		if(size > heap.length / 2)
			enlarge();
		
	}
	
	@SuppressWarnings("unchecked")
	private void fixHeapUp() //swaps the node to the proper spot in the heap
	{
		
		int index = size - 1; //node that was just added
		
		while( index > 0)
		{
			int parentIndex = getParentIndex(index);
			int compResult = comp.compare((T)heap[index], (T)heap[parentIndex]);
			
			if(compResult > 0)
			{
				Object tempVal = heap[index];
				heap[index] = heap[parentIndex];
				heap[parentIndex] = tempVal;

				index = parentIndex;
			}
			else
				break;
		}	
	}
	
	@SuppressWarnings("unchecked")
	public T remove()
	{		
		 if (size == 0) 
			 return null;

		 Object toReturn = heap[0];
		 heap[0] = heap[--size];
		 fixHeapDown();
		 
		 return (T)toReturn;
	}
	
	@SuppressWarnings("unchecked")
	private void fixHeapDown() //fixes the heap for remove
	{
		int node = 0;
		int leftC = getChildIndex(node, true);
		int rightC = getChildIndex(node, false);
		int smallerC = leftC;

		 while (leftC <= size-1) 
		 {
			 // if there are two children and left is larger than right
			 if (leftC < size-1 && comp.compare((T)heap[leftC], (T)heap[rightC]) < 0) 
				 smallerC = rightC;
			 
			 // if the node is larger than the smaller one, swap
			 if (comp.compare((T)heap[node], (T)heap[smallerC]) < 0)
			 {
				 Object tempVal = heap[node];
				 heap[node] = heap[smallerC];
				 heap[smallerC] = tempVal;
			 }
			 else 
				 break;
	
			 node = smallerC;
			 leftC = getChildIndex(node, true);
			 rightC = getChildIndex(node, false);
			 smallerC = leftC;
		 }
	}
	
	public int size()
	{
		return this.size;
	}
	
	public String toString () 
	{
		 String s = "";
		 int level = 0;
		 int leftn = size;
		 
		 while (leftn > 0) 
		 {
			 int count = 1;
			 int pow = (int)Math.pow(2, level);
			 
			 while (count <= pow) 
			 {
				 if (leftn == 0) 
					 break;
				 
				 s += heap[size-leftn] + " ";
				 count++;
				 leftn--;
			 }
			 
			 if (leftn != 0) 
				 s += "\n";
			 
			 level++;
		 }
		 return s;
	}
	
	public String first(int n) //returns a string only containing the first n objects in the heap
	{
		long time = System.currentTimeMillis();
		
		String s = "";
		
		if(n > heap.length)
			n = heap.length;
		
		for (int i = 0; i < n; i++) 
		{
			s += heap[i] + " \n";
		}
		
		time = System.currentTimeMillis() - time;	
		System.out.println("Time Taken for Normal Find First: " + time);
		
		return s;
	}
	
	@SuppressWarnings("unchecked")
	public String otherFirst(int n)
	{
		long time = System.currentTimeMillis();
		
		ArrayList<KeyValuePair<String, Integer>> list = new ArrayList<KeyValuePair<String, Integer>>();
		HashSet<Integer> checked = new HashSet<Integer>();
		Random rand = new Random();
		
		for (int i = 0; i < heap.length; i++) 
		{
			int index = rand.nextInt(heap.length);
			
			if(checked.contains(index))
				i--;
			else
			{
				checked.add(index);
				
				if(heap[index] != null)
					list.add((KeyValuePair<String, Integer>) heap[index]);
				
			}		
		}
		
//		for(int i = 0; i < list.size(); i++)
//		{
//			for (int j = 0 ; j < list.size()-1; j++) 
//			{			
//				if(list.get(j).getValue() < list.get(j+1).getValue())
//				{
//					KeyValuePair<String, Integer> temp = list.get(j+1);
//					list.set(j+1, list.get(j));
//					list.set(j, temp);
//				}
//						
//			}
//		}
		list.sort(new ValueComparator());
		
		String s = "";
		
		if(n > heap.length)
			n = heap.length;
		
		for (int i = list.size()-1; i > list.size()-1 - n; i--) 
		{
			s += list.get(i) + " \n";
		}
		
		 time = System.currentTimeMillis() - time;	
		 System.out.println("Time Taken for Silly Find First: " + time);
		
		return s;
		
	}

	public static void main(String[] args) 
	{
		PQHeap<Integer> test = new PQHeap<Integer>(new IntegerComparator());
		test.add(4);
		test.add(5);
		test.add(5);
		test.add(5);
		test.add(5);
		test.add(2);
		test.add(5);
		test.add(1);
		test.remove();
		test.remove();
		test.add(0);
		test.add(3);
		test.add(2);
		
		System.out.println(test);
		
		
	}
	
	
	
}
