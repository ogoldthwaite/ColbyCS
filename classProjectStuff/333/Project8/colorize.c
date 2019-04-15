#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/time.h>
#include "ppmIO.h"

typedef struct ThreadSegment
{
	int rows;
	int cols;
	int start;
	Pixel* src;
}ThreadSegment;

long long getMS();

void* tProcess(void* args)
{
    ThreadSegment* seg = (ThreadSegment*) args;
	srand(time(0));

	for(size_t j = 0; j < 50; j++)
	{
		for(size_t i=seg->start; i < seg->rows*seg->cols; i++) 
		{
			// seg->src[i].r = seg->src[i].r > 128 ? (220+seg->src[i].r)/2 : (30+seg->src[i].r)/2;
			// seg->src[i].g = seg->src[i].g > 128 ? (220+seg->src[i].r)/2 : (30+seg->src[i].g)/2;
			// seg->src[i].b = seg->src[i].b > 128 ? (220+seg->src[i].r)/2 : (30+seg->src[i].b)/2;
			seg->src[i].b = rand() % 255; //red
			seg->src[i].r = rand() % 255; //green
			seg->src[i].g = rand() % 255; //blue
		}
	}
    
}

int main(int argc, char *argv[]) {
	Pixel *src;
	int rows, cols, colors;
	int i;

	// check usage
	if( argc < 2 ) {
		printf("Usage: %s <image filename>\n", argv[0]);
		exit(-1);
	}

	// read image and check for errors
	src = ppm_read( &rows, &cols, &colors, argv[1] );
	if( !src ) {
		printf("Unable to read file %s\n", argv[1]);
		exit(-1);
	}

	size_t threadcount;
    printf("Enter a number of threads: \n");
    scanf("%d", &threadcount);

	// process image normalls
	long curtime = getMS();

	for(size_t j = 0; j < 50; j++)
	{
		for(i=0;i<rows*cols;i++) {
			// src[i].r = src[i].r > 128 ? (220+src[i].r)/2 : (30+src[i].r)/2;
			// src[i].g = src[i].g > 128 ? (220+src[i].g)/2 : (30+src[i].g)/2;
			// src[i].b = src[i].b > 128 ? (220+src[i].b)/2 : (30+src[i].b)/2;
			src[i].b = rand() % 255; //red
			src[i].r = rand() % 255; //green
			src[i].g = rand() % 255; //blue
		}
	}

	printf("Time for normal: %ld ms\n", getMS()-curtime);
	
	curtime = getMS();

	int rowseg = rows / threadcount;
	int colseg = cols / threadcount;

	ThreadSegment* segs[threadcount];
    pthread_t threads[threadcount];

	int colstart = 0;
	int rowstart = 0;
	int lastend = 0;
	for(size_t i = 0; i < threadcount; i++) //Initializing the thread structs
	{
	   	ThreadSegment* seg = (ThreadSegment*) malloc(sizeof(ThreadSegment));
		seg->src = src;
		seg->cols = colstart + colseg;
		seg->rows = rowstart + rowseg;
		seg->start = lastend;

		colstart = seg->cols;
		rowstart = seg->rows;
		lastend = colstart*rowstart;

		//printf("S: %d  R: %d  C: %d\n", seg->start, seg->rows,seg->cols);

		segs[i] = seg;
	}

	for(size_t i=0; i < threadcount; i++) //running threads
        pthread_create(&(threads[i]), NULL, tProcess, (segs[i]) );

	for(size_t i=0; i < threadcount; i++) //joining threads            
		pthread_join( threads[i], NULL );   
       

	printf("Time for threaded: %ld ms\n", getMS()-curtime);

	// write out the image
	ppm_write( src, rows, cols, colors, "bold.ppm" );

	free(src);

	return(0);
}

long long getMS() //Gets current time!
{
    struct timeval tv;

    gettimeofday(&tv,NULL);
    return (((long long)tv.tv_sec)*1000)+(tv.tv_usec/1000);
}