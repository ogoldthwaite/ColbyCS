/**
* Counts the number of lines, characters and vowels.
  Gotta use the -L flag to access the library!!!! gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl
  
  Owen Goldthwaite
  9/23/18
*/
%{
#include <string.h>

int lineNum = 0; 
int charNum = 0; 
int vowelNum = 0;
int numNum = 0;
int sentNum = 0;
int wordNum = 0;
%}

VOWEL [a,e,i,o,u]
NUMBER [0-9]+"."*[0-9]*
WORD [A-Za-z]("."|"!"|"?"|","|" "|\n)
SENTENCE [A-Za-z0-9]("."|"!"|"?")
VSENTENCE [a,e,i,o,u]("."|"!"|"?")

%%

{VSENTENCE} {sentNum++; charNum++; vowelNum++; wordNum++;}
{SENTENCE} {sentNum++; charNum++; wordNum++;}
{WORD}   {wordNum++; charNum += strlen(yytext); }
{NUMBER} {numNum++; charNum++;}
{VOWEL}  {vowelNum++; charNum++;}
\n       {lineNum++; charNum++;}
.        {charNum++;} 


			 
%%
			 
int main ( int argc, char *argv[] ) {
				 
    yylex();
    printf("Character Count: %d\n", charNum);
    printf("Line Count: %d\n", lineNum);
    printf("Vowel Count: %d\n", vowelNum);
    printf("Number Count: %d\n", numNum);
    printf("Sentence Count: %d\n", sentNum);
    printf("Word Count: %d\n", wordNum);





			 
 }