/**
 * Trys to find the magic float!
 *
 * Owen Goldthwaite
 * 9/20/18 
 */

#include <stdio.h>
#include <stdlib.h>


int main (int arg, char *argv[]) {
    
    float num1 = __FLT_MAX__;
    float num2 = num1 + 1.0;

    printf("%f\n", num1);
    printf("%f\n", num2);

    if(num1 == num2)
        printf("Equal");
    else
        printf("Not Equal");

  return 0;
}  