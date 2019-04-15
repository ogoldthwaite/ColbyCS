/**
 * Looks at how data in different variables is stored in memory
 *
 * Owen Goldthwaite
 * 9/16/18 
 */

#include <stdio.h>
#include <stdlib.h>


int main (int arg, char *argv[]) {
    
    char char1 = 'a';
    short short1 = 10;
    int int1 = 0x01234567;
    long long1 = 1;
    float float1 = 1.0;
    double double1 = 1.0;
    
    unsigned char* ptr = (unsigned char*)&int1;

    for(int i=0;i<sizeof(int);i++) 
        printf("%d: %02X\n", i, ptr[i]);

 
					
  return 0;
}  