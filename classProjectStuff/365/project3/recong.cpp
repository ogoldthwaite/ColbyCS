// Owen Goldthwaite
// 2/8/19
// Object Recongnition File 

#include <opencv2/opencv.hpp>
#include <cstdio>
#include <cstdlib>
#include <dirent.h>
#include <cstring>
#include <string.h>
#include <math.h>
#include <fstream>
#include <iterator>

cv::Mat morphProcess(cv::Mat img);
std::vector<double> computeFeatures(cv::Mat img);
std::vector<double> computeFeaturesWithDraw(cv::Mat img, int drawcount);
std::vector<cv::Point> getLargestContour(std::vector<std::vector<cv::Point>> contours);
std::map<std::vector<double>, std::string> readVectorDatabase(std::string filename);
double calculateEuclidDist(std::vector<double> baseVec, std::vector<double> curVec, std::vector<std::vector<double>> meanStds);
std::vector<std::vector<double>> calcMeanStdev(std::vector<std::vector<double>> featureVecs);
std::vector<double> findClosestObject(std::vector<double> checkFeat, std::vector<std::vector<double>> featureDB);
std::vector<double> computeFeatures(cv::Mat img);
void writeNewUnknown(std::string filename, std::vector<double> featureVec);

using namespace std;
using namespace cv;

