from MyR_lexer import lexer
from MyR_parser import parser
from semantic_analysis import check_types
from semantic_analysis import symbol_table
from semantic_analysis import function_table
from code_generation import generate_code
from virtual_machine import VirtualMachine

import traceback

# Initialize the symbol table
# symbol_table = {}

# Read input from file
with open('sample1.myr', 'r') as f:
    input_str = f.read()

# Parse input
parse_tree = parser.parse(input_str, lexer=lexer)

# Perform semantic analysis
if parse_tree is not None:
    try:
        check_types(parse_tree)
        print('Semantic analysis successful!')
        print('Symbol table:', symbol_table)
        print('Function table:', function_table)

        # Perform code generation
        code = generate_code(parse_tree)
        print('generated code:')
        print(code)
        # Run the generated code on the virtual machine
        print('Running the generated code on the virtual machine:')
        vm = VirtualMachine(code, symbol_table, function_table)
        vm.run()
    except Exception as e:
        print('Semantic error detected:', str(e))
        traceback.print_exc()  # Print the stack trace
else:
    print('Syntax error detected.')
