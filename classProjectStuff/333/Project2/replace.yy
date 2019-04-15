/**
* Hello World: replace "blah" with "hello world"
  Gotta use the -L flag!!!! gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl
*/
			 
%%
			 
blah    printf("hello world");
			 
%%
			 
int main ( int argc, char *argv[] ) {
				 
 yylex();
			 
 }