CS333 Project 5 - README
Owen Goldthwaite

Project5.
    C:.
        clltest.c
        funcll.c
        funcll.h
        funcllTest.c
        linkedlist.c                 
        linkedlist.h
        README.txt

C: 
    --Task 1--

        File Name: linkedlist.c 
        Compile/Run: -gcc -o clltest clltest.c linkedlist.c 
                     -./clltest
        
        Input: None!
        Output: A lot of stuff showing different tests of the different linkedlist functions. Starting with testing ints and then testing
        chars.

        EXTENSIONS:

        1. I made the delete function called ll_delete(LinkedList list*, int index). It deletes the node at the given index and updates the
        pointers of other nodes to make sure the list is still a list then returns the value of the deleted node. I don't have an explicit test
        function to test it since I actually use it as part of my required ll_remove() function. So if ll_remove() works properly, which as of 
        writing this it does, then ll_delete() must work properly. 

        2. I added the functionality of the simple helper function getNode(LinkedList list, int index). It loops through the list and returns
        the node at the given index. Creating this let me significantly simplify many other functions. It makes functions much easier to implement
        and if very useful. Again I don't have an explicit test for it but as long as everything else is working it has to be working.

        3. Made the ll_insert() function which takes a list, a value and an index as parameters. When called it adds the passed in value into the list at
        the given index. It uses getNode() to find the location in the list. And I added some tests for it at the end of the clltest.c file. 

        4. I remade mose of the LinkedList in a more functional way. It's not completely solely functional, but it is definitely far more functional than
        the original linkedlist.c. It used a lot of recursion and I did my best to eliminate any non-functional statements. For the most part I was
        pretty successful, but at certain times it would've been far more work to do than it's worth. Certain things I also left in for safety measures.
        Size for example is one of these, I never use it but just in case I did I just incremented/decremented in when needed, not functionally.
        
        Making it more functional made some functions so much easier to write, for example ll_push. Barring the boundry testing and size increment I have in the function
        it is really only one line: 
        
        list->head = createNode(list->head, data); 

        Sure it's an assignment, but this psuedo-functional semi-complete linked list isn't perfect!! I implemented and tested the following functions:
        ll_pop, ll_push, ll_append, ll_delete, ll_remove, ll_map, ll_create. Of course there are far more functions to help make those ones work, but those are the 
        ones another user would use. Also it could be polymorphic just like the other list since it also uses void*, but I only wrote test code for ints.

        The linkedlist file is called funcll.c, with header funcll.h and test file funcllTest.c. 

        File Name: funcll.c 
        Compile/Run: -gcc -o funcllTest funcllTest.c funcll.c 
                     -./funcllTest
        
        Input: None!
        Output: A lot of stuff showing different tests of the different linkedlist functions. Testing integers! 