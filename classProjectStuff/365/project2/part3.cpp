
#include <opencv2/opencv.hpp>
#include <cstdio>
#include <cstdlib>
#include <dirent.h>
#include <cstring>

double calculateDif(std::vector<cv::Mat> base_hists, cv::Mat curimg);

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
	
	std::vector<cv::Mat> baseimgsects; //vector for parts of base image
	std::vector<cv::Mat> basehistsects; //vector for histograms for each base image piece

	//Splitting up base image and adding them to the vector
	int prevrow = 0;
	for(int i = 0; i < 3; i++)
	{
		baseimgsects.push_back(cv::Mat(baseimg, cv::Rect(0,prevrow,baseimg.cols,baseimg.rows/
																			3)));	
		prevrow+=baseimg.rows/3;		
	}

	//calculating base image histograms
	int channels[] = {0,1};
	const int histsize[] = {60, 80};
	float hrange[] = {0,180};
	float srange[] = {0,256};
	const float* histrange[] = {hrange, srange};
	bool uniform = true;
	bool accumulate = false;
	
	for(int i = 0; i < baseimgsects.size(); i++)
	{
		cv::Mat temphist;		

		calcHist(&baseimgsects.at(i), 1, channels, cv::Mat(), temphist, 1, histsize,
			 	 histrange, uniform, accumulate);
		
		normalize(temphist, temphist, 0, baseimgsects.at(i).rows, cv::NORM_MINMAX, -1,
				 cv::Mat());
		
		basehistsects.push_back(temphist);
	}

	cv::Mat curimg; //current image
	std::vector<cv::Mat> imgs; //vector of the images

	//Calculating all the other image histograms
	std::map<double, cv::Mat> dists_Img_Map;
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
			double dif = calculateDif(basehistsects, curimg);
			dists_Img_Map.emplace(dif, imgs.back()); //adding value and image to map
		}
	}
	
	//Getting all keys out of the map
	std::vector<double> keys;
	int i = 0;
	for(std::map<double, cv::Mat>::iterator itr = dists_Img_Map.begin(); itr !=
		 dists_Img_Map.end(); ++itr) 
	{
  		keys.push_back(itr->first);
		i++;
	}
	//Sorting the key vector, lowest should be first
	std::sort(keys.begin(), keys.end());
	//Getting the ten closest images to base	
	for(int i = 0; i < 10; i++)
	{
		double curvalue = keys.back();
		keys.pop_back();			
		cv::Mat outputimg = dists_Img_Map.at(curvalue);

		std::string s = std::to_string(i);
		std::string outputname = "./outputp3/image"+s+".jpg";
		
		//outputting images to output folder
		cv::imwrite(outputname, outputimg);	
	}	
	
	// close the directory
	closedir(dirp);
		
	printf("\nTerminating\n");

	return(0);
}

//Function to calculate the difference between images, changes depending on what style
//of comparison is being used. This one is SSD.
double calculateDif(std::vector<cv::Mat> base_hists, cv::Mat curimg)
{	
	//Splitting up cur image and adding the results to the vector
	std::vector<cv::Mat> curimgsects;
	int prevrow = 0;
	for(int i = 0; i < 3; i++)
	{
		curimgsects.push_back(cv::Mat(curimg, cv::Rect(0,prevrow,curimg.cols,curimg.rows/
																			3)));	
		prevrow+=curimg.rows/3;		
	}

	//Making current image histograms	
	std::vector<cv::Mat> cur_hists;
	int channels[] = {0,1};
	const int histsize[] = {60, 80};
	float hrange[] = {0,180};
	float srange[] = {0,256};
	const float* histrange[] = {hrange, srange};
	bool uniform = true;
	bool accumulate = false;	

	for(int i = 0; i < curimgsects.size(); i++)
	{
		cv::Mat temphist;		

		calcHist(&curimgsects.at(i), 1, channels, cv::Mat(), temphist, 1, histsize,
			 	 histrange, uniform, accumulate);
		
		normalize(temphist, temphist, 0, curimgsects.at(i).rows, cv::NORM_MINMAX, -1,
				 cv::Mat());
		
		cur_hists.push_back(temphist);
	}
	
	double compval = 0.0;
	for(int i = 0; i < curimgsects.size(); i++)
	{
		compval += compareHist(base_hists.at(i), cur_hists.at(i), 0);
	}
	
	return compval;

}

	




