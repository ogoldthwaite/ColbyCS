/* cstack library file!

   Owen Goldthwaite
   9/30/18
*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>
#include "cstk.h"

void increaseSize(Stack*);

size_t CSTK_MAX = 50;

typedef struct testStruct{
    int* array;
}TestArray;

//creates a stack with num as the initial size of the array
Stack* stk_create(int size)
{
    Stack* stkPtr = (Stack*) malloc(sizeof(Stack)); //allocating memory for stack structure
    stkPtr->top = -1; 
    stkPtr->stack = (int*) malloc(size * sizeof(int)); //allocating memory for the array in the stack struct

    return stkPtr; //pointer to the stack
}

//Deleting stack be reallocating it to have 0 bytes of memory to use
void stk_destroy(Stack* stkPtr)
{
     free(stkPtr->stack);
     stkPtr->top = -1;
}

//Extension, returns true if stack is full, false otherwise
bool stk_isFull(Stack* stkPtr)
{
    return stkPtr->top == CSTK_MAX ? true : false; //redundant ternary statement, but looks cool!
}

//Exentsion, returns true is stack is empty, false otherwise
bool stk_isEmpty(Stack* stkPtr)
{
    return stkPtr->top < 0 ? true : false; //still looks cool all these lines later
}

//increments top value of stack and then sets new top location to val
void stk_push(Stack* stkPtr, int val)
{ 
    stkPtr->stack[++(stkPtr->top)] = val;

    if( stk_isFull(stkPtr) ) //EXTENSION, Increase size of stack if needed!!
    { 
        printf("--ATTEMPTING SIZE INCREASE!!!--\n");
        increaseSize(stkPtr);
        printf("--INCREASE DONE--\n");
    }
}

//Extension increases stack size. Right now it's by *250 because of many reasons that make no sense to mortal beings. It's safer for 
//grading this way!
void increaseSize(Stack* stkPtr) //Extension, Increases stack size.
{
     CSTK_MAX *= 250; 
     int* temp = realloc(stkPtr->stack, CSTK_MAX * sizeof(int));
     free(stkPtr->stack);
     stkPtr->stack = temp;
}

//returns top value of stack and then decreases top by 1
int stk_pop(Stack* stkPtr)
{ 
    return stkPtr->stack[(stkPtr->top)--]; 
}

//Extension, returns the top value of the stack, doesnt change top.
int stk_peek(Stack* stkPtr)
{
    return stkPtr->stack[stkPtr->top]; 
}

//Prints out stack list in reverse if reverse == 1, otherwise prints in order
void stk_display(Stack* stkPtr, int reverse)
{

    if(reverse == 1)
    {
        for(size_t i = stkPtr->top+1; i > 0; i--) //reverse
        {
            printf("%d ", (*stkPtr).stack[i-1]);
        }
    }
    else
    {
        for(size_t i = 0; i < stkPtr->top+1; i++) //normal
        {
            printf("%d ", (*stkPtr).stack[i]);
        }
    }
    printf("\n");

}
