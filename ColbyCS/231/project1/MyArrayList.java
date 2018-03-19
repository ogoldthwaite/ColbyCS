package project1;

import java.util.Iterator;

/**
 * File: MyArrayList.java
 * Author: Owen Goldthwaite
 * Date: 02/18/2018
 */

//import java.util.ArrayList;
//import java.util.Arrays;

public class MyArrayList<E> implements Iterable<E> //Not making it iterable, Iterable method incomplete
{
	private Object[] a;
	private int size;
	

	public MyArrayList()
	{
	    a = new Object[10];
		size = 0;
	}

	public MyArrayList(int initialCapacity)
	{
		if (initialCapacity < 0)
			throw new IllegalArgumentException();
		a = new Object[initialCapacity];
		size = 0;
	}
	
	public MyArrayList(MyArrayList<E> list)
	{
		size = 0;
		a = new Object[list.size()];
		for(int i = 0; i < list.size(); i++)
		{
			this.add( list.get(i) );
			size++;
		}
		
	}
	
	public void clear()
	{
		Object[] temp = new Object[10];
		a = temp;
	}

	public int size()
	{
		return size;	
	}

    @SuppressWarnings("unchecked")
	public E get(int index)
	{
		if (index < 0 || index >= size)
			throw new IndexOutOfBoundsException();
        return (E) a[index];
	}

	@SuppressWarnings("unchecked")
	public E set(int index, E element)
	{	
		if (index < 0 || index >= size)
			throw new IndexOutOfBoundsException();
		
		Object temp = a[index];
		a[index]=element;
		
		return (E) temp;
	}

	public boolean contains(Object elem)
	{
		for(int i = 0; i< size;i++)
		{
			if (a[i].equals(elem) && !(elem.equals(null)))
				return true;
		}
		return false;
	}

	public void trimToSize()
	{
		if(size < a.length)
		{
			Object[] temparray = new Object[size];
			for(int i = 0; i < temparray.length; i++)
				temparray[i]=a[i];
		a = temparray;
		}
		
	}

	public void add(E elem)
	{
		add(size, elem);
		this.trimToSize();
	}

	public void add(int index, E element)
	{
		if (index < 0 || index > size)
			throw new IndexOutOfBoundsException();
		if (size >= a.length || a.length == 0)
		{
			Object[] temparray = new Object[a.length*2+1];
			for(int i = 0; i <a.length; i++)
				temparray[i]=a[i];
			 a=temparray; 
 		}
		for (int i = size; i > index; i--)
		{			
			a[i] = a[i-1];
		}
		a[index] = element;
		size++;
		
		
	}
	
	@SuppressWarnings("unchecked")
	public E remove(int index)
	{
		if (index < 0 || index > size)
			throw new IndexOutOfBoundsException();
		Object temp;
		for (int i = index; i <= size-1; i++)
		{
			a[i]= a[i-1];
		}
		temp = a[size-1];
		a[size - 1] = null;
		size--;
		
		return (E) temp;
	}

	public boolean remove(Object elem)
	{
		for(int i = 0; i<a.length; i++)
		{
			if(a[i].equals(elem) && !(a[i].equals(null)))
			{
				remove(i);
				return true;
			}
		}
		return false;	
	}
	
	public String toString()
	{
		String toReturn = "[";
		for (int i = 0; i < a.length; i++) 
			toReturn += a[i]+",";		
		return toReturn +"]";
	}
	
	@Override
	public Iterator<E> iterator() {
		return null;
	}
	
}
