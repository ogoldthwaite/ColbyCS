

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.util.Random;

public class GameMessage extends Agent
{
	private String message;
	
	public GameMessage(String msg)
	{
		this.message = msg;
	}
	
	public void draw(Graphics g)
	{		
		Random rand = new Random();
		g.setColor(new Color(rand.nextInt(255), rand.nextInt(255), rand.nextInt(255)));
		g.setFont(new Font("TimesRoman", Font.PLAIN, 36)); 
		g.drawString(message, 0, 50);
	
	}
}
