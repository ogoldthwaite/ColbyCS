package project1;
/**
 * File: Shuffle.java
 * Author: Owen Goldthwaite
 * Date: 02/12/2018
 */

import java.util.ArrayList;
import java.util.Random;	

public class Shuffle 
{

	public static void main ( String[] args )
	{
		ArrayList<Integer> list = new ArrayList<Integer>();
		ArrayList<Integer> toRandList = new ArrayList<Integer>();

		Random rand = new Random();

		for (int i = 0; i < 10; i++) 
		{
			//list.add(rand.nextInt(99));
			list.add(i);
			toRandList.add(i);
			System.out.println(list.get(i));
		}

		System.out.println(randomOrder(toRandList));
			
		for (int i = 0; i < 10; i++) 
		{
			System.out.println(list.remove(rand.nextInt(list.size())) + " was removed from the list!");
			System.out.println(list + " remain in the list");
			System.out.println("-------");
		}

		//System.out.println(randomOrder(list));
	
	}

	public static ArrayList<Integer> randomOrder(ArrayList<Integer> coolList)
	{
		/* Randomizes the ArrayList list by randomly removing elements from it and adding them
		to a new ArrayList. Only works for Integers right now
		*/
		ArrayList<Integer> toReturn = new ArrayList<Integer>();
		Random rand = new Random();
		int x = coolList.size();

		for (int i = 0; i < x; i++) 
			toReturn.add(coolList.remove(rand.nextInt(coolList.size())));

		return toReturn;


	}
}
