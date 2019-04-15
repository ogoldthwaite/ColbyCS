/* Task 2.2, C seg fault signal handler!


Owen Goldthwaite
10/28/18
*/
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
    

void segHandler(int num)
{
    fprintf(stderr, "UH OH! A SEG-FAULT!\n");
    exit(num);
}

void dostuff()
{
    signal(SIGSEGV, segHandler);
    
    char* str = "oof";
    str[0] = 'z'; //Seg-fault caused here
}

int main(int argc, char const *argv[])
{
    dostuff();

    return 0;
}
