# plyMyr

## Structure of a MyR Program

A typical MyR program has the following structure:

```MyR
Program Name_prog ;
<Declaration of Global Variables>
<Function Definition> %% There are only functions
%% Main Procedure .... comment
main()
{
<Statutes>
}
```

## variable declaration
Variables in MyR can be declared globally or locally. The syntax for variable declaration is as follows:
```
VARS %%Reserved word.
type: list_ids;
<type: list_ids; > etc...
```
Where type can be int, float and char. list_ids is a comma-separated list of identifiers. You can define a one-dimensional array by using the syntax id[N] where N is an integer and the array is indexable from 1 to N.

Example: int: id1, id2, id3[6]; %% This defines two variables and a vector of 6 integers (1 to 6).

## function declaration
You can define zero or more functions in MyR. The syntax for function declaration is as follows:
```
function <return-type> module_name ( <Parameters> ) ;
<Declaration of Local Variables>
{
<Statements> %% The language supports recursive calls.
}

```
Parameters follow the syntax of simple variable declaration and are input only. return-type can be of any supported type or void (if no value is returned).

## statuses
The basic syntax for each of the statutes in the MyR language is:

Id = Expression; or Id[exp] = Expression; 

Id = Function_Name((<arg1>, (<arg2>,...); %%always the arguments (actual parameters) are Expressions.

Id = Function_Name(<arg1>,..) + Id2[i+2] - cte

## void function
Function_Name (<arg1>,...); //void


## return of a function
return( exp ); %%This statute goes inside the functions and indicates the return value (if it is not void).

## read
read ( id, id[j-3],....);

## write
write ( "sign" or expression<, "sign" or expression>....);

## decision if/else
```
If (expression) then %% typical double decision
{ <statutes>; }
<else
{ <Statutes>; }>
```

## while 
```
while (expression) do %% Repeat statutes as long as the expression is true.
{ <Statutes>; }
```
## for 
```
for Id<dimensions>= exp to exp do
{ <Statutes>; } %% Repeat from N to M by skipping 1 by 1

```
## special functions 

Each special function will have the appropriate parameterization, e.g., POINT(x,y), CIRCLE (RADIUS), etc..

LINE, DOT, CIRCLE, ARC, PENUP, PENDOWN, COLOR, THICKNESS, CLEAN, etc.
(graphic)

LINE, CIRCLE, ARC: Paint a line, circle, and arc respectively.

PENUP, PENDOWN: Raise the pen (do not paint), lower the pen (paint).

COLOR, THICKNESS: Change color and thickness when painting.

Etc.

## example program: 
```
program fibonacci;
vars 
    int num, result;

function int fibonacci(int n) 
vars 
    int result;
{
    if (n <= 1) then {
        write("base case");
        return(n);
    } else {
        write("fibbonacci iteration 1");
        return (fibonacci(n - 1) + fibonacci(n - 2));
    }
}
   
main(){
  num = 10;
  result = fibonacci(num);
  write("Fibonacci of", result);
}
```


# Avancement logs
## 1st avance 
Created lexer and parser in antlr, not working but grammar rules defined 

## 2nd avance
hit a wall

From scratch start again October..

# 1st avance 22-24 oct:
reset project because antlr did not work and i could not figure it out... changing to ply restarted 22 october
pip install ply and started writing some tokens.
Lexer and Parser working, seems promising, can do sample 1 parse successful and tokens generated. 


# 2nd avance 24 oct- 4 nov
Semantic analysis working, functions will be added later... saves variables in a symbol table working in MyR format. Syntax errors happens as well :) 

# 3rd avance 4-nov - 7 nov
code generation at 80%. working missing functions, and loops. 

# 4th avance 7-nov 13nov 
updated code gen, more testing needed, will start on virt machine tomorrow, looks promising... 

# 5th avance 13nov - 23nov
panic mode, redid code generation for correct format, recreated vm so it ran that code, added grafics with turtle python, added array functionality, fixed bugs
