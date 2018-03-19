package project3;

import java.util.Comparator;
/*
* CellComparator.java for suduko so heapsort can work
* Owen Goldthwaite
* 3/2/18
*/
public class CellComparator implements Comparator<Cell>
{
	@Override
	public int compare(Cell c1, Cell c2) //Compares cells based on the number of possible solutions it has
	{
		if(c1.getNumSols() == c2.getNumSols())
			return 0;
		else
			return (c1.getNumSols() < c2.getNumSols() ? -1 : 1);
	}

}
