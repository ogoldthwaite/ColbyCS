/* C functional linked list!

-Owen Goldthwaite
10/21/18
*/
#include <stdio.h>
#include <stdlib.h>
#include "funcll.h"

Node* createNode(Node* next, void* value) //creates a new node with the next pointer and value value 
{
    return createNodeHelper( (Node*)malloc(sizeof(Node)), next, value );
}

Node* createNodeHelper(Node* node, Node* next, void* value) //assigns values and returns node
{
    node->val = value;
    node->next = next;
    return node;
}

LinkedList* ll_create() //Could be done functionally, but for simplicities sake this will remain the same
{
    LinkedList* list = (LinkedList*) malloc(sizeof(LinkedList));
    list->size = 0; //For now size is not going to be functional.
    list->head = (Node*) malloc(sizeof(Node));
    list->head->next = NULL;

    return list;
}

void ll_push(LinkedList* list, void* data)
{
    if(list->size == 0) //If list is empty
        list->head->val = data;
    else
        list->head = createNode(list->head, data);
    
    list->size++;
}

void* ll_pop(LinkedList* list)
{
    return popHelper(list);
}

void* popHelper(LinkedList* list) //returns value of head and calls updateToNext on head
{
    list->size--;
    void* totallyNotATempVar = list->head->val;
    list->head = updateToNext(list->head);
    return totallyNotATempVar;
}

Node* updateToNext(Node* node) //Makes node passed in the next node
{
    node = node->next;
    return node;
}

void ll_append(LinkedList* list, void* data) //appends to end
{
    if(list->size == 0) //If list is empty
        list->head->val = data;
    else
        appendHelper(list->head, data); 
    
    list->size++; //Size increment
}

void appendHelper(Node* node, void* data) //recursively goes through list and appends new node with value to end
{
    if(node->next == NULL) //If there is no next node
        node->next = createNode(NULL, data); //Create a new node with value data at current nodes next pointer and assign new node next to null
    else
        appendHelper(node->next, data); //Call appendHelper again with next node

}

void* ll_delete(LinkedList* list, int index)
{
    list->size--;
    if(index == 0) //If trying to delete first thing in list, not too functional!
    {
        void* totallyNotATempVar = list->head->val; //returning this value, sadly not functional!
        list->head = updateToNext(list->head);
        return totallyNotATempVar;
    }

    return (deleteHelper(list->head, 0, index))->val;
}

Node* deleteHelper(Node* node, int count, int index) //loops through list and deletes node once count reaches index
{
    if(count >= (index-1) )
    {
        node->next = updateToNext(node->next);
        return node;
    }
    else
        deleteHelper(node->next, count + 1, index);
}

void ll_map(LinkedList* list, void (*mapfunc)(void*))
{
    mapHelper(list->head, mapfunc);
}

void mapHelper(Node* node, void (*mapfunc)(void*))
{
    if(node == NULL)
        return;
    else
    {
        mapfunc(node->val);
        mapHelper(node->next, mapfunc);
    }
}

void* ll_remove(LinkedList* list, void* target, int (*compfunc)(void*, void*))
{
    list->size--;
    return removeHelper(list->head, target, compfunc, 0);
}

void* removeHelper(Node* node, void* target, int (*compfunc)(void*, void*), int curIndex)
{
    if(compfunc(node->next->val, target) != 0)
        return (deleteHelper(node, 0, 0))->val; //deletes the node sent in sinze count == index from the start
    else
        return removeHelper(node->next, target, compfunc, curIndex + 1);
}
