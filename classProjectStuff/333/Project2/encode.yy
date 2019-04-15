/**
* Takes a-z or A-Z and shifts it 13 spaces foward in alphabet, with wraparound.
  Gotta use the -L flag to access the library!!!! gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl
  
  Owen Goldthwaite
  9/23/18
*/

%{
#include <stdio.h>
void test();

void test()
{
    printf("hey\n");
}

%}

LOWCHAR [a-z]
HIGHCHAR [A-Z]

%%

{LOWCHAR}     {
                if(*yytext + 13 > 122)
                    {
                        *yytext = 97 + (13 - (122 - *yytext));
                    }
                else
                    {
                        *yytext = *yytext + 13;
                    }
                    
                printf("%c", *yytext);
            }

{HIGHCHAR}     {
                if(*yytext + 13 > 90)
                    {
                        *yytext = 65 + (13 - (90 - *yytext));
                    }
                else
                    {
                        *yytext = *yytext + 13;
                    }
                    
                printf("%c", *yytext);
            }    
			 
%%
			 
int main ( int argc, char *argv[] ) {
				 
 yylex();
			 
 }