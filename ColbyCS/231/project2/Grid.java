package project2;
/*
* Grid.java
* Owen Goldthwaite
* 02/19/18
*/
import java.util.*;

public class Grid
{
	public static void main(String[] args) 
	{
		int yogi = Integer.parseInt(args[0]);
		int booboo = Integer.parseInt(args[1]);
		Random rand = new Random();

		for (String s : args) 
		{
			System.out.println(s);
		}

		System.out.println(yogi + " rows!");
		System.out.println(booboo + " cols!");

		String[][] ranger = new String[yogi][booboo];

		for (int i = 0; i < ranger.length; i++ ) 
		{
			System.out.println();
			for (int j = 0; j < ranger[0].length ;j++ ) 
			{
				String thing = Character.toString((char) (rand.nextInt(26) + 65));
				ranger[i][j] = thing;
				System.out.print(ranger[i][j] +" ");
			}
		}
		System.out.println();


	}



}
