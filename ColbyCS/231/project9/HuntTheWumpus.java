package project9;
/*
 * HuntTheWumpus.java
 * Owen Goldthwaite
 * 5/6/2018
 */

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Random;
import java.util.Scanner;

enum GameState {Play, Quit};

public class HuntTheWumpus
{
	private Landscape scape;
	private LandscapeDisplay display;
	private Graph graph;
	private Hunter hunter;
	private Wumpus wumpus;
	private int scale;
	private GameState state;
	
	public HuntTheWumpus()
	{
		Scanner scan = new Scanner(System.in);
		System.out.println("Enter Board Size, i.e. 8 for 8x8 game. 5 for 5x5 game. etc");
		System.out.println("Input: ");
		scale = scan.nextInt();
		
		scape = new Landscape(scale * 100, scale * 100 + 60);
		display = new LandscapeDisplay(scape);
		graph = new Graph();
		hunter = new Hunter();
		wumpus = new Wumpus();
		state = GameState.Play;
		Control control = new Control();
		display.addKeyListener(control);	
		
		initGame();
		
		scan.close();
		
	}
	
	public void initGame() //Initializes the game!
	{
		scape.addAgent(hunter);
		scape.addAgent(wumpus);
		
		initVerts();
		
		ArrayList<Vertex> vertList = graph.getVertList();
		
		//Spawning the wumpus and hunter at random different locations
		Random rand = new Random();
		int hspawn = rand.nextInt(vertList.size());
		int wspawn = rand.nextInt(vertList.size());
		
		while(hspawn == wspawn)
		{
			hspawn = rand.nextInt(vertList.size());
			wspawn = rand.nextInt(vertList.size());
		}
		
		hunter.updateCurrentVertex(vertList.get(hspawn)); 
		wumpus.updateCurrentVertex(vertList.get(wspawn));
		
		for (Vertex vertex : vertList) 
		{
			scape.addForeAgent(vertex);
		}
		
		//Making shortest path vals from wumpus
		graph.shortestPath(vertList.get(wspawn));
		
		HashSet<Integer> traps = new HashSet<Integer>();
		
		for(int i = 0; i < scale/2 + 1; i++)
		{
			int loc = rand.nextInt(vertList.size());
			
			while(loc == hspawn || loc == wspawn || traps.contains(loc) || vertList.get(loc).getCost() <= 2)
				loc = rand.nextInt(vertList.size());
			
			traps.add(rand.nextInt(vertList.size()));
			vertList.get(loc).setTrapped(true);
		
		}
	}
	
	private void initVerts() //Initializes the vertices of the graph
	{		
		ArrayList<ArrayList<Vertex>> rows = new ArrayList<ArrayList<Vertex>>();
		
		for (int i = 0; i < scale; i++) 
		{
			rows.add(new ArrayList<Vertex>());
		}
			
		Vertex prevVert;
		int n = 0;
		int yOffset = 60;
		
		for (int y = 0; y < scale * 100; y+=100) 
		{
			prevVert = new Vertex(0, y + yOffset); //first vertex in row
			
			for (int x = 100; x < scale * 100; x+=100) 
			{
				Vertex v = new Vertex(x,y+yOffset);
				graph.addEdge(prevVert, v, Direction.East);
				
				if(!rows.get(n).contains(prevVert))
					rows.get(n).add(prevVert);
				
				rows.get(n).add(v);
				prevVert = v;
			}
			n++;
		}
		
		for (int i = 0; i < rows.size() - 1; i++) 
		{
			for (int j = 0; j < rows.get(i).size(); j++) 
			{
				graph.addEdge(rows.get(i).get(j), rows.get(i+1).get(j), Direction.South);
			}
		}
		
	}
	
