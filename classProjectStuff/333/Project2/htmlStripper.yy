/**
* Strips an html formatted file of all tags, comments, and whitespace without <p> tag.
  Gotta use the -L flag to access the library!!!! gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl

  //[\n\t' '] for SPACE if you dont want any spaces between words
  Owen Goldthwaite
  9/23/18
*/
%{


%}

PTAG <p>
TAG \<[^>]+>
SPACE [\n\t]

%%

{PTAG} printf("\n\n");
{TAG} 
{SPACE}
			 
%%
			 
int main ( int argc, char *argv[] ) {
				 
    yylex();
			 
 }