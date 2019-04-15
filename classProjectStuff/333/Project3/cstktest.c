/**
 * Test code for Stack 
 *
 * Ying Li
 * 08/01/2016
 */
#include <stdio.h>
#include "cstk.h"

int main (int argc, char **argv) {
	Stack *s = stk_create(CSTK_MAX);
	
	int num;
	printf("Enter number of of ints to add to stack: ");
	scanf("%d", &num); //Simple user input
	
	printf("\nChecking if stack is empty (1 yes, 0 no): %d\n", stk_isEmpty(s));

	int i;
	for(i = 0; i < num; i++) 
	{
		stk_push(s, i);
	} 

	printf("Peeking at top value on stack: %d\n", stk_peek(s));
	printf("Checking if the stack is full (1 yes, 0 no): %d\n", stk_isFull(s)); //Should never really be full
	printf("Checking if stack is empty (1 yes, 0 no): %d\n", stk_isEmpty(s));


	printf("\n\nThe original list: ");
	stk_display(s, 0);

	printf("\nThe reversed list: ");
	stk_display(s, 1);

	
	// for(i = 0; i < 15; i++) 
	// 	printf("Popped: %d\n", stk_pop(s));

	stk_destroy(s);
	
	stk_display(s,0); //should print nothing 
	
	printf("Finished!");
	return 0;
}