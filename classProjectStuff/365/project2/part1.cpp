
#include <opencv2/opencv.hpp>
#include <cstdio>
#include <cstdlib>
#include <dirent.h>
#include <cstring>

int calculateDif(cv::Mat mainImg, cv::Mat img);

int main(int argc, char *argv[]) {
	char dirname[256];
	DIR *dirp;
	struct dirent *dp;

	cv::Mat baseimg;
	char filename[256];

	// usage statement
	if(argc < 3) {
		printf("Usage %s <query image filename> <directory name>\n", argv[0]);
		exit(-1);
	}
	strcpy(filename, argv[1]);

	// read the image
	baseimg = cv::imread(filename);
	
	// test if the read was successful
	if(baseimg.data == NULL) {
		printf("Unable to read image %s\n", filename);
		exit(-1);
	}
	

	// by default, look at the current directory
	strcpy(dirname, ".");

	// if the user provided a directory path, use it
	if(argc > 1) {
		strcpy(dirname, argv[2]);
	}
	printf("Accessing directory %s\n\n", dirname);

	// open the directory
	dirp = opendir( dirname );
	if( dirp == NULL ) {
		printf("Cannot open directory %s\n", dirname);
		exit(-1);
	}
	
	//Variables to be used in this process
	cv::Mat curimg; //current image
	std::vector<float> ssds; //vector of SSD values
	std::vector<cv::Mat> imgs; //vector of the images
	int count = 0;
	// loop over the contents of the directory, looking for images
	while( (dp = readdir(dirp)) != NULL ) 
	{
		if( strstr(dp->d_name, ".jpg") || strstr(dp->d_name, ".png") || 
			strstr(dp->d_name, ".ppm") || strstr(dp->d_name, ".tif") ) 
		{
			//Opening the image into a mat in a pretty dumb way, but it works
			char newfilename[256] = "";
			strcat(newfilename, dirname);
			strcat(newfilename, "/");
			strcat(newfilename, dp->d_name);
			
			//loading the image and adding it to it's vector
			curimg = cv::imread(newfilename);
			imgs.push_back(curimg);	
	
			//Calculating image difference from base image and adding to to the vector
			ssds.push_back(calculateDif(baseimg, curimg));	
		}
	}
	
	//Getting the five closest images to base	
	for(int i = 0; i < 5; i++)
	{
		//Finding the index of the lowest SSD		
		int min_index = std::min_element(ssds.begin(),ssds.end()) - ssds.begin();
		
		std::string s = std::to_string(i);
		std::string outputname = "./outputp1/image"+s+".jpg";
		
		//outputting images to output folder
		cv::imwrite(outputname, imgs.at(min_index));
		
		//clearing lowest value SSD from the vector 		
		ssds.erase(ssds.begin()+(min_index-1));		
	}	
	
	// close the directory
	closedir(dirp);
		
	printf("\nTerminating\n");

	return(0);
}

//Function to calculate the difference between images, changes depending on what style
//of comparison is being used. This one is SSD.
int calculateDif(cv::Mat baseimg, cv::Mat curimg)
{
	//Values to start the 5x5 pixel selection, currently assumes the images are the same size
	int base_x = baseimg.cols / 2;
	int base_y = baseimg.rows / 2;
	int cur_x = curimg.cols/2;
	int cur_y = curimg.rows/2;
	
	float bval = 0.0;
	float gval = 0.0;
	float rval = 0.0;
	std::vector<cv::Vec3b> basepixs;
	std::vector<cv::Vec3b> curpixs;
	
	for(int i=base_y; i < base_y+5; i++)
	{
		for(int j=base_x; j < base_x+5; j++)
		{	
			basepixs.push_back(baseimg.at<cv::Vec3b>(j,i));
		}	
	}

	for(int i=cur_y; i < cur_y+5; i++)
	{
		for(int j=cur_x; j < cur_x+5; j++)
		{	
			curpixs.push_back(curimg.at<cv::Vec3b>(j,i));
		}	
	}
	
	for(int i = 0; i < 25; i++)
	{
		cv::Vec3b base_pixel = basepixs.at(i);
		cv::Vec3b cur_pixel =  curpixs.at(i);

		float btemp = base_pixel[0] - cur_pixel[0];
		float gtemp = base_pixel[1] - cur_pixel[1];
		float rtemp = base_pixel[2] - cur_pixel[2];
		
		bval += btemp*btemp;
		gval += gtemp*gtemp;
		rval += rtemp*rtemp;
	}
	return bval + gval + rval;	
}

	




