/* Fucntional LinkedList test file


	Owen Goldthwaite
    10/25/18
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "funcll.h"

void squareInt(void *i) {
	int *a = (int *)i;

	*a = *a * *a;
}

void printInt(void *i) {
	int *a = (int *)i;

	printf("%d, ", *a);
}

int compInt(void *i, void *j) {
	int *a = (int *)i;
	int *b = (int *)j;

	return(*a == *b);
}


int main(int argc, char const *argv[])
{
    LinkedList* list;
    int* num;
    int* oof = malloc(sizeof(int));

    
    list = ll_create();

    
    for(size_t i = 0; i < 4; i++)
    {
        num = malloc(sizeof(int));
        *num = i;
        ll_push(list, num);
    }

    printf("\nAfter Pushing\n");
    ll_map(list, printInt);

    oof = (int*) ll_pop(list);
    printf( "\nValue from popping: %d \n", *oof );

    printf("\nList After Pop\n");
    ll_map(list, printInt);

    for(size_t i = 3; i < 6; i++)
    {
        num = malloc(sizeof(int));
        *num = i;
        ll_append(list, num);
    }

    printf("\nList After Append\n");
    ll_map(list, printInt);

    ll_delete(list, 0);

    printf("\nList After deleting INDEX 0\n");
    ll_map(list, printInt);

    ll_delete(list, 3);
    
    printf("\nList After deleting INDEX 3\n");
    ll_map(list, printInt);

    int* tar = malloc(sizeof(int));
    *tar = 3;

    num = ll_remove(list, tar, compInt);

    printf("\nList After deleting VALUE 3\n");
    ll_map(list, printInt);

    *tar = 0;

    num = ll_remove(list, tar, compInt);

    printf("\nList After deleting VALUE 0\n");
    ll_map(list, printInt);

    oof = (int*) ll_pop(list);
    printf( "\nValue from popping: %d \n", *oof );

    printf("\nList After Pop\n");
    ll_map(list, printInt);




    // bob = (int*) ll_pop(list);
    // printf( "Val: %d \n", *bob );
    // bob = (int*) ll_pop(list);
    // printf( "Val: %d \n", *bob );
    // bob = (int*) ll_pop(list);
    // printf( "Val: %d \n", *bob );




    return 0;
}
