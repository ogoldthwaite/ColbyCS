/* C linked list!

-Owen Goldthwaite
10/21/18
*/
#include <stdio.h>
#include <stdlib.h>
#include "linkedlist.h"


LinkedList* ll_create()
{
    LinkedList* list = (LinkedList*) malloc(sizeof(LinkedList));
    list->size = 0;
    
    return list;
}

Node* getNode(LinkedList* list, int index)
{
    if(index <= 0)
        return list->head;
    
    Node* tempNode = list->head;
    
    for(size_t i = 0; i < index; i++)
        tempNode = tempNode->next;

    return tempNode;
}

//EXTENSION, removes node in list at given location. Returns removed value
void* ll_delete(LinkedList* list, int index)
{
    void* toReturn;

    if(index <= 0) //removes head if value is invalid
    {
        Node* toRemove = list->head;
        toReturn = toRemove->val;
        list->head = toRemove->next;
        free(toRemove);
    }
    else
    {
        Node* prevNode = getNode(list, index-1);
        Node* toRemove = prevNode->next;
        //Node* toRemove = getNode(list, index);
        toReturn = toRemove->val;
        prevNode->next = toRemove->next; //Pointer of previous node is now current nodes next, no pointer in list to removed node anymore
        free(toRemove);
    }

    list->size--;
    return toReturn;
}

void ll_push(LinkedList* list, void* data)
{
    Node* newNode = (Node*) malloc(sizeof(Node));
    newNode->val = data;
    newNode->next = list->head;
    list->head = newNode;
    list->size++;
}

void* ll_pop(LinkedList* list)
{
    void* toReturn = list->head->val;
    Node* prevHead = list->head;
    list->head = prevHead->next;
    free(prevHead);

    list->size--;
    return toReturn;
}

void ll_append(LinkedList* list, void* data)
{
    if(ll_size(list) == 0) //if list is empty
    {
        list->head = (Node*) malloc(sizeof(Node));
        list->head->val = data;
    }

    Node* tail = getNode(list, ll_size(list)-1); //size call isn't necessary with current implementation, but safer for future change
    Node* newNode = (Node*) malloc(sizeof(Node));
    newNode->val = data;
    tail->next = newNode;
    list->size++;
}

//Extension: Insert adds value into the list at the given index
void ll_insert(LinkedList* list, void* data, int index)
{
    if(ll_size(list) == 0) //if list is empty
    {
        list->head = (Node*) malloc(sizeof(Node));
        list->head->val = data;
    }

    Node* prevNode = getNode(list, index);
    Node* nextNode = prevNode->next;
    Node* newNode = malloc(sizeof(Node));
    newNode->val = data;
    prevNode->next = newNode;
    newNode->next = nextNode;

    list->size++;
}

//returns NULL if nothing was found
void* ll_remove(LinkedList* list, void* target, int (*compfunc)(void*, void*))
{
   void* toReturn = NULL;
   Node* curNode = list->head;
 
   for(size_t i = 0; i < ll_size(list); i++)
   {
       //ASK ABOUT THIS IN CLASS, COMPARATOR FUNCTIONS RETURN 0 FOR EQUAL NORMALLY, RIGHT??
       if(compfunc(curNode->val, target) != 0) //if target and current val are eqaul
       {
            toReturn = ll_delete(list, i); //deletes node at current index
            break;
       }
       else
            curNode = curNode->next;
   }
   
   //size--; //Size is decremented in delete function!!
   return toReturn;
}

void ll_clear(LinkedList* list, void (*freefunc)(void*))
{
     Node* curNode = (Node*) malloc(sizeof(Node));
     Node* nextNode = (Node*) malloc(sizeof(Node));

     curNode = list->head;

    for(size_t i = 0; i < ll_size(list); i++)
    {
        nextNode = curNode->next;
        freefunc(curNode->val);
        free(curNode);
        curNode = nextNode;
    }

    list->size = 0;
}

void ll_map(LinkedList* list, void (*mapfunc)(void*))
{
    Node* curNode = list->head;
    int size = ll_size(list);

    for(size_t i = 0; i < size; i++)
    {
        mapfunc(curNode->val);
        curNode = curNode->next;
    }

}

int ll_size(LinkedList* list)
{
    // int size = 0;
    // Node* curNode = list->head;

    // while(curNode != NULL)
    // {
    //     size++;
    //     curNode = curNode->next;
    // }
    return list->size;
}


// int main(int argc, char const *argv[])
// {
//     LinkedList* list = ll_create();   
//     ll_push(list, (void*) 1);
//     ll_push(list, (void*) 2);
//     ll_push(list, (void*) 3);
//     ll_push(list, (void*) 4);
//     ll_append(list, (void*) 5);
//     printf("PRE: %d\n", getNode(list, 3)->val);
//     ll_delete(list, 3);
//     printf("POST: %d\n", getNode(list, 3)->val);
//     // printf("%d\n", ll_pop(list));
//     // printf("%d\n", ll_pop(list));

//     printf("Size: %d", ll_newSize());

//    // printf("Size: %d", ll_size(list));
//     return 0;
// }
