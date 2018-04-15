package project6;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

class FileSplit {
    
	public static ArrayList<String> splitFile(File f) throws IOException //Splits a file into 4MB segments and returns a string array list containing the names of those file segments
    {
        int partCounter = 1; //increments with each file segment, helps differentiate between files
        
        ArrayList<String> toReturn = new ArrayList<String>();

        int fileSize = 4096 * 4096; //max size of file size, currently set at 4MB/4096 KB
        byte[] buffer = new byte[fileSize];

        String fileName = f.getName();

        //try-with-resources to ensure closing stream
        try (FileInputStream fis = new FileInputStream(f);
             BufferedInputStream bis = new BufferedInputStream(fis)) 
        {

            int bytesAmount = 0;
            while ((bytesAmount = bis.read(buffer)) > 0) 
            {
                
            	//write each chunk of data into separate file with different number in name
                String filePartName = String.format("%s.%03d", fileName, partCounter++);
                //Adding file name to the array list of names
                toReturn.add(filePartName); 
                
                //Making the new file!
                File newFile = new File(f.getParent(), filePartName);
                try (FileOutputStream out = new FileOutputStream(newFile)) 
                {
                    out.write(buffer, 0, bytesAmount);
                }
            }
        }
        
        return toReturn;
    }

    public static void main(String[] args) throws IOException 
    {
        splitFile(new File("reddit_comments_2008_copy.txt"));
    }
}