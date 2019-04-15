/* LinkedList header file!

Owen Goldthwaite
10/21/18
*/

typedef struct Node Node;

struct Node
{
    Node* next;
    void* val; //arbitrary pointer
};

typedef struct LinkedList
{
    Node* head;
    int size; //size! Incrementing/Decrementing when needed so size function simply returns this value
}LinkedList;

//Functions
LinkedList* ll_create();
void ll_push(LinkedList* list, void* data);
void* ll_pop(LinkedList* list);
void ll_append(LinkedList *list, void* data);
void* ll_remove(LinkedList* list, void* target, int (*compfunc)(void*, void*));
int ll_size(LinkedList* list);
void ll_clear(LinkedList* list, void (*freefunc)(void*));
void ll_map(LinkedList* list, void (*mapfunc)(void*));
void* ll_delete(LinkedList* list, int index); //Extension, removes node in list at given location. Returns removed value
Node* getNode(LinkedList* list, int index); //returns the node at the given index, used to help other functions
void ll_insert(LinkedList* list, void* data, int index);