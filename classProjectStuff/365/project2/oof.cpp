#include <opencv2/opencv.hpp>
#include <cstdio>
#include <cstdlib>
#include <dirent.h>
#include <cstring>


int main(int argc, char *argv[]) 
{
	int prevrow = 0;
	cv::Mat img = cv::imread("base2.jpg");
	
	cv::Mat halfimg = cv::Mat(img, cv::Rect(0,prevrow,img.cols,img.rows/3));
	
	cv::imwrite("test1.jpg", halfimg);
	prevrow += img.rows/3;
	cv::Mat halfimg2 = cv::Mat(img, cv::Rect(0,prevrow,img.cols,img.rows/3));
	
	cv::imwrite("test2.jpg", halfimg2);

}
