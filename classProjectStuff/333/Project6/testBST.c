/* Binary Search Tree test file


Owen Goldthwaite
10/28/18

*/
#include <stdio.h>
#include <stdlib.h>
#include "BST.h"

int compInt(void *i, void *j) {
	int *a = (int *)i;
	int *b = (int *)j;

	if(*a != * b)
        return (*a < * b) ? -1 : 1;
    else
        return 0;
}

void printInt(void* val)
{
    int* num = (int*)val;
    printf("%d \n", *num);
}

int main(int argc, char const *argv[])
{
    
    BST* bst = bst_create();

    int* num = malloc(sizeof(int));
    *num = 5;
    bst_add(bst, num, compInt);

    int* num1 = malloc(sizeof(int));
    *num1 = 2;
    bst_add(bst, num1, compInt);

    int* num2 = malloc(sizeof(int));
    *num2 = 8;
    bst_add(bst, num2, compInt);

    int* numNo = malloc(sizeof(int));
    *numNo = 8;

    // Node* node = malloc(sizeof(Node));
    // node = bst_get(bst, numNo, compInt);

    // int* num3 = malloc(sizeof(int));
    // num3 = (int*) node->data;
    // printf("%d\n", *num3);

    printf("%d\n", bst_contains(bst, numNo, compInt));
    
    printf("\n");
    bst_inorder(bst, printInt);


    return 0;
}
