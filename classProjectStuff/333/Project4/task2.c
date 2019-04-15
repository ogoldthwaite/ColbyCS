/* Factorial Thing!


    Owen Goldthwaite
    10/7/18

*/
#include <stdio.h>
#include <stdlib.h>

int factorial(int);

int main(int argc, char const *argv[])
{
    int val = 0;

    printf("Enter a number to find the factorial of: ");
	scanf("%d", &val); 

    int (*calc)(const int) = factorial;
    
    printf("%d", calc(val));
    
    return 0;
}

//finds factorial of num and returns it
int factorial(int num)
{
    int toReturn = num;

    for(size_t i = num-1; i > 0 ; i--)
        toReturn *= --num;

    return toReturn;
}
