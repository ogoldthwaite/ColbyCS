/**
* Encodes character better than normal encode! I don't know the specifics of how I'm coding them yet ;)
* THIS IS AN EXTENSION
*  Gotta use the -L flag to access the library!!!! gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl
  
  Owen Goldthwaite
  9/23/18
*/
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>

#define ARRAYLENGTH(array) (sizeof(array)/sizeof(array[0]))
void cipher();
char swapLet(char initChar, bool upperCase);

typedef struct newLetter
{
    char letter;
    char oldLet;
    int num;
}newLet;

char lowBet[26] = "abcdefghijklmnopqrstuvwxyz";
char upBet[26] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
newLet newLowBet[26];
newLet newUpBet[26];

void cipher() //creates alternate alphabet for enciphering
{
     srand(time(0));

     for(int i = 0; i < ARRAYLENGTH(newLowBet); i++) //Creating the array
     {     
         newLowBet[i].num = i;
         newUpBet[i].num = i;
     }
     for(int i = 0; i < ARRAYLENGTH(newLowBet); i++) //Shuffling the array
     {
         newLet temp1 = newLowBet[i];
         int randIndex1 = rand()%26;

         newLowBet[i] = newLowBet[randIndex1];
         newLowBet[randIndex1] = temp1;

         newLet temp2 = newUpBet[i];
         int randIndex2 = rand()%26;

         newUpBet[i] = newUpBet[randIndex2];
         newUpBet[randIndex2] = temp2;
     }

     for (int i = 0; i < ARRAYLENGTH(newLowBet); i++) //Assigning characters from alphabet to corresponding newLowBet.num vals i.e. A->1 B->2 etc
     {    
         int loc = newLowBet[i].num;
         newLowBet[i].letter = lowBet[loc];
         newLowBet[i].oldLet = lowBet[i];

         loc = newUpBet[i].num;
         newUpBet[i].letter = upBet[loc];
         newUpBet[i].oldLet = upBet[i];
     }
    
    //Just printing stuff! Not necessary
    printf("Initial Lowercase Alphabet: a b c d e f g h i j k l m n o p q r s t u v w x y z\n");
    printf("Enciphered Lowercase Alpha: ");
    for (int i = 0; i < ARRAYLENGTH(newLowBet); i++)
    { printf("%c ", newLowBet[i].letter); }

    printf("\n\n");

    printf("Initial Uppercase Alphabet: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n");
    printf("Enciphered Uppercase Alpha: ");
    for (int i = 0; i < ARRAYLENGTH(newLowBet); i++)
    { printf("%c ", newUpBet[i].letter); }

    printf("\n\n");
}

char swapLet(char initChar, bool upperCase) //swaps initChar with the apropraite letter substitute, uppercase letters if uppercase is true
{
    for (int i = 0; i < ARRAYLENGTH(newLowBet); i++)
    {
        if( !(upperCase) && initChar == newLowBet[i].oldLet)
        {
            return newLowBet[i].letter;
            break;
        }
        else if( (upperCase) && initChar == newUpBet[i].oldLet)
        {
            return newUpBet[i].letter;
            break;
        }
    }
    return '-'; //Shouldn't reach this, here to debug mainly
}

%}

LOWCHAR [a-z]
HIGHCHAR [A-Z]

%%

{LOWCHAR}     {
                *yytext = swapLet(*yytext, false);
                    
                printf("%c", *yytext);
              }

{HIGHCHAR}     {
                *yytext = swapLet(*yytext, true);
                    
                printf("%c", *yytext);
              }
  
			 
%%
			 
int main ( int argc, char *argv[] ) 
{
 
 cipher();
 yylex();
			 
}