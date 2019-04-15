/*
    Memory management fun stuff in C!

    Owen Goldthwaite
    11/11/18
*/

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

long long getMS();



int main(int argc, char const *argv[])
{
    //memory sizes
    size_t small;
    printf("Enter a size for small allocation: \n");
    scanf("%d", &small);

    size_t med;
    printf("Enter a size for med allocation: \n");
    scanf("%d", &med);

    size_t large;
    printf("Enter a size for large allocation: \n");
    scanf("%d", &large);

    //Count!
    float count;
    printf("Enter count of allocations: \n");
    scanf("%f", &count);
    
    //small memory amount
    long time = getMS();

    for(size_t i = 0; i < count; i++)
    {
        void* a;
        a = malloc(small);
    }

    int timetaken = getMS() - time;
    printf("Time Taken for all small allocations: %d ms\n", timetaken);
    float avgper = timetaken / count;
    printf("Average time per allocation: %f ms\n\n", avgper);


    //med memory amount
    time = getMS();

    for(size_t i = 0; i < count; i++)
    {
        void* a;
        a = malloc(med);
    }

    timetaken = getMS() - time;
    printf("Time Taken for all medium allocations: %d ms\n", timetaken);
    avgper = timetaken / count;
    printf("Average time per allocation: %f ms \n\n", avgper);


    //large memory amount
    time = getMS();

    for(size_t i = 0; i < count; i++)
    {
        void* a;
        a = malloc(large);
    }

    timetaken = getMS() - time;
    printf("Time Taken for all large allocations: %d ms\n", timetaken);
    avgper = timetaken / count;
    printf("Average time per allocation: %f ms\n\n", avgper);
    
    return 0;
}

long long getMS() //Gets current time!
{
    struct timeval tv;

    gettimeofday(&tv,NULL);
    return (((long long)tv.tv_sec)*1000)+(tv.tv_usec/1000);
}