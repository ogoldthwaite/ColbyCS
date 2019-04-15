/* Task 1 C using threads to sort an array!

Owen Goldthwaite
12/2/18
*/

#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <time.h>
#include <string.h>
#include <sys/time.h>

long long getMS();

typedef struct ThreadInfo //stores part of array and index of thread in case I need it!
{
    void** array;
    int index;
    int arrsize;
    int (*compfunc)(const void* a, const void* b);
}ThreadInfo;

int* mergetwo (int* t1, int* t2, int c1, int c2);


int intcomp(const void* a, const void* b)
{
    return ( *(int*)a - *(int*)b );
}

void* tSort(void* args)
{
    ThreadInfo* tinfo = (ThreadInfo*) args;

    qsort(tinfo->array, tinfo->arrsize, sizeof(tinfo->array[0]), tinfo->compfunc);
}

int main(int argc, char const *argv[])
{
    size_t threadcount;
    printf("Enter a number of threads: \n");
    scanf("%d", &threadcount);

    size_t arraysize;
    printf("Enter size of the array: \n");
    scanf("%d", &arraysize);

    int typenum;
    printf("Enter 1 for ints, 2 for floats: \n");
    scanf("%d", &typenum);

    void* type;
    if(typenum == 1)
    {
        int* a = malloc(sizeof(int));
        type = a;
    }
    else
    {
        float* a = malloc(sizeof(float));
        type = a;
    }

    ThreadInfo* tinfos[threadcount];
    pthread_t threads[threadcount];

    srand(time(0));
    int arrsize = arraysize;
    void** array = malloc(arrsize * sizeof(*type));
    size_t tinfoarrsize = arrsize / threadcount;   

    
    for(size_t i = 0; i < threadcount; i++) //Initializing the thread structs
    {
       ThreadInfo* tinfo = (ThreadInfo*) malloc(sizeof(ThreadInfo));
       tinfo->array = (void**) malloc(tinfoarrsize * sizeof(int)); //CHANGE FROm INT LATER
       tinfo->index = i;
       tinfo->arrsize = tinfoarrsize;
       tinfo->compfunc = intcomp;
       tinfo->array[arrsize];

       tinfos[i] = tinfo;
    }

    int count = 0;
    int done = 0;
    srand(time(0));
    for(size_t i = 0; i < arrsize; i+=tinfoarrsize)
    {
        if(done) //makes sure doesnt loop over total size which causes issues
            break;

        ThreadInfo* tinfo = tinfos[count++];     

        int size;
        if(count == threadcount) //another boundry check thing
        {
            size = (arrsize - i)-1;
            done = 1;
            tinfo->arrsize = size;
        }
        else
            size = tinfoarrsize;
        
        for(size_t j = 0; j < size; j++) //creating array segments and full array
        {
            int num = rand() % 1000;
            tinfo->array[j] = (void*)num;
            array[i+j] = (void*)num;
        }
    }
   
    long curtime = getMS();

    for(size_t i=0; i < threadcount; i++) //running threads
        pthread_create(&(threads[i]), NULL, tSort, (tinfos[i]) );

    for(size_t i=0; i < threadcount; i++) //joining threads
        pthread_join( threads[i], NULL );

  
    if(threadcount > 1)
    {     
        int* total = malloc(arrsize * sizeof(int));
        int start = 0;
        for(size_t i = 0; i < count; i++)
        {
           ThreadInfo* curinfo = tinfos[i];
           memcpy(total + start, curinfo->array, curinfo->arrsize * sizeof(curinfo->array[0]));
           start += curinfo->arrsize;
        }
        qsort(total,arrsize, sizeof(total[0]), tinfos[0]->compfunc);

        
        for(size_t i = 0; i < arrsize; i++)
        {
            printf("val: %d\n", total[i]);
        }
        

        // int* test = malloc(arrsize*sizeof(int));
        // test = mergetwo(tinfos[0]->array, tinfos[1]->array, tinfos[0]->arrsize, tinfos[1]->arrsize);

        // for(size_t i = 2; i < threadcount-1; i++)
        // {
        //     test = mergetwo(test, tinfos[i]->array, tinfoarrsize * i, tinfos[i]->arrsize);   
        // }

    }

    printf("Time Taken for Threads: %ld ms\n", getMS() - curtime);

    curtime = getMS();

    qsort(array, arrsize, sizeof(array[0]), tinfos[0]->compfunc);

    printf("Time Taken for Normal: %ld ms", getMS() - curtime);

    return 0;
}


long long getMS() //Gets current time!
{
    struct timeval tv;

    gettimeofday(&tv,NULL);
    return (((long long)tv.tv_sec)*1000)+(tv.tv_usec/1000);
}

int* mergetwo (int* a, int* b, int c1, int c2)
{
    int size1 = c1;
    int size2 = c2;
    // int* a = malloc(sizeof(int) * m);
    // int* b = malloc(sizeof(int) * n);
    // a = t1->array;
    // b = t2->array;
    
    int i=0;
    int j=0;

    int* list = (int*) malloc((size1+size2) * sizeof(int));
    int curindex = 0;

    while(i < size1 && j < size2)
    {
        if(a[i] <= b[j])
        {
            list[curindex++] = a[i];
            i++;
        }
        else
        {
            list[curindex++] = b[j];
            j++;
        }
    }

    while(i < size1)
    {
        list[curindex++] = a[i];
        i++;
    }

    while(j < size1)
    {
        list[curindex++] = a[j];
        j++;
    }

    // ThreadInfo* toReturn = malloc(sizeof(ThreadInfo));
    // toReturn->arrsize = curindex;
    // toReturn->array = list;

    return list;

}