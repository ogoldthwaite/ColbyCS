package project7;

public class WordCountThread implements Runnable //Each instance of this class is a thread analyzing a section of text
{
	private int id; //id of this thread used for debugging/ some other stuff
	private String fileName; //name of file that this thread is analyzing
	private WordCounter wc; //wordcounter instance for this specific thread
	
	public WordCountThread(int id, String fileName)
	{
		this.id = id;
		this.fileName = fileName;
		wc = new WordCounter(true);
	}
	
	@Override
	public void run() //Required run method, calls analyze for given file part and then writes a word count file for it
	{
        try
        {
            wc.analyze(fileName);
            wc.writeWordCountFile(fileName+"_result_"+id);
        }
        catch (Exception e)
        {
            System.out.println ("Exception caught!");
        }
		
	}

}
