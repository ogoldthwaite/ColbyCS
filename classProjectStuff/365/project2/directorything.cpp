/*
	Bruce A. Maxwell

	Simple example showing how to get a listing of all files in a directory.  

	Code modeled on the sample code in the man pages for directory.

	man directory

*/
#include <cstdio>
#include <cstdlib>
#include <dirent.h>
#include <cstring>

int main(int argc, char *argv[]) {
	char dirname[256];
	DIR *dirp;
	struct dirent *dp;

	// by default, look at the current directory
	strcpy(dirname, "stolenimages");

	// if the user provided a directory path, use it
	if(argc > 1) {
		strcpy(dirname, argv[1]);
	}
	printf("Accessing directory %s\n\n", dirname);

	// open the directory
	dirp = opendir( dirname );
	if( dirp == NULL ) {
		printf("Cannot open directory %s\n", dirname);
		exit(-1);
	}

	// loop over the contents of the directory, looking for images
	while( (dp = readdir(dirp)) != NULL ) {
		printf("hey");
		if( strstr(dp->d_name, ".dng") ||
				strstr(dp->d_name, ".png") ||
				strstr(dp->d_name, ".ppm") ||
				strstr(dp->d_name, ".tif") ) {

			printf("image file: %s\n", dp->d_name);

		}
	}

	// close the directory
	closedir(dirp);
		
	printf("\nTerminating\n");

	return(0);
}