int main(int argc, char *argv[]) 
{
	//Initializing stuff for command lind inputs
	char dirname[256];
	DIR *dirp;
	struct dirent *dp;

	char vecDBName[256];
	char vidBool[256];

	// usage statement
	if(argc < 4) {
		printf("Usage %s <vector database filename> <image directory name> <1 for add objects w/ video, 0 for no> \n", argv[0]);
		exit(-1);
	}
	strcpy(vecDBName, argv[1]);
	strcpy(vidBool, argv[3]);
	//builtDB is just used a boolean to stop seg faults if vector.txt is empty
	int builtDB;
	std::cout << "Do you have a built vector dataset already? 1 for yes, 0 for no." << std::endl;
	std::cin >> builtDB;


	// read in vector database form the vector.txt
	std::map<std::vector<double>, std::string> vectorDB = readVectorDatabase(vecDBName);

	//Getting all keys out of the map and adding them to a features vector vector #lol
	std::vector<std::vector<double>> featureVectors;
	int i = 0;
	for(std::map<std::vector<double>, std::string>::iterator itr = vectorDB.begin(); itr != vectorDB.end(); ++itr) 
	{
  		featureVectors.push_back(itr->first);
		i++;
	}

	// ---------------------------------------------
	// This if is mainly for initial training from given images and testing when not in Davis
	// It uses no video input, just images from a directory and that kinda stoooof.
	if(strcmp(vidBool, "0") == 0)
	{		
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
		
		int count = 0;
		cv::Mat curimg;

		int training;
		cout << "Building the vector file with images or identifiying objects in other images? 1 for build 0 for not: " << endl;
		cin >> training;

		if(builtDB == 1 && training == 0)
		{
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

					//Reading in image
					curimg = cv::imread(newfilename);	

					// Computing the feature vector of the given image and finding the closest vector inside the database
					// Then using that closest vector to access DB map to get the label of the image
					// Currently computing with the drawing function because 
					std::vector<double> closestVec;
					std::vector<double> featureVec = computeFeatures(curimg);
					if(builtDB == 1)
						closestVec = findClosestObject(featureVec, featureVectors);
					//Just writing a label onto the video frame with object label
					std::string label = vectorDB.at(closestVec);
					cv::putText(curimg, label, cv::Point(50,50), cv::FONT_HERSHEY_COMPLEX, 1.0, cv::Scalar(255,255,255), 1, CV_AA);
					
					//Image output
					std::string s = std::to_string(count++);
					std::string outputname = "./output/image"+s+".png";

					cv::imwrite(outputname, curimg);
				}
			}

		}
		else
		{
			cout << "Not testing because either there is no built vectorDB already or you didnt want too!" << endl;
			//Opening file for writing vector information
			std::ofstream vectorOutput;
			vectorOutput.open("./vectors.txt");
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

					//Reading in image
					curimg = cv::imread(newfilename);	

					// Computing the feature vector of the given image and finding the closest vector inside the database
					// Then using that closest vector to access DB map to get the label of the image
					// Currently computing with the drawing function because 
					std::vector<double> closestVec;
					std::vector<double> featureVec = computeFeaturesWithDraw(curimg, count++);
					if(builtDB == 1)
						closestVec = findClosestObject(featureVec, featureVectors);

					//Writing out vector information to a .txt file. 
					for(size_t i = 0; i < featureVec.size(); i++)
					{
						vectorOutput << featureVec[i] << " ";
					}
					std::string imagefile = dp->d_name;
					std::string name = imagefile.substr(0, imagefile.find("."));
					vectorOutput << name << std::endl;
				}
			}
			// This is just a little trivial test to make sure everything is working
			curimg = cv::imread("test.png");	
			std::vector<double> featureVec = computeFeatures(curimg);
			std::vector<double> closestVec = findClosestObject(featureVec, featureVectors);
			std::cout << "Item is: " << vectorDB.at(closestVec) << "\n";
		}
	
	}
	else
	{ 
	// ----------------------------------------------------------
	// This is the actual part that we will test with, image read in from camera and all that. I haven't tested it yet
	// but it will use the same code as the previous part just from a video so I highly doubt it won't work. The N key part
	// might not work but that's easy to fix when I need too.
		if(!(strcmp(vidBool, "0") == 0))
		{
			//Video input stuff here
			cv::VideoCapture *capdev;

			// open the video device
			capdev = new cv::VideoCapture(0);
			if( !capdev->isOpened() ) {
				printf("Unable to open video device\n");
				return(-1);
			}

			cv::Size refS( (int) capdev->get(cv::CAP_PROP_FRAME_WIDTH ),
					(int) capdev->get(cv::CAP_PROP_FRAME_HEIGHT));

			printf("Expected size: %d %d\n", refS.width, refS.height);

			cv::namedWindow("Video", 1); 
			cv::Mat frame;
			
			int effect = 1;
			for(;;) {
				*capdev >> frame; // get a new frame from the camera, treat as a image

				if( frame.empty() )
				{
					printf("frame is empty\n");
					break;
				}
				
				//same stuff as before really, 
				std::vector<double> closestVec;
				std::vector<double> featureVec = computeFeaturesWithDraw(frame, 0);
				if(builtDB == 1)
					closestVec = findClosestObject(featureVec, featureVectors);

				//Just writing a label onto the video frame with object label
				std::string label = vectorDB.at(closestVec);
				cv::putText(frame, label, cv::Point(50,50), cv::FONT_HERSHEY_COMPLEX, 1.0, cv::Scalar(0,0,0), 1, CV_AA);

				cv::imshow("Video", frame);

				// Hitting N to add the current object's vector to the database, type in a label.
				if(cv::waitKey(1) == 'n') 
					writeNewUnknown(vecDBName, featureVec);
				

				if(cv::waitKey(1) == 'q') 
					break;

			}

			// terminate the video capture
			printf("Terminating\n");
			delete capdev;

			return(0);
		}
		else
		{
			printf("\nSome argument was invalid, try again :)\n");
			exit(-1);
		}
	}
}

//Just a function to append stuff to a file, simple!
void writeNewUnknown(std::string filename, std::vector<double> featureVec)
{
	std::string label;
	std::cout << "Enter a label for this new object: " << "\n";
	std::cin >> label;

	std::ofstream vectorOutput;
	vectorOutput.open("./vectors.txt", std::ios_base::app);

	for(size_t i = 0; i < featureVec.size(); i++)
	{
		vectorOutput << featureVec[i] << " ";
	}
	vectorOutput << label << std::endl;

	vectorOutput.close();
}

