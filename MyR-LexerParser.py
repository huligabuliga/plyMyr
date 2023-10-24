# project: MyR
# Author: Jonas Tobias Clausen

# /------------------------------------------------------------------------------------------------------------------\


# Lexer for MyR
import ply.lex as lex

# parser for Myr
import ply.yacc as yacc

# List of token names.   This is always required
tokens = (
    # Identifiers aka variables
    'ID',

    # Literals (constant values)
    'INT_CONST',
    'FLOAT_CONST',
    'CHAR_CONST',
    'STRING_CONST',

    # Operators +, -, *, /, %, &, |, !, <, <=, >, >=, ==, !=
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'MOD',
    'AND',
    'OR',
    'NOT',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQ',
    'NE',

    # Punctuation symbols ( ) [ ] , ; :
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'SEMICOLON',
    'COLON',

    # Keywords (reserved words)
    'PROGRAM',
    'VARS',
    'FUNCTION',
    'RETURN',
    'READ',
    'WRITE',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'DO',
    'FOR',
    'TO',
    'VOID',


)

# Regular expression rules for the tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_AND = r'&'
t_OR = r'\|'
t_NOT = r'!'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'


# Regular expression rules with action code
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOAT_CONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CHAR_CONST(t):
    r"'.'"
    t.value = t.value[1]
    return t


def t_STRING_CONST(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Reserved words
reserved = {
    'program': 'PROGRAM',
    'vars': 'VARS',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'read': 'READ',
    'write': 'WRITE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'to': 'TO',
    'void': 'VOID',
}


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
