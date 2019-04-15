
#include <cstdio>
#include <opencv2/opencv.hpp>
#include <stdio.h>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

vector<Point2f> generatePose(vector<Point2f> imagePoints, Mat camMat, Mat distCoeffs);

int main(int argc, char *argv[]) {
	//Reading in camera calibration parameters
	Mat camMat = Mat(3,3, CV_64FC1);
	Mat distorts = Mat(1,5, CV_64FC1);
		
	std::ifstream infile("./camdistort.txt");
	double val;
	
	int count = 0;
	int row = 0;
	int col = 0;
	while(infile >> val)
	{
		if(count < 9) //Camera Matrix
		{
			camMat.at<double>(row,col++) = val;
			if(col == 3)
			{
				col = 0;
				row++;
			}
			count++;
		}
		else
		{			
			distorts.at<double>(0, col++) = val;
		}
	}

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
	
	
	vector<Point2f> imgPts;
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

			imgPts = generatePose(cornerSet, camMat, distorts);
		}

		if(imgPts.size() != 0)
		{
			/*	
			//Axes Draw		
			Point2f origin = imgPts[0];	
			//Names correspond to how far these points are from origin			
			Point2f oppOrigin = imgPts[53];
			Point2f shortOrigin = imgPts[5];
			Point2f farOrigin = imgPts[48];	
					
			circle(frame, origin, 5, Scalar(255,51,255));
			circle(frame, shortOrigin, 5, Scalar(255,51,255));
			circle(frame, oppOrigin, 5, Scalar(255,51,255));
			circle(frame, farOrigin, 5, Scalar(255,51,255));
			
			line(frame, origin, Point2f(origin.x,origin.y-100), Scalar(255,51,255), 2);
			line(frame, origin, shortOrigin, Scalar(255,51,255), 2);
			line(frame, origin, farOrigin, Scalar(255,51,255), 2);
			*/
			
			//Display points numbers
			/*
			int height = 0;			
			for(int i = 0; i < imgPts.size(); i++)
			{
				string s = std::to_string(i);
				Point2f pt = Point2f(imgPts[i].x,imgPts[i].y-height++);
				cv::putText(frame, s, pt,
				 cv::FONT_HERSHEY_COMPLEX, 0.5, cv::Scalar(255,51,255), 1, CV_AA);
			}
		    */
			//Creating Shape Thing
			
			Point points[1][4];
			points[0][0] = imgPts[0];
			points[0][1] = imgPts[48];
			points[0][2] = imgPts[53];
			points[0][3] = imgPts[5];	
			
			const Point* ppt[1] = { points[0] };
			int npt[] = { 4 };
	
			fillPoly(frame, ppt, npt, 1, Scalar(0), 8);
			
			line(frame, imgPts[37], imgPts[19], Scalar(255,51,255), 2);
			
			Point2f topPt1 = Point2f(imgPts[19].x,imgPts[19].y-75);
			Point2f topPt2 = Point2f(imgPts[37].x,imgPts[37].y-75);
			
			line(frame, imgPts[19], topPt1, Scalar(255,51,255), 2);
			line(frame, imgPts[37], topPt2, Scalar(255,51,255), 2);
			line(frame, topPt1, topPt2, Scalar(255,51,255), 2);
			
			line(frame, topPt1, imgPts[22], Scalar(255,51,255), 2);
			line(frame, topPt2, imgPts[22], Scalar(255,51,255), 2);
			line(frame, imgPts[19], imgPts[22], Scalar(255,51,255), 2);
			line(frame, imgPts[37], imgPts[40], Scalar(255,51,255), 2);
			line(frame, imgPts[40], imgPts[22], Scalar(255,51,255), 2);
		
			
			
		}
		
		cv::imshow("Video", frame);
		

		if(cv::waitKey(10) == 'q')
		{	    			
			break;
		}

	}

	printf("Terminating\n");
	delete capdev;

	return(0);
}


vector<Point2f> generatePose(vector<Point2f> imagePoints, Mat camMat, Mat distCoeffs)
{
	//Building pointSet
	int vert = 0;
	int hori = 0;
	int cornerPerCol = 6;
	vector<Point3f> objectPoints;
	for(int i = 1; i < imagePoints.size()+1; i++)
	{
		objectPoints.push_back(Point3f(vert--, hori, 0));
		if( (i % cornerPerCol == 0) && (imagePoints[0] != imagePoints[i]) )
		{
			vert = 0;
			hori++;
		}	
	}

	Mat	rotations;
	Mat translations;
	
	solvePnP(objectPoints, imagePoints, camMat, distCoeffs, rotations, translations, 0);
		
	cout << "Rotation" << endl << rotations << "\n\n" << endl;
	cout << "Translation" << endl << translations << "\n\n" << endl;

	vector<Point2f> newImagePoints;
	projectPoints(objectPoints, rotations, translations, camMat, distCoeffs,
				 newImagePoints);

	return newImagePoints;
}
