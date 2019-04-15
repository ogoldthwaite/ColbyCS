/* cstack header file for declaring stuff!

   Owen Goldthwaite
   9/30/18
*/
#include <stdbool.h>

typedef struct stack {
		int* stack;
		int top;
	} Stack;

extern size_t CSTK_MAX;

Stack* stk_create(int);
void stk_destroy(Stack*);
void stk_push(Stack*, int);
int stk_pop(Stack*);
void stk_display(Stack*, int);
int stk_peek(Stack*);
bool stk_isFull(Stack*);
bool stk_isEmpty(Stack*);