	private void checkWumpEndGame(Vertex toCheck) throws InterruptedException //checks the vertex for the wumpus and gives win/lost conditions based upon conditions
	{
		if(wumpus.getVert() == toCheck)
		{
			if(hunter.isArmed())
			{
				//Win Condition
				System.out.println("You won!");
				wumpus.setState(-1);
				scape.addAgent(new GameMessage("You wumped that wumpus! Nice!"));
				state = GameState.Quit;
			}
			else
			{
				//Lose Condition
				System.out.println("You died!");
				wumpus.setState(1);
				scape.addAgent(new GameMessage("Damn, you just got wumped good! RIP"));
				state = GameState.Quit;
			}	
		}
		else if(hunter.isArmed())
		{
			wumpus.updateCurrentVertex(hunter.getVert());
			wumpus.setState(1);
			System.out.println("The Wumpus heard your failed attack and came to eat you!");
			scape.addAgent(new GameMessage("You missed, get wumped on!"));
			state = GameState.Quit;
		}
		else if(toCheck.isTrapped())
		{
			Random rand = new Random();
			hunter.updateCurrentVertex(graph.getVertList().get(rand.nextInt(graph.getVertList().size())));
		}
		
	}
	
	
    private class Control extends KeyAdapter implements ActionListener 
    {

        public void keyTyped(KeyEvent e)
        {
            boolean armed = hunter.isArmed();
        	
        	System.out.println( "Key Pressed: " + e.getKeyChar() );
            
            if( ("" + e.getKeyChar()).equalsIgnoreCase("w") ) 
            {
            	Vertex toGo = hunter.getVert().getNeighbor(Direction.North);
            	if(toGo != null)
            	{
            		toGo.setVisible(true);
          		
            		hunter.setArmed(armed);
            		
            		if(!hunter.isArmed())
            		{
            			hunter.updateCurrentVertex(toGo);        			
            		}
            		
            		try {
						checkWumpEndGame(toGo);
					} catch (InterruptedException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
            	}
            }
        
            if( ("" + e.getKeyChar()).equalsIgnoreCase("a") ) 
            {
            	Vertex toGo = hunter.getVert().getNeighbor(Direction.West);
            	if(toGo != null)
            	{
            		toGo.setVisible(true);
              		
            		hunter.setArmed(armed);
            		
            		if(!hunter.isArmed())
            		{
            			hunter.updateCurrentVertex(toGo);        			
            		}
            		
            		try {
						checkWumpEndGame(toGo);
					} catch (InterruptedException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
            	}
            }
           
            if( ("" + e.getKeyChar()).equalsIgnoreCase("s") ) 
            {
            	Vertex toGo = hunter.getVert().getNeighbor(Direction.South);
            	if(toGo != null)
            	{
            		toGo.setVisible(true);
              		
            		hunter.setArmed(armed);
            		
            		if(!hunter.isArmed())
            		{
            			hunter.updateCurrentVertex(toGo);        			
            		}
            		
            		try {
						checkWumpEndGame(toGo);
					} catch (InterruptedException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
            	}
            }
            
            if( ("" + e.getKeyChar()).equalsIgnoreCase("d") ) 
            {
            	Vertex toGo = hunter.getVert().getNeighbor(Direction.East);
            	if(toGo != null)
            	{
            		toGo.setVisible(true);
              		
            		hunter.setArmed(armed);
            		
            		if(!hunter.isArmed())
            		{
            			hunter.updateCurrentVertex(toGo);        			
            		}
            		
            		try {
						checkWumpEndGame(toGo);
					} catch (InterruptedException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
            	}
            }
            
            if( ("" + e.getKeyChar()).equalsIgnoreCase(" ") ) 
            {
            	hunter.setArmed(!hunter.isArmed());
            }
            
            if( ("" + e.getKeyChar()).equalsIgnoreCase("q") ) 
            {
            	state = GameState.Quit;
            }
            
            if( ("" + e.getKeyChar()).equalsIgnoreCase("r") ) 
            {
            	//restart
            }
            
        
        }

        public void actionPerformed(ActionEvent event) {
            if( event.getActionCommand().equalsIgnoreCase("Color") ) {
                // change the color of the ball
                Random gen = new Random();
            }
            else if( event.getActionCommand().equalsIgnoreCase("Quit") ) {
            }
        }

    }
    
    public static void main(String[] args) throws InterruptedException 
    {	
    	runGame();
	}
    
    private static void runGame() throws InterruptedException
    {
    	HuntTheWumpus game = new HuntTheWumpus();
		while(game.state == GameState.Play)
		{
			game.display.repaint();
			Thread.sleep(33);
		}
		for (int i = 0; i < 10; i++) 
		{
			game.display.repaint();
			Thread.sleep(300);
		}
		
		game.display.dispose();
    }
}
    

