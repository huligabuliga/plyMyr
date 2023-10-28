from MyR_lexer import lexer
from MyR_parser import parser
from semantic_analysis import check_types

# Initialize the symbol table
symbol_table = {}

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
    except Exception as e:
        print('Semantic error detected:', str(e))
else:
    print('Syntax error detected.')