/*
	Bruce Maxwell
	Fall 2012
	CS 333

	Linked list test function
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "linkedlist.h"

// function that prints an integer
void printInt(void *i) {
	int *a = (int *)i;

	printf("value: %d\n", *a);
}

// function that prints a char
void printFloat(void* c) 
{
	float *a = (float*) c;
	printf("float: %f\n", *a);
}

// function that squares an integer
void squareInt(void *i) {
	int *a = (int *)i;

	*a = *a * *a;
}

// Moves char value up one
void squareFloat(void* c)
{
	float *a = (float*) c;

	*a = *a * *a;
}

// function that compares two integers and returns 1 if they are equal
int compInt(void *i, void *j) {
	int *a = (int *)i;
	int *b = (int *)j;

	return(*a == *b);
}

int compFloat(void *i, void* j)
{
	float *a = (float *)i;
	float *b = (float *)j;

	return(*a == *b);
}

// test function for the various linked list functions
int main(int argc, char *argv[]) {
	LinkedList *l;
	int *a;
	int *target;
	int i;

	// create a list
	l = ll_create();

	// push data on the list
	for(i=0;i<20;i+=2) {
		a = malloc(sizeof(int));
		*a = i;

		ll_push(l, a);
	}

	// printing the list and testing map
	printf("After initialization\n");
	ll_map(l, printInt);

	ll_map(l, squareInt);

	printf("\nAfter squaring\n");
	ll_map(l, printInt);

	// testing removing data
	target = malloc(sizeof(int));

	*target = 16;
	a = ll_remove(l, target, compInt);
	if(a != NULL)
		printf("\nremoved: %d\n", *a);
	else
		printf("\nNo instance of %d\n", *target);

	*target = 11;
	a = ll_remove(l, target, compInt);
	if(a != NULL)
		printf("\nremoved: %d\n", *a);
	else
		printf("\nNo instance of %d\n", *target);

	printf("\nAfter removals\n");
	ll_map(l, printInt);

	// testing appending data
	ll_append(l, target);

	printf("\nAfter append\n");
	ll_map(l, printInt);

	// test clearing
	ll_clear(l, free);

	printf("\nAfter clear\n");
	ll_map(l, printInt);

	// rebuild and test append and pop
	for(i=0;i<5;i++) {
		a = malloc(sizeof(int));
		*a = i;
		ll_append(l, a);
	}

	printf("\nAfter appending\n");
	ll_map(l, printInt);

	a = ll_pop(l);
	printf("\npopped: %d\n", *a);
	free(a);

	a = ll_pop(l);
	printf("popped: %d\n", *a);
	free(a);

	printf("\nAfter popping\n");
	ll_map(l, printInt);

	printf("\nList size: %d\n", ll_size(l) );

	//NOW CHAR TESTING
	printf("\n--USING FLOATS NOW--\n");
	LinkedList *list;
	// create a list
	list = ll_create();

	// push data on the list
	float x = 1.1;
	float y = 1.2;
	float z = 1.3;

	float* b = (float*) malloc(sizeof(float));
	float* c = (float*) malloc(sizeof(float));
	float* d = (float*) malloc(sizeof(float));
	b = &x;
	c = &y;
	d = &z;
	ll_push(list, b);
	ll_push(list, c);
	ll_push(list, d);

	// printing the list and testing map
	printf("After initialization\n");
	ll_map(list, printFloat);

	ll_map(list, squareFloat);

	printf("\nAfter changing\n");
	ll_map(list, printFloat);

	float o = 1.2 * 1.2;
	float* tar = (float*) malloc(sizeof(float));
	tar = &o;
	float* u = malloc(sizeof(float));
	u = ll_remove(list, tar, compFloat);
	if(u != NULL)
		printf("\nremoved: %f\n", *u);
	else
		printf("\nNo instance of %f\n", *tar);

	printf("\nAfter Removal\n");
	ll_map(list, printFloat);

	// testing appending data
	ll_append(list, c);

	printf("\nAfter append\n");
	ll_map(list, printFloat);

	printf("\nTesting Size Pre-Pop\n");
	printf("size: %d\n", ll_size(list));

	printf("\nTesting Pop\n");

	u = ll_pop(list);
	printf("\npopped: %f\n", *u);
	free(u);

	u = ll_pop(list);
	printf("\npopped: %f\n", *u);
	free(u);

	printf("\nRemaining after pops\n");
	ll_map(list, printFloat);

	printf("\nTesting Size Post-Pop\n");
	printf("size: %d\n", ll_size(list));

	ll_push(list, b);
	ll_push(list, c);
	ll_push(list, d);

	printf("\nCreating longer list to test insert..\n");
	ll_map(list, printFloat);

	float lit = 6.9;
	float af = 4.20;
	float fam = 13.37;

	b = &lit;
	c = &af;
	d = &fam;

	ll_insert(list, b, 2);
	ll_insert(list, c, 3);
	ll_insert(list, d, 2);


	printf("\nList Post Inserts\n");
	ll_map(list, printFloat);

	return(0);
}