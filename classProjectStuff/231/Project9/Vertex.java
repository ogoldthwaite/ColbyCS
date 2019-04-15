
/* Owen Goldthwaite
 * Vertex.java, it's a vertex dude
 * April 30, 2018
 */

import java.awt.Color;
import java.awt.Graphics;
import java.util.Collection;
import java.util.HashMap;

enum Direction {North, East, South, West};

public class Vertex extends Agent implements Comparable<Vertex>
{	
	private HashMap<Direction, Vertex> edges;
	private int cost;
	private boolean marked;
	private boolean visible;
	private boolean trapped;
	
	public Vertex(double xpos, double ypos)
	{
		super(xpos, ypos);
		edges = new HashMap<Direction, Vertex>();
		cost = Integer.MAX_VALUE;
		marked = false;
		visible  = false;
		trapped = false;
	}
	
	public Vertex()
	{
		super();
		edges = new HashMap<Direction, Vertex>();
		cost = Integer.MAX_VALUE;
		marked = false;
		visible = false;
		trapped = false;
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
	
	public void setVisible(boolean newVis)
	{
		this.visible = newVis;
	}
	
	public void setTrapped(boolean newTrap)
	{
		this.trapped = newTrap;
	}
	
	public boolean isTrapped()
	{
		return trapped;
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
	
	public void draw(Graphics g)
	{
		this.draw(g, 0, 0, 100);
	}
	
	public void draw(Graphics g, int x0, int y0, int scale)
	{

		
		if (!this.visible) return;
		
		int x = (int) (x0 + this.xPos);
		int y = (int) (y0 + this.yPos);
		int border = 2;
		int half = scale / 2;
		int eighth = scale / 8;
		int sixteenth = scale / 16;
		
		//g.drawRect(x + border, y + border, scale - 2*border, scale - 2 * border);
		
		// draw rectangle for the walls of the cave
		if (this.cost <= 2)
			g.setColor(Color.red);
		else if(trapped)
			g.setColor(new Color(198,5,198));
		else
			g.setColor(Color.black);
			
		g.drawRect(x + border, y + border, scale - 2*border, scale - 2 * border);
		
		// draw doorways as boxes
		g.setColor(Color.black);
		if (this.edges.containsKey(Direction.North))
			g.fillRect(x + half - sixteenth, y, eighth, eighth + sixteenth);
		if (this.edges.containsKey(Direction.South))
			g.fillRect(x + half - sixteenth, y + scale - (eighth + sixteenth), 
				  eighth, eighth + sixteenth);
		if (this.edges.containsKey(Direction.West))
			g.fillRect(x, y + half - sixteenth, eighth + sixteenth, eighth);
		if (this.edges.containsKey(Direction.East))
			g.fillRect(x + scale - (eighth + sixteenth), y + half - sixteenth, 
				  eighth + sixteenth, eighth);
	}
	
	
	public String toString()
	{
		String toReturn = "";
		toReturn += "Neighbors: " + edges.size() + "\n";
		//toReturn +=  "Marked: " + marked + "\n";
		//toReturn += "Cost: " + cost + "\n";	
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