// Calculates the closest feature vector to the object using a standardized eucidean distance 
std::vector<double> findClosestObject(std::vector<double> checkFeat, std::vector<std::vector<double>> featureDB)
{
	// Generating the means and stdevs of the database vectors for standardization
	std::vector<std::vector<double>> meanStds = calcMeanStdev(featureDB);
	//Finding vector with smallest distance
	double minDist = 10000.0;
	std::vector<double> closestVec;
	for(size_t i = 0; i < featureDB.size(); i++)
	{
		// Current feature vector
		std::vector<double> curFeat = featureDB[i];

		//Calculating distance

		double dist = calculateEuclidDist(checkFeat, curFeat, meanStds);

		//Getting vector with smallest distance
		if(dist < minDist)
		{
			minDist = dist;
			closestVec = curFeat;
		}
	}

	return closestVec;
}

// This just calculates the mean and stdev of each feature in the feature vector database in order to standardize 
// so weighting of different features is pretty normal.
std::vector<std::vector<double>> calcMeanStdev(std::vector<std::vector<double>> featureVecs)
{
	double sum = 0.0;
	double mean = 0.0;
	double stdev = 0.0;
	// Creating vector of standard deviations and mean of each item in the feature vectors
	// Something like [[mean, stdev], [mean,stdev], [mean, stdev]]
	// This is just stdev math stuff, nothing special
	std::vector<std::vector<double>> returnVec;
	for(size_t j = 0; j < featureVecs[0].size(); j++)
	{
		for(size_t i = 0; i < featureVecs.size(); i++)
			sum += featureVecs[i][j];
		
		mean = sum / featureVecs.size();
		
		for(size_t k = 0; k < featureVecs.size(); k++)
			stdev += ((featureVecs[k][j] - mean) * (featureVecs[k][j] - mean));

		stdev = sqrt(stdev / featureVecs.size());
		std::vector<double> vals;
		vals.push_back(mean);
		vals.push_back(stdev);
		returnVec.push_back(vals);

		stdev = 0.0;
		mean = 0.0;
		sum = 0.0;
	}

	return returnVec;

}

// Calculating the standardized euclidean distance of the two given vectors using the means and stdevs in meanStds
double calculateEuclidDist(std::vector<double> baseVec, std::vector<double> curVec, std::vector<std::vector<double>> meanStds)
{
	std::vector<double> stdBaseVec;
	std::vector<double> stdCurVec;

	//This is just some simple math, nothing special here.
	double euclidDist = 0.0;
	for(size_t i = 0; i < baseVec.size(); i++)
	{
		double mean = meanStds[i][0];
		double stdev = meanStds[i][1];

		double baseVal = (baseVec[i]-mean)/stdev;
		double curVal = (curVec[i]-mean)/stdev;

		euclidDist += ((baseVal - curVal) * (baseVal - curVal));

		stdBaseVec.push_back( (baseVec[i]-mean)/stdev );
		stdCurVec.push_back( (curVec[i]-mean)/stdev );

	}
	euclidDist = sqrt(euclidDist);
	
	return euclidDist;

}

// This reads in the information in the vectors.txt file and creates a map of the information. 
// Each vector of doubles is mapped to a string label that denotes the object type 
std::map<std::vector<double>, std::string> readVectorDatabase(std::string filename)
{
	// opening the file and declared values
	std::ifstream infile(filename);
	double val1,val2,val3,val4,val5,val6,val7,val8,val9;
	std::string label;
	
	// declaring the map
	std::map<std::vector<double>, std::string> databaseMap;

	// looping over the .txt file information and adding to to the map
	while(infile >> val1 >> val2 >> val3 >> val4>>val5>>val6>>val7>>val8>>val9>>label)
	{
		std::vector<double> fv;
		fv.push_back(val1);
		fv.push_back(val2);
		fv.push_back(val3);
		fv.push_back(val4);
		fv.push_back(val5);
		fv.push_back(val6);
		fv.push_back(val7);
		fv.push_back(val8);
		fv.push_back(val9);

		databaseMap.emplace(fv, label);
	}
	infile.close();

	return databaseMap;
}

