

import java.util.ArrayList;
import java.util.PriorityQueue;

/* Owen Goldthwaite
 * Graph.java, it's a graph dude
 * April 30, 2018
 */


public class Graph 
{
	private ArrayList<Vertex> verts;
	
	public Graph()
	{
		verts = new ArrayList<Vertex>();
	}
	
	public int vertexCount()
	{
		return verts.size();
	}
	
	public void addEdge(Vertex v1, Vertex v2, Direction dir) //creates an edge between the two vertexes, v2 is in dir of v1
	{
		if(!verts.contains(v1))
			verts.add(v1);
		if(!verts.contains(v2))
			verts.add(v2);
		
		//Connecting those vertices!
		v1.connect(v2, dir);
		v2.connect(v1, Vertex.opposite(dir));	
	}
	
	public void shortestPath(Vertex v0)
	{
		PriorityQueue<Vertex> queue = new PriorityQueue<Vertex>();
		
		v0.setCost(0);
		queue.add(v0);
		
		while(!queue.isEmpty())
		{
			Vertex v = queue.poll();
			v.setMarked(true);
			for (Vertex w : v.getNeighbors()) 
			{
				if( (!w.isMarked()) && (v.getCost()+1 < w.getCost()) )//Changes in cost are +1 because no move is more than one
				{
					w.setCost(v.getCost() + 1); 
					queue.remove(w); //removing just to make sure there arent any duplicates
					queue.add(w);
				}
			}
		}
		
	}
	
	public ArrayList<Vertex> getVertList()
	{
		return this.verts;
	}
	
	public void printVertices() //Just for testing
	{
		System.out.println(verts.size());
		System.out.println(verts);
	}
	
	public static void main(String[] args) 
	{
		Graph g = new Graph();
		Vertex v1 = new Vertex();
		Vertex v2 = new Vertex();
		Vertex v3 = new Vertex();
		Vertex v4 = new Vertex();
		Vertex v5 = new Vertex();
		Vertex v6 = new Vertex();
		Vertex v7 = new Vertex();
		Vertex v8 = new Vertex();
		
		g.addEdge(v1, v2, Direction.North);
		g.addEdge(v2, v3, Direction.West);
		g.addEdge(v1, v4, Direction.South);
		g.addEdge(v4, v5, Direction.East);
		g.addEdge(v5, v6, Direction.East);
		g.addEdge(v3, v7, Direction.South);
		g.addEdge(v1, v7, Direction.West);
		g.addEdge(v1, v8, Direction.East);
		g.addEdge(v5, v8, Direction.North);
		
		System.out.println(g.verts);
		g.shortestPath(v1);
		System.out.println(g.verts);
	}
	
}
