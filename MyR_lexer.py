import ply.lex as lex

# reserved words
reserved = {
    # program
    'program': 'PROGRAM',
    'main': 'MAIN',

    # var
    'vars': 'VARS',

    # functions
    'function': 'FUNCTION',
    'return': 'RETURN',
    'void': 'VOID',

    # status
    'read': 'READ',
    'write': 'WRITE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'to': 'TO',

    # data types
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'bool': 'BOOL',

    # special functions
    'point': 'POINT',
    'line': 'LINE',
    'circle': 'CIRCLE',
    'penup': 'PENUP',
    'pendown': 'PENDOWN',
    'color': 'COLOR',
    'thickness': 'THICKNESS',
}

# Define the tokens for the MyR language
tokens = [
    'ID', 'ARRAY', 'SEMICOLON',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA', 'ASSIGN', 'PLUS', 'MINUS',
    'TIMES', 'DIVIDE', 'AND', 'OR', 'NOT', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'STRING', 'INTEGER', 'FLOATING_POINT',
]

tokens += reserved.values()

# Define regular expressions for the tokens
t_PROGRAM = r'program'

t_SEMICOLON = r';'
t_VARS = r'VARS'
t_FLOAT = r'float'
t_INT = r'int'
t_CHAR = r'char'
t_FUNCTION = r'function'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_COMMA = r','
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_AND = r'&'
t_OR = r'\|'
t_NOT = r'!'
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_WHILE = r'while'
t_DO = r'do'
t_FOR = r'for'
t_TO = r'to'
t_RETURN = r'return'
t_READ = r'read'
t_WRITE = r'write'
t_POINT = r'POINT'
t_LINE = r'LINE'
t_CIRCLE = r'CIRCLE'
t_PENUP = r'PENUP'
t_PENDOWN = r'PENDOWN'
t_COLOR = r'COLOR'
t_THICKNESS = r'THICKNESS'
# t_STRING = r'"[^"]*"'
t_INTEGER = r'\d+'
t_FLOATING_POINT = r'\d+\.\d+'
t_BOOL = r'true|false'
t_MAIN = r'main'

# define id with reserved words


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

# define STRINGS


def t_STRING(t):
    r'"[^"]*"'
    # t.value = t.value[1:-1]  # Remove the quotes
    return t


def t_ARRAY(t):
    r'([a-zA-Z_][a-zA-Z_0-9]*)\[(\d+)\]'
    # Store the identifier and the size as a tuple
    t.value = (t.value[1], int(t.value[2]))
    t.type = 'ARRAY'
    return t


# Define ignored characters (whitespace and comments)
t_ignore = ' \t\r\n'
t_ignore_COMMENT = r'\%\%.*'

# Define error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out

# Function to print tokens


def print_tokens(lexer, data):
    lexer.input(data)
    for token in lexer:
        print(token)
