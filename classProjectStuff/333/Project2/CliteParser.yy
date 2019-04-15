/**
* Parses a Clite file and outputs a sequence of strings corresponding to the tokens
  If you are Owen then you gotta use the -L flag to access the library!!!! gcc -o repl lex.yy.c -L"C:\GnuWin32\lib" -lfl
  Also properly maintains comments for an extension!!

  Owen Goldthwaite
  9/23/18
*/
%{

%}

INTEGER [0-9]+
FLOAT [0-9]+.[0-9]+
KEYWORD if|else|while|for|int|float
IDENTIFIER [A-Za-z]([A-Za-z]*|[0-9]*)
ASSIGNMENT =
COMPARISON ==|<|>|<=|>=
OPERATOR "+"|"-"|"*"|"/"
OPENBRACKET "{"
CLOSEBRACKET "}"
OPENPAREN "("
CLOSEPAREN ")"
SPACE [\n\t' ']
SINGLECOMMENT "//".*[^\n]
MULTICOMMENT "/*"([^*]|(\*+[^*/]))*"*"+"/"

%%

{KEYWORD} printf("Keyword-%s\n", yytext);
{IDENTIFIER} printf("Identifier-%s\n", yytext);
{INTEGER} printf("Integer-%s\n", yytext);
{FLOAT} printf("Float-%s\n", yytext);
{ASSIGNMENT} printf("Assignment\n");
{COMPARISON} printf("Comparison-%s\n", yytext);
{OPERATOR} printf("Operator-%c\n", *yytext);
{OPENBRACKET} printf("Open-Bracket\n");
{CLOSEBRACKET} printf("Close-Bracket\n");
{OPENPAREN} printf("Open-Paren\n");
{CLOSEPAREN} printf("Close-Paren\n");
{SINGLECOMMENT} printf("%s\n", yytext);
{MULTICOMMENT} printf("%s\n", yytext);
{SPACE}
;

			 
%%
			 
int main ( int argc, char *argv[] ) {
				 
    yylex();
			 
 }