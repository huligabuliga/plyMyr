   Operator Operand1 Operand2      Result
0      goto                    start_main
1     label                           add
2         +        a        b         Ti1
3         =      Ti1                dobby
4    return                         dobby
5   EndFunc
6     label                    start_main
7         =       20                    x
8         =       40                    y
9       ERA      add
10    param        x                 par1
11    param        y                 par2
12    gosub                           add
13        =      add                  Ti2
14        =      Ti2                    c
15    param                      "sum is"
16    param                             c
17    write                             2
18  EndProg
Local variables:
Global variables:
x 0
y 1
c 2
a 3
b 4
Running the generated code on the virtual machine:
pc =  1
goto node detected
pc =  7
pc =  8
equal node detected
arg1:  20
arg2:
result:  x
Assigning value to global variable
Value of  x  is now  20
pc =  9
equal node detected
arg1:  40
arg2:
result:  y
Assigning value to global variable
Value of  y  is now  40
pc =  10
ERA node detected
function info {'return_type': 'int', 'param_types': ['int', 'int'], 'params': ['a', 'b'], 'vars': [('int', ['dobby'])]} 
adding var_name:  a
adding var_name:  b
adding var:  dobby
pc =  11
param node detected
memory_map:  [20, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
stack:  []
result:  par1
arg1:  x
arg2:
global_vars:  {'x': 0, 'y': 1, 'c': 2, 'a': 3, 'b': 4}
local_vars:  [{'a': 0, 'b': 1, 'dobby': 2}]
temp_vars:  {} {} {}
found in global_vars
stack:  [20]
pc =  12
param node detected
memory_map:  [20, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
stack:  [20]
result:  par2
arg1:  y
arg2:
global_vars:  {'x': 0, 'y': 1, 'c': 2, 'a': 3, 'b': 4}
local_vars:  [{'a': 0, 'b': 1, 'dobby': 2}]
temp_vars:  {} {} {}
found in global_vars
stack:  [20, 40]
pc =  13
Assigning 40 value to param b
Assigning 20 value to param a
call stack:  [13]
function_name_stack:  ['add']
pc =  2
pc =  3
+ node detected
new temporal variable detected
Declared temp variable:  Ti1
arg1_value 20 arg2_value: 20 sum is 40
pc =  4
equal node detected
arg1:  Ti1
arg2:
result:  dobby
Assigning value to local variable
Value of  dobby  is now  40
local_vars:  [{'a': 3, 'b': 3, 'dobby': 2}]
local memory map:  [None, 40, 40, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40]
pc =  5
return node detected
local_vars:  [{'a': 3, 'b': 3, 'dobby': 2}]
global_vars:  {'x': 0, 'y': 1, 'c': 2, 'a': 3, 'b': 4}
return_value:  40
stack:  [40]
pc =  6
EndFunc node detected
call stack:  [13]
going to return address:  13
pc:  13
code:  ('=', 'add', '', 'Ti2')
function_name:  add
assining value to global variable:  40
global_vars:  {'x': 0, 'y': 1, 'c': 2, 'a': 3, 'b': 4, 'add': 5}
pc =  14
equal node detected
arg1:  add
arg2:
result:  Ti2
Declaring temp variable:  Ti2
Assigning value to a temporal variable
Value of  Ti2  is now  40
pc =  15
equal node detected
arg1:  Ti2
arg2:
result:  c
Assigning value to global variable
Value of  c  is now  40
pc =  16
param node detected
memory_map:  [None, 40, 40, 20, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 40]
stack:  []
result:  "sum is"
arg1:
arg2:
global_vars:  {'x': 0, 'y': 1, 'c': 2, 'a': 3, 'b': 4, 'add': 5}
local_vars:  []
temp_vars:  {'Ti<bound method MemoryMap.next_temp_index of <memorymap.MemoryMap object at 0x000001869D362850>>': 0, 'Ti1': 100, 'Ti2': 101} {} {}
stack:  ['"sum is"']
pc =  17
param node detected
memory_map:  [None, 40, 40, 20, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 40]
stack:  ['"sum is"']
result:  c
arg1:
arg2:
global_vars:  {'x': 0, 'y': 1, 'c': 2, 'a': 3, 'b': 4, 'add': 5}
local_vars:  []
temp_vars:  {'Ti<bound method MemoryMap.next_temp_index of <memorymap.MemoryMap object at 0x000001869D362850>>': 0, 'Ti1': 100, 'Ti2': 101} {} {}
stack:  ['"sum is"', 40]
pc =  18
"sum is" 40
pc =  19