/* Precedence of memory operators!

Owen Goldthwaite
10/12/18

*/ 
#include <stdio.h>
#include <stdlib.h>


int main(int argc, char const *argv[])
{
    int a = 3;
    int* b = malloc(sizeof(int));
    *b = 4;

    printf("%d\n",*&b); 
    printf("%d\n", &b);
    printf("%d\n",a>>*b);


    return 0;
}
