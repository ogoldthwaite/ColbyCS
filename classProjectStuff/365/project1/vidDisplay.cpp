/*
	Bruce A. Maxwell
	S19
	Simple example of video capture and manipulation
	Based on OpenCV tutorials

	Compile command (macos)

	clang++ -o newvid -I /opt/local/include vidDisplay.cpp -L /opt/local/lib -lopencv_core -lopencv_highgui -lopencv_video -lopencv_videoio

	use the makefiles provided

	make newvid

*/
#include <cstdio>
#include <opencv2/opencv.hpp>


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

	cv::namedWindow("Video", 1); // identifies a window?
	cv::Mat frame;
	
	int effect = 1;
	for(;;) {
		*capdev >> frame; // get a new frame from the camera, treat as a stream

		if( frame.empty() ) {
		  printf("frame is empty\n");
		  break;
		}
		
		int rx = rand() % frame.rows;
		int ry = rand() % frame.cols;
		int dist = rand() % 250;	

			
		for(int i = 0; i < dist; i++)
		{	
			frame.at<cv::Vec3b>(rx+i,ry)[0] = 0;  
			frame.at<cv::Vec3b>(rx+i,ry)[1] = 0;  
			frame.at<cv::Vec3b>(rx+i,ry)[2] = 0;  
		}
		if(effect == 1)
			effect = 0;
		else
			effect = 1;
		
		cv::imshow("Video", frame);

		if(cv::waitKey(1) == 'q') {
		   break;
		}

	}

	// terminate the video capture
	printf("Terminating\n");
	delete capdev;

	return(0);
}
