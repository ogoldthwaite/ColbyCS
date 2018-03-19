package project3;

import java.util.Comparator;
/*
* HeapSort.java for suduko extension thing
* Owen Goldthwaite
* 3/2/18
*/
public class HeapSort //I looked at the wikipedia article for heapsort, if I forget to include that in my writeup. Which I may!
{
	private static int heapSize = 0;
	
	public static <T> void sort(T[] a, Comparator<T> c) //heap sort!
	{
		//c.compare(element1, element2); How you compare stuff!
		for(int i = 1; i < a.length; i++)
		{
			int pIndex = getParentIndex(i);
			int k = i;
			
		while(pIndex >= 0 && c.compare(a[k], a[pIndex]) > 0)
		{
			if (c.compare(a[k], a[pIndex]) > 0)
			{
				swap(a, k, pIndex);
				k = pIndex;
				pIndex = getParentIndex(k); //change this k I think
			}
		}
			heapSize++;
		}
		
		heapSize = a.length;
		
		for(int j = heapSize - 1; j >= 0; j--)
		{
			//System.out.println(a[0] +" preswap");
			swap(a, 0, j);
			//System.out.println(a[0]+ " postswap");
			fixHeap(a, c, 0);
			heapSize--;
		}
		
		//System.out.println(heapSize);
		//System.out.println(a);
		
		
	}
	
	private static void swap(Object[] x, int i, int j)
	{
		Object temp = x[i];
		x[i] = x[j];
		x[j] = temp;
	}

	 protected final static int getParentIndex(int childIndex)
	    {
	        return (childIndex + 1) / 2 - 1;
	    }
	    
	 protected final static int getChildIndex(int parentIndex, boolean left) 
	    {
	        return 2 * parentIndex + (left ? 1 : 2);
	    }

	 private static <T> void fixHeap(T[]a, Comparator<T> c, int nodeIndex) //fixes the heap so it is properly sorted into a min/max heap. 
		{
			int leftChildIndex = getChildIndex(nodeIndex, true);
			int rightChildIndex = getChildIndex(nodeIndex, false);

			
			if(heapSize - 1  != 0)
			{
				T max = a[nodeIndex];
				int minIndex = nodeIndex;
				
				if(leftChildIndex < heapSize - 1)
				{
					fixHeap(a, c, leftChildIndex);
					if(c.compare(a[leftChildIndex], max) > 0)
					{
						max = a[leftChildIndex];
						minIndex = leftChildIndex;
					}
				}

				if(rightChildIndex < heapSize - 1)
				{
					fixHeap(a, c, rightChildIndex);
					if(c.compare(a[rightChildIndex], max) > 0)
					{
						max = a[rightChildIndex];
						minIndex = rightChildIndex;
					}

				}	
					if(minIndex != nodeIndex)
					{	
						a[minIndex] = a[nodeIndex];
						a[nodeIndex] = max;
						//elements.set(minIndex, elements.get(nodeIndex));
						//elements.set(nodeIndex, min);
					} 
			} 	
		}

}
