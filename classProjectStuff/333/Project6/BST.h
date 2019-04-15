/* Header file for binary search tree!


Owen Goldthwaite
10/28/18
*/

typedef struct Node Node;

struct Node
{
    Node* right;
    Node* left; 
    void* data;
};

typedef struct BST
{
    Node* root;
    size_t size;
}BST;

BST* bst_create();
void bst_inorder(BST* bst, void printfunc(void*));
void inorderHelper(Node* node, void printfunc(void*));
void bst_add(BST* bst, void* data, int (*compfunc)(void*, void*));
Node* addHelper(Node* node, void* data, int (*compfunc)(void*, void*));
Node* bst_get(BST* bst, void* target, int (*searchfunc)(void*, void*));
Node* getHelper(Node* node, void* target, int (*searchfunc)(void*, void*));
int bst_contains(BST* bst, void* target, int (*searchfunc)(void*, void*));
int containsHelper(Node* node, void* target, int (*searchfunc)(void*, void*));
void* bst_toArray(BST* bst);
int toArrayHelper(Node* node, void* array[], int curIndex);
