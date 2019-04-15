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

int main (int argc, char **argv) {
	int ary[] = {10, 11, 1, 8, 9, 0, 13, 4, 2, 7, 6, 3, 5, 12};
	int size = sizeof(ary) / sizeof(int);

	qsort((void *) ary, size, sizeof(int), comparator);

    
	
	printf("The sorted array is: ");
	for (int i = 0; i < size; i++) {
		printf("%d ", ary[i]);
	}
	printf("\n");

	return 0;
}
