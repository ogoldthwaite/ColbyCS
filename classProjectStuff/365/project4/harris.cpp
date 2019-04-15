
#include <cstdio>
#include <opencv2/opencv.hpp>
#include <stdio.h>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

int main(int argc, char *argv[]) {
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
	
	for(;;) 
	{
		*capdev >> frame;

		if( frame.empty() ) 
		{
		  printf("frame is empty\n");
		  break;
		}
		
		Mat gray = frame;
		cvtColor(gray, gray, CV_BGR2GRAY);

		Mat dest, destNorm, destNormScaled;

		int blocksize = 2;
		int aperturesize = 3;
		double k = 0.04;
		
		cornerHarris(gray, dest, blocksize, aperturesize, k, BORDER_DEFAULT);

		normalize( dest, destNorm, 0, 255, NORM_MINMAX, CV_32FC1, Mat() );
  		convertScaleAbs( destNorm, destNormScaled );

		for( int j = 0; j < destNorm.rows ; j++ )
     	{ 		
		for( int i = 0; i < destNorm.cols; i++ )
          {
            if( (int) destNorm.at<float>(j,i) > 200 )
              {            				
				circle( frame, Point( i, j ), 5,  Scalar(255,51,255), 2, 8, 0 );
				line( frame, Point(i,j), Point(i, j-100), Scalar(255,51,255), 1);
              }
          }
     	}

		imshow("Video", frame);

		if(cv::waitKey(10) == 'p')
		{	    
			imwrite("./HarrisImg2.png", frame);	
		}		

		if(cv::waitKey(10) == 'q')
		{	    		
			break;
		}

	}

	printf("Terminating\n");
	delete capdev;

	return(0);
}
