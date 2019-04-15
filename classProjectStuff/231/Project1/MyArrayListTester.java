
/**
 * File: MyArrayListTest.java
 * Author: Owen Goldthwaite
 * Date: 02/12/2018
 */
public class MyArrayListTest {

	public static void main(String[] args) 
	{
		MyArrayList<Integer> list =  new MyArrayList<Integer>();
		list.add(1);
		list.add(2);
		list.add(3);
		System.out.println(list);
		System.out.println(list.get(1));
		list.set(1, 5);
		System.out.println(list);
		list.add(8);
		System.out.println(list);
		System.out.println(list.contains(5));
		System.out.println(list.contains(4));
		System.out.println(list.remove(1));
	}

}
