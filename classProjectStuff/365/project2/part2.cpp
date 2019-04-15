
#include <opencv2/opencv.hpp>
#include <cstdio>
#include <cstdlib>
#include <dirent.h>
#include <cstring>

double calculateDif(cv::Mat mainImg, cv::Mat img);

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
	std::vector<double> dists; //vector of distance values
	std::vector<cv::Mat> imgs; //vector of the images

	//calculating base histogram
	cv::Mat basehist;
	int channels[] = {0,1};
	const int histsize[] = {60, 80};
	float hrange[] = {0,180};
	float srange[] = {0,256};
	const float* histrange[] = {hrange, srange};
	bool uniform = true;
	bool accumulate = false;

	calcHist(&baseimg, 1, channels, cv::Mat(), basehist, 1, histsize, histrange, uniform, 
	    		 accumulate);
	normalize(basehist, basehist, 0, baseimg.rows, cv::NORM_MINMAX, -1, cv::Mat());

	
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
			dists.push_back(calculateDif(basehist, curimg));
			//printf("Val: %f\n", calculateDif(basehist, curimg));
		}
	}
	
	//Getting the five closest images to base	
	for(int i = 0; i < 10; i++)
	{
		//Finding the index of the lowest distance		
		int min_index = std::min_element(dists.begin(),dists.end()) - dists.begin();
		
		std::string s = std::to_string(i);
		std::string outputname = "./outputp2/image"+s+".jpg";
		
		//outputting images to output folder
		cv::imwrite(outputname, imgs.at(min_index));
		
		//clearing lowest value SSD from the vector 		
		dists.erase(dists.begin()+(min_index-1));		
	}	
	
	// close the directory
	closedir(dirp);
		
	printf("\nTerminating\n");

	return(0);
}

//Function to calculate the difference between images, changes depending on what style
//of comparison is being used. This one is SSD.
double calculateDif(cv::Mat basehist, cv::Mat curimg)
{	
	cv::Mat curhist;
	int channels[] = {0,1};
	const int histsize[] = {60, 80};
	float hrange[] = {0,180};
	float srange[] = {0,256};
	const float* histrange[] = {hrange, srange};
	bool uniform = true;
	bool accumulate = false;	
	calcHist(&curimg, 1, channels, cv::Mat(), curhist, 1, histsize, histrange, uniform, 
	    		 accumulate);
	normalize(curhist, curhist, 0, curimg.rows, cv::NORM_MINMAX, -1, cv::Mat());
	
	double compval = compareHist(basehist, curhist, 3);
	return compval;

}

	




