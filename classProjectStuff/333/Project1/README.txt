CS333 Project 1 - README
Owen Goldthwaite

Project1.
    C:.
        BusError.c
        FloatingPointTest.c
        Proj1Task1.c
        Proj1Task2.c
        Proj1Task3.c
        Proj1Task4.c
        Proj1Task5.c
	README.txt

OS: Windows 10
gcc: gcc (MinGW.org GCC-6.3.0-1) 6.3.0

C:

--Part 1--

Task 1: The file for this task is Proj1Task1.c, it has no input, everything is hard coded. It should output a information that represents
how different data types are stored in memory. To do this just pick a variable and assign it as a casted unsigned char* to the pointer ptr
then change any necessary code in the for loop, like sizeof(<datatype>). Compile and run!

Task 1 Questions: My machine is little-endian. I can tell because when I run the program using an int with the value 0x01234567 the order
of the bytes printed is 67 45 23 01. This means it's little-endian because the least significant byte is placed at the location with the
lowest address, i.e. 67 is the first byte. If it were big endian the byte order would be 01 23 45 67.

Compile: gcc -o Proj1Task1 Proj1Task1.c 
Run: ./Proj1Task1

Task 2: File for this one is Proj1Task2.c, again no input. It outputs a bunch of bytes that show how the memory is structured and where
certain variables may be stored inside said memory.

Task 2 Questions: So the amount of memory that I can access seems relatively arbitrary. The loop currently runs for __INT_MAX__ times. But
it always stops early, sometimes the program will stop as early as 223 bytes, sometimes it loops through over 800,000. I'm not sure why
it changes like this. At the end of the process the program just stops. If it stops prematurely there is a bit of a delay where nothing is
printed, if it stops on time (with only 100 bytes printed persay) this delay isn't there. I can see the other variables I declared. I have
two ints for simplicities sake with easy to spot hex values. You can see them on bytes 4-7 and 8-11.

Compile: gcc -o Proj1Task2 Proj1Task2.c 
Run: ./Proj1Task2

Task 3: File is Proj1Task3.c, no input or output. Inefficiently allocates a lot of memory. This can be seen anywhere you can view memory
usage, I just used the performance monitor on Windows 10. 

Task 3 Questions: I have 16 gigs of ram. Right now, running whatever processes I'm running I'm using about 48% of that. When I run this
program WITHOUT the free statement that jumps up to about 60% or so and stays there. With the Free statement it stays at ~48% with no readable
change at all. 

Compile: gcc -o Proj1Task3 Proj1Task3.c 
Run: ./Proj1Task3

Task 4: File is Proj1Task4.c, in input. Outputs 25 bytes of memory. The struct starts at byte 4. 

Task 4 Question: So I spent some time looking into structs and how they work. At first the sizeof did not meet my expectation, originally I
had 4 variables, the byte amount of the added varibles was 11, but the struct had a size of 12 bytes. I thought I was doing something
wrong so I learned about padding bytes and how everything is trying to remain aligned. So now my struct is 13 bytes of variables, 16 bytes in
total because 3 padding bytes are added to the end of it. I organized the order of the variables so there are no padding bytes between them,
only at the end. So no, there are no gaps in my fields currently, but there were originally. So to better answer the question, if the items
in the struct are not ordered specifically to limit alignment bytes in between them then extra bytes will be added and potentiall cause
far more memory than anticipated to be used.

Compile: gcc -o Proj1Task4 Proj1Task4.c 
Run: ./Proj1Task4

Task 5: File is Proj1Task5.c, input is typed in. Just run the program normally and it will prompt you to put in a string. Outputs "Hacked" if value of stringThing.num has been changed by inputting a string that messes up
it's value in memory. "Safe" if nothing changed. So will output "Hacked" if the string parameter in the function rip is any longer than
4 characters (line 37). 

Task 5 Questions: No Questions

Compile: gcc -o Proj1Task5 Proj1Task5.c 
Run: ./Proj1Task5

--EXTENSION STUFF--

1: Task 5 User Input Extension: It should say so in the task 5 part above, but I allowed the user to input the string used to test the safe/Hacked.
The program will prompt you for a string, just type it in and hit enter! 

Compile: gcc -o Proj1Task5 Proj1Task5.c 
Run: ./Proj1Task5

2: Bus Error Extension: The file to run is BusError.c, no input needed. It should give a bus error! Since a bus error occurs when you're
trying to reference memory that doesn't exist I just tried to print the result of 5/0, which shouldn't exist. Therefore it should give
a bus error, which it did! The difference between a bus error and a seg fault is a bus error is caused when the memory doesn't exist whereas
a seg fault is when you try to access memory that you are unable too for some reason, maybe it's being used by another process for example.

Compile: gcc -o BusError BusError.c 
Run: ./BusError

3: Float + 1 = Float Extension: So I'm not sure if this is the answer that was being looked for, but it's here anyway! File to run is
FloatingPointTest.c, it just outputs the max float value, the max float value plus 1 and if they are equal or unequal. They are equal as you would
expect, therefore the float you can add 1 to and get the same number is the max float value!

Compile: gcc -o FloatingPointTest FloatingPointTest.c 
Run: ./FloatingPointTest

4: Extra Paragraph: I did an extra language "paragraph" thing on Lua, it should be on the wiki.








