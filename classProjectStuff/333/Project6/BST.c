/* Binary Search tree for use in project 6. EXTENSION


Owen Goldthwaite
10/28/18
*/
#include <stdio.h>
#include <stdlib.h>
#include "BST.h"


BST* bst_create()
{
    //Creating bst struct
    BST* bst = (BST*) malloc(sizeof(BST));
    bst->root = (Node*) malloc(sizeof(Node));
    bst->root->data = malloc(sizeof(void*));
    bst->root->data = NULL;
    bst->root = NULL;
    bst->size = 0;

    return bst;
}

//Creates a node with the given right, left and data
Node* createnode(Node* right, Node* left, void* data)
{
    Node* node = (Node*)malloc(sizeof(Node));
    node->right = (Node*)malloc(sizeof(Node));
    node->left = (Node*)malloc(sizeof(Node));
    node->right = right;
    node->left = left;
    node->data = data;
    return node;
}

//Prints the BST inorder using the given print function
void bst_inorder(BST* bst, void printfunc(void*))
{
    inorderHelper(bst->root, printfunc);
}

void inorderHelper(Node* node, void printfunc(void*))
{
    if(node != NULL)
    {
        inorderHelper(node->left, printfunc);
        printfunc(node->data);
        inorderHelper(node->right, printfunc);
    }
}

//Adds a node to the tree at the proper location based upon the nodes future data value.
void bst_add(BST* bst, void* data, int (*compfunc)(void*, void*))
{
    //Check if root is empty, may change to a size check. Probably pointless ;) 
    if(bst->root == NULL)
        bst->root = createnode(NULL, NULL, data);
    else
        addHelper(bst->root, data, compfunc);

    bst->size++;
}

Node* addHelper(Node* node, void* data, int (*compfunc)(void*, void*))
{
    if(node == NULL)
        return createnode(NULL, NULL, data);

    if(compfunc(data, node->data) < 0)
       node->left = addHelper(node->left, data, compfunc);
    else if (compfunc(data, node->data) >= 0)
        node->right = addHelper(node->right, data, compfunc);

    return node;

}

//Finds the node with the given target, equality is based upon search function
Node* bst_get(BST* bst, void* target, int (*searchfunc)(void*, void*))
{
    if(bst->root == NULL)
        return NULL;
    else
        return getHelper(bst->root, target, searchfunc);

    return NULL;
}

Node* getHelper(Node* node, void* target, int (*searchfunc)(void*, void*))
{
    if(node == NULL)
        fprintf(stderr, "ERROR: Node with value located at %x was not in tree. CRASHING", &target );
    
    if(searchfunc(target, node->data) == 0)
        return node;
    
    if(searchfunc(target, node->data) < 0)
        return getHelper(node->left, target, searchfunc);
    else if(searchfunc(target, node->data) > 0)
        return getHelper(node->right, target, searchfunc);
}

//Like get but just returns a true/false value if node with given target value is present
int bst_contains(BST* bst, void* target, int (*searchfunc)(void*, void*))
{
    if(bst->root == NULL)
        return 0;
    else
        return containsHelper(bst->root, target, searchfunc);

    return 0;
}

int containsHelper(Node* node, void* target, int (*searchfunc)(void*, void*))
{
    if(node == NULL)
        return 0;
    
    if(searchfunc(target, node->data) == 0)
        return 1;
    
    if(searchfunc(target, node->data) < 0)
        return containsHelper(node->left, target, searchfunc);
    else if(searchfunc(target, node->data) > 0)
        return containsHelper(node->right, target, searchfunc);
}

//Returns an array of all Node->data in the BST. 
void* bst_toArray(BST* bst)
{
    void* array = malloc(sizeof(void*)*bst->size);
    toArrayHelper(bst->root, array, 0);
    return array;
}

int toArrayHelper(Node* node, void* array[], int curIndex)
{
    if(node == NULL)
        return curIndex;

    array[curIndex] = node->data;
    curIndex++;

    if(node->left != NULL)
        curIndex = toArrayHelper(node->left, array, curIndex);
    if(node->right != NULL)
        curIndex = toArrayHelper(node->right, array, curIndex);
        
    return curIndex; 
}