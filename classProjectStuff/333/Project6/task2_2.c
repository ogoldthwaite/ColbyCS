/* Task 2.2, C floating point signal handler


Owen Goldthwaite
10/28/18
*/
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
    
int a = 5;
int b = 0;

void fpeHandler(int num)
{
    fprintf(stderr, "Floating Point Exception!\n");
    b = 5;
    dostuff();
}

void dostuff()
{
    signal(SIGFPE, fpeHandler);
    
    printf("%d\n", a / b);

    printf("hey\n");
}

int main(int argc, char const *argv[])
{
    dostuff();

    return 0;
}
