CS333 Project 4 - README
Owen Goldthwaite

Project4.
    C:.
        task2.c                 
        haiku.c
        precedence.c
        task1.c
        task1Ex.c
        README.txt

C: 
    --Task 1--
        File Name: task1.c 
        Compile/Run: -gcc -o task1 task1.c 
                     -./task1
        
        Input: None!
        Output: The sorted array sorted with evens first in descending order, followed by odds in ascending order.

    --Task 2--
        File Name: task2.c 
        Compile/Run: -gcc -o task2 task2.c 
                     -./task2

        Input: You'll be prompted to enter a number to take the factorial of, just type it in!
        Output: The value of the input numbers factorial. num!

        Q1. This demonstrates function pointers and that a variable can in a way have the type of a function which allows for functions to 
        essentially be passed as arguments and used like any other variable of some type would be.

        Q2. Going past 12! from 13! and onwards the numbers reach the max 32 bit integer capacity, and therefore start to wrap around starting
        from the bottom again. 


        EXTENSIONS:
            1: A haiku, it's in file haiku.c. The actual haiku is the body of the main function, I needed it inside so it would actually compile.
            It talks about the if statement and it's then part! I'm assuming that printf is prounouces print f and is two syallabes.
            
                    File Name: haiku.c 
                    Compile/Run: -gcc -o haiku haiku.c 
                     -./haiku

                     Input: None
                     Output: Just prints some stuff

            2: I made my comparator function faster. I did this by creating some variables at the start of the method so I don't have to perform as
            man operations. The speed increase isn't anything crazy, but it's definitely faster. It's the function fast comp in the file is task1Ex.c. 
            It first runs the normal comparator and prints out how long it took, then runs the faster one and prints out how long that one took.

                    File Name: task1Ex.c 
                    Compile/Run: -gcc -o task1Ex task1Ex.c 
                     -./task1Ex

                     Input: None
                     Output: prints out the times taken for each comparator.

            3: I just made a file to look at memory operator precedence in C. I looked at *, & and >>. I found that the precedence seems to be
            in that order. First *, then &, then >> (or <<). The file I look at this in is precedence.c. Looking at the code I make an int (a) and an int* (b).
            First I print out *&b then just &b. Since the two things printed are different it means that *&b derefences b first and then prints the address of the 
            derefenced thing, whereas &b justprints the address of b. Next with the bitshift operator >> I shifted a by *b bits, or a>>*b. Since the only way
            this even compiles is if the dereference of b is used it means that * is done before >> is.

                    File Name: precedence.c 
                    Compile/Run: -gcc -o precedence precedence.c 
                     -./precedence

                     Input: None
                     Output: Prints out some addresses and values of things!
