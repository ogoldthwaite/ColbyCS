/**
 * Checking how structs are allocated in memory.
 *
 * Owen Goldthwaite
 * 9/16/18 
 */

#include <stdio.h>
#include <stdlib.h>

struct stuff //13 bytes of variables, however adds 3 padding bytes at end for 16 bytes to stay consistent
{
    short shortNum; //2 bytes
    char letter1; //1 byte
    char letter2; //1 byte
    float floatynum; //4 bytes
    int number; //4 bytes
    char letter3; //1 byte
};


int main (int arg, char *argv[]) {
    
    struct stuff info = {0xAAAA, 'b', 'c', 1.0, 0x01234567, 'd'};
    printf("size of structure in bytes : %d\n", sizeof(info));

    int* a = malloc(sizeof(info)); //allocating the struct

    unsigned char* ptr;
    ptr = (unsigned char*)&ptr;

    for(int i=0;i<25;i++) 
        printf("%d: %02X\n", i, ptr[i]);


 
					
  return 0;
}  