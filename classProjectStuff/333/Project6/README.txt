CS333 Project 6 - README
Owen Goldthwaite

Project6.
    C:.
        BST.c
        BST.h
        README.txt
        task2_1.c
        task2_2.c                
        task2_3.c
        test.txt
        testBST.c
        wordcounter.c

OS: Windows 10
gcc: gcc (MinGW.org GCC-6.3.0-1) 6.3.0

C: 
    --Task 1--
        
        File Name: wordcounter.c 
        Compile/Run -gcc -o wordcounter wordcounter.c BST.c
                    -./wordcounter test.txt

                    Input: Name of text file as command line argument, currently test.txt is the one given.
                    Output: The top 20 most common words in the file will be printed with count and word shown. Descending order.

                    The file is called wordcounter.c. The main parts of it are the readfile and countwords functions. The read file opens the
                    file and writes its contents to a string, the countwords function takes this string and breaks it up word by word. Each word is assigned
                    to a WordCountPair (WCP) strict which holds a string for the word and a count for the number of times the word shows up. When a new word is
                    found a WCP is made and it's added to a Binary Search Tree. When a word is found that is already in the tree then the count of that WCP is incremented.
                    The BST is sorted by the strings of the WCPs. Once the file is read then the BST function toArray is called, which returns an array of the tree.
                    That array is then sorted and the first 20 values are printed.

                    Also it should be noted that currently my wordcounter treats hyphenated words like "stone-work" as two seperate things. So in my Output
                    the word stone has count of two, when in the output on the website it has it with a count of 1. I asked in class and this is fine, just cutting stuff
                    up with a different delimiter!

    --Task 2--

        Part 1:

            File Name: task2_1.c
            Compile/Run -gcc -o task2_1 task2_1.c
                        -./task2_1 

                    Input: Hit ctrl-c after running!
                    Output: Interrupted!! When ctrl-c is hit.

        Part 2:
            File Name: task2_2.c
            Compile/Run -gcc -o task2_2 task2_2.c
                        -./task2_2

                    Input: None
                    Output: Scary infinite loop.

                    Currently, in an effort to get the program to continue to execute after catching the signal I set the value of b to 5 inside the handler
                    function. However, this creates an infinite loop for some reason, though the program does proceed to run past the error causing line! It just runs 
                    forever! :)

        Part 3:
            File Name: task2_3.c
            Compile/Run -gcc -o task2_3 task2_3.c
                        -./task2_3

                    Input: None
                    Output: UH OH! A SEG-FAULT!

        --EXTENSIONS--

            1. I made a binary search tree! The file is called BST.c with header file BST.h. There is a test file called testBST.c but it's not super
            extensive or detailed. I made it more for myself as I was making the binary search tree. The BST is the data structure I use in task 1. At this point I don't
            have tons of functions implemented, I'll probably add more later so I'm not going to list them all out or anything. But as far as the more needed ones go I have
            bst_add() which adds the value at the right spot in the tree based upon a given comparator function, bst_get() which takes a value and if it finds a node with that value
            will return the node, again uses a comparator function to check the values. Right now I only have an inorder print, but making the others is literally just moving a couple lines. 
            My inorder takes a function that details how the data is to be printed since the BST is polymorphic. I also have toArray which returns an array of all the
            nodes values. 

            2. The wordcounter will not take invalid file names. If you ran it with a command line input that doesn't exist it will print out

                "FILE NOT FOUND! Please run again."

            and quit the program. 