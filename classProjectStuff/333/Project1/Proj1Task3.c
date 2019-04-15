/**
 * Repeatedly allocates a small amount of memory in a long loop to see what happens!! BAD
 *
 * Owen Goldthwaite
 * 9/16/18 
 */

#include <stdio.h>
#include <stdlib.h>


int main (int arg, char *argv[]) {
    
    int* a; 

    for(;;)
    {
        a = malloc(10); //10 bytes of allocation
        free(a); //Freeing memory stored by a
    }

 
					
  return 0;
}  