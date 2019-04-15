/**
 * Explores how much memory we can access and what it happens when we end.
 *
 * Owen Goldthwaite
 * 9/16/18 
 */

#include <stdio.h>
#include <stdlib.h>


int main (int arg, char *argv[]) {
    
    int int1 = 0x99999999;
    int int2 = 0xFFFFFFFF;
    
    unsigned char* ptr;
    ptr = (unsigned char*)&ptr;

    for(int i=0;i<__INT_MAX__;i++) 
        printf("%d: %02X\n", i, ptr[i]);

 
					
  return 0;
}  