//this is the main function where the features are computed, this one draws them at the end as well, the other one does not.
std::vector<double> computeFeaturesWithDraw(cv::Mat img, int drawcount)
{
	//converting image to grayscale
	cv::Mat cur_gray;
	cvtColor(img, cur_gray, cv::COLOR_BGR2GRAY);

	//thresholding out the white
	cv::Mat dest;
	threshold(cur_gray, dest, 125, 255, 1);
	
	//Morphological Processing to fill holes and clear noise
	dest = morphProcess(dest);			
	
	//Conneceted Components function identifies connected component regions
	cv::connectedComponents(dest, dest, 8, CV_16U);
	
	// Normalizing so that the entire image isn't just black. Black stays black, anything other turns white so the object can
	// actually be seen
	cv::Mat visibleRegions;
	cv::normalize(dest, visibleRegions, 0, 255, cv::NORM_MINMAX, CV_8U);
	
	//Some variables for contour stuff
	std::vector<std::vector<cv::Point>> contours;
	std::vector<cv::Vec4i> hierarchy;
	
	//This function finds the contours of the image, since it has been thresholded it should mainly be the primary object
	cv::findContours(visibleRegions, contours, hierarchy, cv::RETR_TREE,
	cv::CHAIN_APPROX_SIMPLE, cv::Point(0,0));
	

	//getting largest area contour, assuming that to be the item
	std::vector<cv::Point> maxContour =  getLargestContour(contours);

	//created bounding rectangles, one for calculations and one for visualization
	cv::RotatedRect minRect = cv::minAreaRect(cv::Mat(maxContour));
	cv::Rect boundingRect = cv::boundingRect(maxContour);

	// Calculating Feature vector of each object
	// [Total Mass (moment 00), Extent of bounding box, Aspect Ratio of bounding box]
	std::vector<double> featureVec;
	cv::Moments moments = cv::moments(maxContour, false);
	cv::Point2f centroid = cv::Point2f(moments.m10/moments.m00, moments.m01/moments.m00);;

	// Total mass 
	//featureVec.push_back(moments.m00);
	// Exxtent
	double rectWidth = boundingRect.width;
	double rectHeight = boundingRect.height;
	double rectArea = rectWidth * rectHeight;
	double contArea = cv::contourArea(maxContour);
	featureVec.push_back(contArea / rectArea);
	// Aspect Ratio
	featureVec.push_back(rectWidth / rectHeight);
	//Eccentricity
	double val = sqrt( ( moments.m20 - moments.m02 ) *  ( moments.m20 - moments.m02 )  + 4 * moments.m11 * moments.m11);
	val = ( moments.m20 + moments.m02 + val ) / ( moments.m20 + moments.m02 - val );
	featureVec.push_back(val);
	//humoments
	double hu[7];
	cv::HuMoments(moments, hu);
	featureVec.push_back(hu[0]);
	featureVec.push_back(hu[1]);
	featureVec.push_back(hu[2]);
	featureVec.push_back(hu[3]);
	featureVec.push_back(hu[4]);
	featureVec.push_back(hu[5]);

	//---------------------------
	// All this stuff is just for drawing the images, not really necessary apart from testing.
	//Drawing Contours
	cv::Scalar color = cv::Scalar(255,255,255);
	cv::Mat drawing = cv::Mat::zeros(visibleRegions.size(), CV_8UC3);
	for(int i = 0; i < contours.size(); i++)
	{
		cv::drawContours(drawing, contours, i, color, 2, 8, hierarchy, 0 , 
						 cv::Point());
	}
	
	//Drawing bounding box
	cv::Point2f rectPoints[4];
	minRect.points(rectPoints);
	for(int j = 0; j < 4; j++)
		cv::line(drawing, rectPoints[j], rectPoints[(j+1)%4], color, 1, 8);

	//Drawing the centroid
	cv::circle(drawing, centroid, 4, color, -1, 8, 0);

	//Drawing some text for the feature
	std::string featureVal = std::to_string(featureVec[4]);
	std::string featureText = "Hu Moment 0 " + featureVal;
	cv::putText(drawing, featureText, cv::Point(50,50), cv::FONT_HERSHEY_COMPLEX, 1.0, cv::Scalar(255,255,255), 1, CV_AA);

	//Image output
	std::string s = std::to_string(drawcount);
	std::string outputname = "./output/image"+s+".png";
	
	//cv::imshow("Scary Video", drawing);
	cv::imwrite(outputname, drawing);
	
	return featureVec;
	
}

