/* Task 2.1, C interrupt signal handler


Owen Goldthwaite
10/28/18
*/
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

void exitProgram(int num)
{
    printf("Interrupted!! \n");
    exit(num);
}


int main(int argc, char const *argv[])
{
    signal(SIGINT, exitProgram);

    while(1) { ; }
    
    return 0;
}
