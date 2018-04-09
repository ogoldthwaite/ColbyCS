package project7;

import java.util.Comparator;

public class StringAscending implements Comparator<String>
{
	@Override
	public int compare(String a, String b) 
	{	
		return a.compareTo(b);
	}
	
}