//This function is identical to the one above except it does not draw and output the images
std::vector<double> computeFeatures(cv::Mat img)
{
	//converting to grayscale
	cv::Mat cur_gray;
	cvtColor(img, cur_gray, cv::COLOR_BGR2GRAY);

	//thresholding out
	cv::Mat dest;
	threshold(cur_gray, dest, 125, 255, 1);
	
	//Morphological Processing
	dest = morphProcess(dest);			
	
	//Conneceted Components
	cv::connectedComponents(dest, dest, 8, CV_16U);
	
	cv::Mat visibleRegions;
	cv::normalize(dest, visibleRegions, 0, 255, cv::NORM_MINMAX, CV_8U);
	
	//Finding image contours
	std::vector<std::vector<cv::Point>> contours;
	std::vector<cv::Vec4i> hierarchy;

	cv::findContours(visibleRegions, contours, hierarchy, cv::RETR_TREE,
	cv::CHAIN_APPROX_SIMPLE, cv::Point(0,0));
	

	//getting largest area contour, assuming that to be the item
	std::vector<cv::Point> maxContour =  getLargestContour(contours);

	//bounding rect
	cv::RotatedRect minRect = cv::minAreaRect(cv::Mat(maxContour));
	cv::Rect boundingRect = cv::boundingRect(maxContour);

	// Feature vector of each object
	std::vector<double> featureVec;
	cv::Moments moments = cv::moments(maxContour, false);
	cv::Point2f centroid = cv::Point2f(moments.m10/moments.m00, moments.m01/moments.m00);;

	// Total mass 
	//featureVec.push_back(moments.m00);
	// Exxtent
	double rectWidth = boundingRect.width;
	double rectHeight = boundingRect.height;
	double rectArea = rectWidth * rectHeight;
	double contArea = cv::contourArea(maxContour);
	featureVec.push_back(contArea / rectArea);
	// Aspect Ratio
	featureVec.push_back(rectWidth / rectHeight);
	//Eccentricity
	double val = sqrt( ( moments.m20 - moments.m02 ) *  ( moments.m20 - moments.m02 )  + 4 * moments.m11 * moments.m11);
	val = ( moments.m20 + moments.m02 + val ) / ( moments.m20 + moments.m02 - val );
	featureVec.push_back(val);
	//humoments
	double hu[7];
	cv::HuMoments(moments, hu);
	featureVec.push_back(hu[0]);
	featureVec.push_back(hu[1]);
	featureVec.push_back(hu[2]);
	featureVec.push_back(hu[3]);
	featureVec.push_back(hu[4]);
	featureVec.push_back(hu[5]);

	
	return featureVec;
	
}

//Returns largest countour vector by area, pretty simple
std::vector<cv::Point> getLargestContour(std::vector<std::vector<cv::Point>> contours)
{
	double max = 0;
	int maxIndex = 0;
	for(int i = 0; i < contours.size(); i++)
	{				
		double area = cv::contourArea(contours[i]);
		if(area > max)
		{
			max = area;	
			maxIndex = i;
		}	
	}
	return contours[maxIndex];
}

//Does some morphological processing on the image to clear noise and holes and all that
cv::Mat morphProcess(cv::Mat img)
{
	cv::Mat element = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3), cv::Point(-1, -1));	
	
	for(int i =0; i < 1; i++)
		cv::erode(img, img, element);

	for(int i =0; i < 1; i++)
		cv::dilate(img, img, element);
		
	for(int i =0; i < 8; i++)
		cv::dilate(img, img, element);

	for(int i =0; i < 8; i++)
		cv::erode(img, img, element);
	
	return img; 
}
