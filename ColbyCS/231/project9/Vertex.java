package project9;
/* Owen Goldthwaite
 * Vertex.java, it's a vertex dude
 * April 30, 2018
 */

import java.util.Collection;
import java.util.HashMap;

enum Direction {North, East, South, West};

public class Vertex implements Comparable<Vertex>
{	
	private HashMap<Direction, Vertex> edges;
	private int cost;
	private boolean marked;
	
	public Vertex()
	{
		edges = new HashMap<Direction, Vertex>();
		cost = Integer.MAX_VALUE;
		marked = false;
	}
	
	public boolean isMarked()
	{
		return marked;
	}
	
	public int getCost()
	{
		return cost;
	}
	
	public void setCost(int newCost)
	{
		this.cost = newCost;
	}
	
	public void setMarked(boolean newMark)
	{
		this.marked = newMark;
	}
	
	public void connect(Vertex other, Direction dir) //Connects other vertex to this one
	{
		edges.put(dir, other); //Adds vertex other to this ones edge list, currently only does it one direction
	}
	
	public Vertex getNeighbor(Direction dir) //returns neighbor in given direction or null
	{
		return edges.get(dir);
	}
	
	public Collection<Vertex> getNeighbors()
	{
		//ArrayList<Vertex> neighbors = (ArrayList<Vertex>) edges.values();
		return edges.values();
	}
	
	public static Direction opposite(Direction dir) //returns the opposite direction of dir
	{
		if( dir == Direction.North )
			return Direction.South;
		else if ( dir == Direction.South )
			return Direction.North;
		else if ( dir == Direction.East )
			return Direction.West;
		else if ( dir == Direction.West )
			return Direction.East;
		else 
			return null;
	}
	
	public String toString()
	{
		String toReturn = "";
		toReturn += "Neighbors: " + edges.size() + "\n";
		toReturn +=  "Marked: " + marked + "\n";
		toReturn += "Cost: " + cost + "\n";	
		return toReturn;
	}
	
	@Override
	public int compareTo(Vertex o) 
	{
		if(this.cost == o.getCost())
			return 0;
		else
			return (this.cost > o.getCost() ? 1 : -1); //May want to swap the greater than sign
	}
	
	public static void main(String[] args) 
	{
		Vertex v1 = new Vertex();
		Vertex v2 = new Vertex();
		
		v1.connect(v2, Direction.North);
		System.out.println(v1.getNeighbor(Direction.North));
		System.out.println(v1.getNeighbor(Direction.South));
		System.out.println(v1);
		System.out.println(v2);
		v1.setCost(1);
		v2.setCost(2);
		v1.setMarked(true);
		System.out.println(v1);
		System.out.println(v2);
		System.out.println(Vertex.opposite(Direction.South));
		
	}
	
}
