/**
 * Trying to overwrite a decision variable in a function with a long string
 *
 * Owen Goldthwaite
 * 9/16/18 
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct stringThing
{
    char str[4];
    int num;
};

//assigns oof (a long string) to thing.str to try and affect the value of num
void rip(struct stringThing thing, char oof[]) 
{
    strcpy(thing.str, oof);
    
    if(thing.num == 0) //if thing.num has had it's value changed
        printf("Safe\n");
    else
        printf("Hacked\n");
}

int main (int arg, char *argv[]) {
    
     struct stringThing lol = {"bbbb", 0};
     printf("size of structure in bytes : %d\n", sizeof(lol));

     int* a = malloc(sizeof(lol)); //allocating the struct

     printf("Enter a string to test: ");
     char name[0];
     fgets(name,10,stdin);
     //printf("%s\n", name);
     rip(lol,name); //String parameter here will break if over 4 chars, since struct asks for a 4 length string
				
  return 0;
}  