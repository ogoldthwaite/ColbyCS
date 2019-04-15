CS333 Project 6 - README
Owen Goldthwaite

Project6.
    C:.
        memoryp1.c
        memoryp2.c 
        README.txt
        profileout

OS: Windows 10
gcc: gcc (MinGW.org GCC-6.3.0-1) 6.3.0

C: 
    -Task 1--
        Part 1:

        File Name: memoryp1.c 
        Compile/Run -gcc -o memoryp1 memoryp1.c 
                    -./memoryp1 

                Input: The program will prompt you for small, med and large allocation size and the allocation count.
                Output: Total time and average time for each allocation size.

                The average time per call changes depending on what values you use, honestly there isn't much to say here since the program
                outputs all the data, so just run it! :)

        Part 2:
        
        File Name: memoryp2.c 
        Compile/Run -gcc -o memoryp2 memoryp2.c 
                    -./memoryp2 

                Input: Program will prompt you for some stuff to put in! Similar to last one.
                Output: Basically same thing as last program, total time fo all calls and avg time per call.

                The time of the management calls definitely seems to change when using free. For example, I ran the first program with small size set at 
                10000, with a count of 1000000 and the other two sizes at 0. I waited about 5 seconds and the small wasn't even done so I want to the second program
                and ran it with the same memory size, 10000 and the same count, 1000000. It finished pretty quickly. This leads me to believe that for every allocation
                call that isn't freed the runtime will increase more and more. However, when it is freed this problem is more or less negated. Though some extra time
                is used in the actual time it takes to free. 

                Also, when running this file it does all the mallocs with frees, but then does the same amount of mallocs again to see if they take longer. They don't.
                They theoretically should since the heap is split up into memory chunks that should be used by the same memory size so when a different one comes along 
                it has a harder time allocating it, but this doesn't seem to be the case probably due to some sort of compiler optimization.
                
                It seems to make a difference allocating/freeing set sizes versus random sizes. It's hard to say for sure because random is
                after all random, but I've tried running the program with different sizes/counts keeping the count the same for random / fixed and
                random seems to almost always come out ahead. Even if the fixed size is larger than the average random size would be. 


        Extensions:
            1. A lot of user input so it's easier to run the files with different parameters. They will prompt you for whatever it is you are 
            supposed to enter. Just makes it easier to compare things.

            2. I used a profiler on my code. The output file with all the information is called profileout