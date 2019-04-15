CS333 Project 2 - README
Owen Goldthwaite

[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]

[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]

[CHANGE YOUR FILE DIRECTORY TREE THING]

[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]
[CHANGE YOUR FILE DIRECTORY TREE THING]


Project1.
    C:.
        BusError.c                 CHANGE THIS STUFF
        FloatingPointTest.c
        Proj1Task1.c
        Proj1Task2.c
        Proj1Task3.c
        Proj1Task4.c
        Proj1Task5.c
        README.txt

OS: Windows 10
gcc: gcc (MinGW.org GCC-6.3.0-1) 6.3.0

Flex:

    --Task 1--
    File: encode.yy
    Compile/Run: $ flex encode.yy
                 $ gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl 
                 OR (I use above, but project says to use below, so I included both)
                 $ gcc -o repl lex.yy.c -ll
                 $ type EncodeTest.txt | repl
                 OR (I use above, but I assume below would be what you use on a mac)
                 $ cat EncodeTest.txt | ./repl 

    Output: All characters in EncodeTest.txt moved 13 char values foward, wrapping around at z back to a.

    --Task 2--
    File: RowCharVowel.yy
    Compile/Run: $ flex RowCharVowel.yy
                 $ gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl 
                 OR (I use above, but project says to use below, so I included both)
                 $ gcc -o repl lex.yy.c -ll
                 $ type Task2Test.txt | repl
                 OR (I use above, but I assume below would be what you use on a mac)
                 $ cat Task2Test.txt | ./repl

    Output: The number of characters, lines, and vowels in the file. The program assumes that we are counting \n as a character.
            Also uses all characters, not just letters. So things like spaces, quotes, brackets etc. will add to character count.
            Exention: I made it also count the number of sentences, words and numbers in the file!  

    --TASK 3--
    File: htmlStripper.yy
    Compile/Run: $ flex htmlStripper.yy
                 $ gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl 
                 OR (I use above, but project says to use below, so I included both)
                 $ gcc -o repl lex.yy.c -ll
                 $ type htmlTest1.txt | repl
                 OR (I use above, but I assume below would be what you use on a mac)
                 $ cat htmlTest1.txt | ./repl
                 
                 htmlTest1.txt is the small html file, the whole website one is called htmlTest2.txt

                 Output: The file but all tags, comments and whitespace except following where a <p> tag was, if there was a <p> then a 
                 blank line was put in. Currently keeps in spaces between words, but easy to change if needed!
                [\n\t' '] for SPACE if you dont want any spaces between words


    --TASK 4--
    File: CliteParser.yy
    Compile/Run: $ flex CliteParser.yy
                 $ gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl 
                 OR (I use above, but project says to use below, so I included both)
                 $ gcc -o repl lex.yy.c -ll
                 $ type CliteTest.txt | repl
                 OR (I use above, but I assume below would be what you use on a mac)
                 $ cat CliteTest.txt | ./repl

                 CliteTest.txt is the file given in the project put in a txt

                 Output: Text that lists all the tokens with their name, i.e. Integer, Keyword etc and their value i.e. 5, int etc.
                 It will also make sure all single and multiline comments are printed out.  

Extensions: 
    
    1:
        My first extension was done solo. It is making my Clite parser properly maintain comments. It works for single line and multiline
        comments. The .txt file CliteTest.txt has comments in it, so by the time you're reading this you should of already seen that it
        works.

    2:
        My second extension was also done solo. I made encode.yy a little more complex. I did this in a new file called CoolEncode.yy
        Instead of just sliding over every letter by x amount of spaces I instead substitute out each letter for a completely random 
        different letter in the alphabet. For example, ABCDEFGHIJKLMNOPQRSTUVWXYZ may become JXNHCPTOEVKFGUSQRILWADBMZY. The enciphered
        alphabet is random each time. Also, to make it even harder to decipher uppercase and lowercase letters will have seperate enciphered
        alphabets. The enciphered alphabets are created, and then the text is parsed with flex and every character is swapped for whatever
        it should be in the new enciphered alphabet. I reccomend looking through the file CoolEncode.yy to see what's going on!

            File: CoolEncode.yy
            Compile/Run: $ flex CoolEncode.yy
                 $ gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl 
                 OR (I use above, but project says to use below, so I included both)
                 $ gcc -o repl lex.yy.c -ll
                 $ type CoolEncodeTest.txt | repl
                 OR (I use above, but I assume below would be what you use on a mac)
                 $ cat CoolEncodeTest.txt | ./repl

                 Output: It will print out both the Initial and enciphered alphabets for easy comparison, followed by the enciphered text.
    
    3: 
        My third extension was also done solo. I just made the Task2 document analyser do a bit more. In addition to counting vowels, characters
        and lines it will now count any numbers, sentences and words as well. By the time you're reading this you probably already ran it
        because I didn't make any new files for this, just added to the old RowCharVowel.yy file. So compile/run commands are the same as for
        task 2!