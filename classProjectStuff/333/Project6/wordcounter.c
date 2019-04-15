/* Counts words from a file!!


Owen Goldthwaite
10/28/18
*/

#include <stdio.h>
#include <stdlib.h>
#include <String.h>
#include <ctype.h>
#include "BST.h"

typedef struct WordCountPair
{
    char* word;
    int count;
}WCP;

size_t maxfilelength = 1000;

void countWords(char*);
void readFile(char*);

//Compares the words of two WCPs, used for creating the BST.
int compWCP(void* w1, void* w2)
{
    WCP* wcp1 = (WCP*)w1;
    WCP* wcp2 = (WCP*)w2;
    
    return strcmp(wcp1->word, wcp2->word);
}

//Compares WCPs based on value of count
int compWCPCount(const void* w1, const void* w2)
{
    WCP* wcp1 = *(WCP**)w1;
    WCP* wcp2 = *(WCP**)w2;

    if(wcp1->count != wcp2->count)
        return (wcp1->count > wcp2->count) ? -1 : 1;
    else
        return 0;
}

//Prints a WCP, called through BSTs inorder function
void printWCP(void* w)
{
    WCP* wcp = (WCP*) w;
    printf("%s - %d\n", wcp->word, wcp->count);
}


void readFile(char* fileName)
{
    //Opening file
    FILE *fptr;
    fptr = fopen(fileName, "r");

    //if file wasn't found
    if(fptr == NULL)
    {
        printf("FILE NOT FOUND! Please run again.\n");
        exit(0);
    }
    
    //writing contenst of file to a string
    char str[maxfilelength];
    fgets(str, maxfilelength, fptr);
    fclose(fptr);

    countWords(str);
}

void countWords(char* str)
{
    BST* bst = bst_create();
    
    char* splitStr = strtok(str, " ,.-");
    
    while(splitStr != NULL)
    {
        //Creating WCP with current word as it's word
        splitStr[0] = tolower(splitStr[0]);
        WCP* wcp = malloc(sizeof(WCP));
        wcp->word = splitStr;
        
        //If BST already has the word, then find that node and increment its count value
        if(bst_contains(bst, wcp, compWCP))
        {
            //Getting wcp out of tree
            Node* node = malloc(sizeof(node));
            node = bst_get(bst, wcp, compWCP);
            
            //Incrementing the count of the found WCP
            WCP* toIncrement = (WCP*) node->data;
            toIncrement->count++;
        }
        else
        {
            //If word isnt already there, create a new node with it at count = 1
            wcp->count = 1;
            bst_add(bst, wcp, compWCP);
        }      
        splitStr = strtok(NULL, " ,.-");
    }

    void** array = malloc(sizeof(void*)*bst->size);
    memcpy(array, bst_toArray(bst), sizeof(void*)*bst->size);

    //Sorting array
    qsort(array, bst->size, sizeof(void*), compWCPCount);

    //Printing sorted array
    for(size_t i = 0; i < 20; i++)
        printWCP(array[i]);
    
}

int main(int argc, char* argv[])
{
    char* fileName = argv[1];
    
    readFile(fileName);
    printf("\n");

    return 0;
}

