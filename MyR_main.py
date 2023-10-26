from MyR_lexer import lexer
from MyR_parser import parser
from semantic_analysis import check_types_ast


# Read input from file
with open('sample1.myr', 'r') as f:
    input_str = f.read()

# Tokenize input
lexer.input(input_str)

tokens = []
while True:
    tok = lexer.token()
    if not tok:
        break
    tokens.append(tok)

# Parse input
parse_tree = parser.parse(input_str, lexer=lexer)

# Print tokens and parse tree
print(tokens)
print(parse_tree)
if parse_tree is not None:
    print('Parse successful!')
else:
    print('Syntax error detected.')

# Perform semantic analysis
if parse_tree is not None:
    # ast[2]
    print(parse_tree[2])
    check_types_ast(parse_tree)
    print('Semantic analysis successful!')
else:
    print('Syntax error detected.')
