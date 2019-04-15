/*
    Memory management fun stuff in C!

    Owen Goldthwaite
    11/11/18
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>

long long getMS();

int main(int argc, char const *argv[])
{
    float count;
    printf("Enter count of allocations/frees: \n");
    scanf("%f", &count);

    int yesno;
    printf("Do you want to use a fixed allocation size or random one? Enter 1 for fixed, 0 for random: \n");
    scanf("%d", &yesno);

    size_t memsize;
    if(yesno == 1)
    {
        printf("Enter a size for base memory allocation: \n");
        scanf("%d", &memsize);
    }
    else
        srand(time(NULL));

    long time = getMS();

    for(size_t i = 0; i < count; i++)
    {
        void* a;
        if(yesno == 1)
            a = malloc(memsize);
        else
            a = malloc(rand());

        free(a);
    }
    
    int timetaken = getMS() - time;
    printf("\nTime Taken for all allocations and frees: %d ms\n", timetaken);
    float avgper = timetaken / count;
    printf("Average time per allocation and free: %f ms\n\n", avgper);


    printf("\nNow testing if allocating the same amount of memory will take longer after calling free and alloc a lot\n");
    time = getMS();


    for(size_t i = 0; i < count; i++)
    {
        void* a;
        if(yesno == 1)
            a = malloc(memsize);
        else
            a = malloc(rand());

        free(a);
    }

    timetaken = getMS() - time;
    printf("\nTime Taken for all allocations: %d ms\n", timetaken);
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