CS333 Project 8 - README
Owen Goldthwaite

Project8.
    C:.
      colorize.c
      IMG_4203.ppm
      ppmlO.c
      ppmlO.h
      README.txt
      task1.c

OS: Windows 10
gcc: gcc (MinGW.org GCC-6.3.0-1) 6.3.0

C: 
    --Task 1--

        File Name: task1.c 
        Compile/Run -gcc -o task1 task1.c -lpthread
                    -./task1 
                
                Input: You'll be prompted to whatever input you need
                Output: The times taken by sorting using threads vs. just using qsort 

        Computation time is obviously increased for the larger the array is. However, a very small array takes the threaded sort longer than
        normal qsort because it has to break everything up, which is pretty pointless with such a small array. As the array gets larger the difference
        between the two is increased, but using say 2 threads doesn't double the speed. Also, if you use too many threads it will be slower than
        the normal way. With my program it seems around 8 threads is the fastest. However, my remerge after sorting the split array is very ineefficient.
        It works, but it's far from as effective as it could be! This definitely impacts the speeds, but overall threaded is still faster than not.
        It's hard to say if this compares well to Amdahl's law because it's far from perfect, but as is it's not very similar!

    --Task 2--

        File Name: colorize.c 
        Compile/Run -gcc -o colorize -I. colorize.c ppmIO.c -lm -lpthread
                    -./colorize IMG_4203.ppm
                
                Input: You'll be prompted to whatever input you need
                Output: A file called bold.ppm with the new image, right now it should just be a teal box

        This one is a much better computation time comparison. Similar to the first one, threads are faster. However, the difference is a lot
        more noticable here. Using 10 threads you can triple the computation time. To compare I made each thread process it's segment 50 times
        and the nonthreaded process also processes the image 50 times. The difference is pretty substantial. I came across the issue of my computer not
        really handling editing the ppm very well. For example, running the base code, unedited just returns a blackish-gray image, not the input image bolded.
        My code also did the same after I added support for threads. I asked my partner, Gautam about it and he did not have the issue. I then ran his code on my
        computer and it did the same thing, a blackish-grey square. His works fine on his computer, so the issue is something to do with my computer and therefore can't
        really fix it. It doesn't impact run times in anyway though. But just be aware if you try to open any of my output ppms they won't look normal!


        Extensions:
            1. You can input any number of threads you want, you'll be prompted upon running the program.

            2. My colorize file changes every pixel to a random rgb color to make it look crazzzyy!