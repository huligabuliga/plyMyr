from MyR_lexer import lexer
from MyR_parser import parser
from semantic_analysis import check_types
from semantic_analysis import symbol_table
from semantic_analysis import function_table
from code_generation import generate_code
from virtual_machine import VirtualMachine

import traceback
import pandas as pd


def flatten(lst):
    result = []
    for i in lst:
        if isinstance(i, list):
            result.extend(flatten(i))
        elif isinstance(i, tuple):
            result.append(i)
        else:
            result.append(i)
    return result


def print_tokens(data):
    lexer.input(data)
    # for token in lexer:
    #     print(
    #         f'Type: {token.type}, Value: {token.value}, Line: {token.lineno}, Position: {token.lexpos}')


print("""
     ____    ____             _______     
    |_   \  /   _|           |_   __ \    
      |   \/   |     _   __    | |__) |   
      | |\  /| |    [ \ [  ]   |  __ /    
     _| |_\/_| |_    \ '/ /   _| |  \ \_  
    |_____||_____| [\_:  /   |____| |___| 
                    \__.'                 
    """)


# Ask the user for the filename
filename = input("Please enter the filename: ")

filename = f'testcode/{filename}'
# filename = 'test_code.txt'
# Read input from file
with open(filename, 'r') as f:
    input_str = f.read()

try:
    # Print tokens
    print_tokens(input_str)
except Exception as e:
    print('Error in lexer:', str(e))
    traceback.print_exc()
    exit()

try:
    # Parse input
    # Parse input
    parse_tree = parser.parse(input_str, lexer=lexer)
except Exception as e:
    print('Error in parser:', str(e))
    traceback.print_exc()
    exit()

if parse_tree is not None:
    try:
        # Perform semantic analysis
        check_types(parse_tree)
        print('Semantic analysis successful!')
        print('Symbol table:', symbol_table)
        # Write symbol_table to a file
        with open('symbol_table.log', 'w') as f:
            f.write(str(symbol_table))
        print('Function table:', function_table)
        # Write function_table to a file
        with open('function_table.log', 'w') as f:
            f.write(str(function_table))

    except Exception as e:
        print('Error in semantic analysis:', str(e))
        traceback.print_exc()
        exit()

    try:
        # Perform code generation
        code = generate_code(parse_tree)
        code = flatten(code)
        print('Generated code:')
        print(code)
        # dataframe
        df = pd.DataFrame(
            code, columns=['Operator', 'Operand1', 'Operand2', 'Result'])
        print(df)
        # Write dataframe to a file
        df.to_csv('code.csv', index=False)
    except Exception as e:
        print('Error in code generation:', str(e))
        traceback.print_exc()
        exit()

    # try:
    #     # Run the generated code on the virtual machine
    #     print('Running the generated code on the virtual machine:')
    #     vm = VirtualMachine(code, symbol_table, function_table)
    #     vm.run()
    # except Exception as e:
    #     print('Error in virtual machine:', str(e))
    #     traceback.print_exc()
else:
    print('Syntax error detected.')
