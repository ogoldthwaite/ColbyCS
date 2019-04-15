
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
	
	
	vector<vector<Point2f>> cornerList;
	vector<vector<Point3f>> pointList;
	vector<Mat> calibrationImages;
	vector<vector<Mat>> rotationTranslation;
	int imgnum = 0;

	for(;;) 
	{
		*capdev >> frame;

		if( frame.empty() ) 
		{
		  printf("frame is empty\n");
		  break;
		}
				
		Size patternsize(6,9); //interior number of corners
		Mat gray = frame; //source image
		cvtColor(gray, gray, CV_BGR2GRAY);
		vector<Point2f> cornerSet; //this will be filled by the detected corners

		bool patternfound = findChessboardCorners(gray, patternsize, cornerSet);

		if(patternfound)
		{
			cornerSubPix(gray, cornerSet, Size(11, 11), Size(-1, -1),
				TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
			
			//drawChessboardCorners(frame, patternsize, Mat(cornerSet), patternfound);
		}
		drawChessboardCorners(frame, patternsize, Mat(cornerSet), patternfound);
		

		cv::imshow("Video", frame);
		
		//Saving an image for calibration
		if(cv::waitKey(10) == 's')
		{		
			vector<Point3f> pointSet;
			
			//Building pointSet
			int vert = 0;
			int hori = 0;
			int cornerPerCol = 6;
			for(int i = 1; i < cornerSet.size()+1; i++)
			{
				pointSet.push_back(Point3f(vert--, hori, 0));
				if( (i % cornerPerCol == 0) && (cornerSet[0] != cornerSet[i]) )
				{
					vert = 0;
					hori++;
				}	
			}
			cornerList.push_back(cornerSet);
			pointList.push_back(pointSet);
			string s = std::to_string(imgnum++);
			string outputname = "./calibrationImages/image"+s+".png";
			imwrite(outputname, frame);
			//Saving calibration image
			calibrationImages.push_back(gray);
			cout << pointList.size() << endl;			
		}	

		if(cv::waitKey(10) == 'c')
		{
			double camInit[3][3] = { {1.0, 0.0, frame.cols/2.0},
									 {0.0, 1.0, frame.rows/2.0},
									 {0.0, 1.0,     1.0     } };

			Mat camMat = Mat(3,3, CV_64FC1, camInit);
			Mat distorts;
			vector<Mat>	rotations;
			vector<Mat> translations;
			
			double error = calibrateCamera(pointList, cornerList, gray.size(), camMat,
							 distorts,rotations, translations, CV_CALIB_FIX_ASPECT_RATIO);

			cout << camMat << "\n" << endl;
			cout << distorts << "\n" << endl;
			cout << error << "\n" << endl;

			//Writing out camera matrix and distortion coefficients
			//First 9 things wrote out is the camera matrix row by row, rest is distortion
			std::ofstream matrixdistortOut;
			matrixdistortOut.open("./camdistort.txt");
			
			for(int i = 0; i < 3; i++)
				for(int j = 0; j < 3; j++)
					matrixdistortOut << camMat.at<double>(i, j) << endl;

			for(int j = 0; j < 5; j++)
				matrixdistortOut << distorts.at<double>(0,j) << endl;
			
			//Saving/Outputting rotations and translations
			rotationTranslation.clear();
			rotationTranslation.push_back(rotations);
			rotationTranslation.push_back(translations);
	
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
