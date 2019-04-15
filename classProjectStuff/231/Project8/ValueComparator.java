
import java.util.Comparator;

/*Comparator for comparing the values of two KV pairs
 * Owen Goldthwaite
 */

public class ValueComparator implements Comparator<KeyValuePair<String, Integer>>
{
	@Override
	public int compare(KeyValuePair<String, Integer> o1, KeyValuePair<String, Integer> o2) //May change boolean statement around a bit. Who knows!
	{
		
		float diff = o1.getValue() - o2.getValue();
	     
	     if(diff == 0.0)
	    	 return 0;
	     else
	    	 return (diff < 0.0 ? -1 : 1);
	}

	
}
