from MyR_lexer import lexer
from MyR_parser import parser

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
