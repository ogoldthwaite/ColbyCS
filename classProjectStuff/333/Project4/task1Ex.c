/**
 * Given an array of random integers, sort it in such a way that the even 
 * numbers appear first and the odd numbers appear later. The even numbers 
 * should be sorted in descending order and the odd numbers should be sorted 
 * in ascending order.
 *
 * Ying Li
 * 08/02/2016
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>


long long getMS();
int fastComp( const void *p1, const void *p2);

/* the comparator funciton used in qsort */
int comparator (const void *p1, const void *p2) 
{
    if( (*(int*)p1 % 2 == 0) && (*(int*)p2 % 2 == 0) )
    {
        if(*(int*)p1 == *(int*)p2)
            return 0;
        else
            return *(int*)p1 > *(int*)p2 ? -1 : 1; //p1 before p2 if p1 is larger
    }
    else if( (*(int*)p1 % 2 != 0) && (*(int*)p2 % 2 != 0) )
    {
        if(*(int*)p1 == *(int*)p2)
            return 0;
        else
            return *(int*)p1 < *(int*)p2 ? -1 : 1; //p1 before p2 if p1 is smaller
    }
    else
        return *(int*)p1 % 2 == 0 ? -1 : 1; //p1 first if it's even

}

int fastComp( const void *p1, const void *p2 )
{
    int p1val = (*(int*)p1);
    int p2val = (*(int*)p2);
    int p1bool = p1val % 2;
    int p2bool = p2val % 2;

    if(!p1bool && !p2bool)
    {
        if(p1val == p2val)
            return 0;
        else
            return p1val > p2val ? -1 : 1; //p1 before p2 if p1 is larger
    }
    else if( p1bool && p2bool )
    {
        if(p1val == p2val)
            return 0;
        else
            return p1val < p2val ? -1 : 1; //p1 before p2 if p1 is larger
    }
    else
        return !p1bool ? -1 : 1; //p1 first if it's even

}

int main (int argc, char **argv) {
    long ms =  getMS(); //Getting current time	
    size_t size = 100000000;
	//int ary[] = {10, 11, 1, 8, 9, 0, 13, 4, 2, 7, 6, 3, 5, 12};
	//int size = sizeof(ary) / sizeof(int);

    int* ary = malloc(size * sizeof(int));
    int* otherary = malloc(size * sizeof(int));

    
    for(size_t i = 0; i < size; i++)
    {
        ary[i] = i;
        otherary[i] = i;
    }

    printf("Starting normal comparator...\n");
    ms = getMS();
	qsort((void *) ary, size, sizeof(int), comparator);
    printf("Time taken (ms): %ld\n", getMS() - ms);


    printf("Starting faster comparator...\n");
    ms = getMS();
	qsort((void *) ary, size, sizeof(int), fastComp);
    printf("Time taken (ms): %ld\n", getMS() - ms);

    
	// printf("The sorted array is: ");
	// for (int i = 0; i < size; i++) {
	// 	printf("%d ", ary[i]);
	// }
	printf("\n");

	return 0;
}


long long getMS() 
{
    struct timeval tv;

    gettimeofday(&tv,NULL);
    return (((long long)tv.tv_sec)*1000)+(tv.tv_usec/1000);
}