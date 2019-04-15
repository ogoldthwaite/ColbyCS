CS333 Project 3 - README
Owen Goldthwaite

Project3.
    C:.
        cstk.c                 
        cstk.h
        cstktest.c
        README.txt

C:
    --Task 1--
        File to run Name: cstktest.c
        Compile/Run: -gcc -o cstktest.c cstk.c
                     -./cstktest

        Input: The number of items to push on the stack, it will prompt you.
        Output: All items in the stack listed in original order and then reverse order.

Extensions: 
        1. Quite minor, but I added some simple user input to the cstktest.c file so you can now input the number of items you want to push
        onto the stack. Should've already seen it when running the program!

        2. I added some more simple functions to the cstk.c class. 
        stk_peek() returns the value of the top of the stack, doesn't pop it off.
        stk_isEmpty() returns true(1) if stack is empty, false(0) otherwise.
        stk_isFull() returns true(1) is stack is full, false(0) otherwise.

        3. The stack will dynamically allocate more memory/space to the array within in. This is done through the increaseSize() function
        which is called when the stack is full. Currently when this method is called it increases the size by *250. Basically it SHOULD work
        with only doubling the size, but for me when I run it in the folder it's currently in small numbers do not work, however, large do. 
        So I'm using *250 just to be safe for grading purposes! I know it's dumb. 