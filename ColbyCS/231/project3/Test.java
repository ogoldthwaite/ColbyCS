package project3;

import java.util.Comparator;
import java.util.Random;
/*
* Test.java for testing heapsort
* Owen Goldthwaite
* 3/4/18
*/
public class Test
{
	public static void main(String[] args)
	{
		testSortCell();
	}
	
    public static void testSortCell()
    {
        Cell[] a = new Cell[10];
     
        Random rand = new Random();
        for(int i = 0; i < a.length; i++)
            a[i] = new Cell(0,0,0, rand.nextInt(8)+1);
        
        Comparator<Cell> c = new CellComparator();
        
        System.out.print("a[]: ");
        for(int i = 0; i < a.length; i++)
            System.out.println(a[i] + " ");
        System.out.println();
        
        System.out.println("Running Heap Sort");
        HeapSort.sort(a, c);
        
        System.out.println("a[]: Final Sorted Array");
        for(int i = 0; i < a.length; i++)
            System.out.println(a[i] + " ");
        System.out.println();
        System.out.println();
    }
}
