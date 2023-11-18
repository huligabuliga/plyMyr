import ply.yacc as yacc
from MyR_lexer import tokens

# Define the grammar rules for the MyR language


def p_program(p):
    '''program : PROGRAM ID SEMICOLON vars function_list main_function
               | PROGRAM ID SEMICOLON vars empty main_function'''
    if len(p) == 7:
        p[0] = ('program', p[2], p[4], p[5], p[6])
    else:
        # Replace empty function_list with []
        p[0] = ('program', p[2], p[4], [], p[6])


def p_vars(p):
    '''vars : VARS var_list'''
    p[0] = ('vars', p[2])


def p_var_list(p):
    '''var_list : var_list type id_list SEMICOLON
                | type id_list SEMICOLON'''
    if len(p) == 5:
        p[0] = p[1] + [(p[2], p[3])]
    else:
        p[0] = [(p[1], p[2])]


def p_type(p):
    '''type : INT
            | FLOAT
            | BOOL
            | CHAR'''
    p[0] = p[1]


def p_id_list(p):
    '''id_list : id_list COMMA ID
               | ID'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_function_list(p):
    '''function_list : function_list function
                     | empty'''
    if len(p) == 3:
        # If p[1] is a list of functions, extend it with the new function
        if isinstance(p[1], list):
            p[1].extend([p[2]])
            p[0] = p[1]
        # If p[1] is a single function, create a new list with p[1] and p[2]
        else:
            p[0] = [p[1], p[2]]
    else:
        p[0] = []


def p_function(p):
    '''function : FUNCTION type ID LPAREN param_list RPAREN vars LBRACE statement_list return_statement RBRACE
                | FUNCTION type ID LPAREN param_list RPAREN LBRACE statement_list return_statement RBRACE'''
    if len(p) == 12:
        p[0] = ('function', p[2], p[3], p[5], p[7], p[9], p[10])
    else:
        p[0] = ('function', p[2], p[3], p[5], None, p[8], p[9])


def p_param_list(p):
    '''param_list : param_list COMMA type ID
                  | type ID'''
    if len(p) == 5:
        p[0] = p[1] + [(p[3], p[4])]
    else:
        p[0] = [(p[1], p[2])]


def p_main_function(p):
    '''main_function : MAIN LPAREN RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('main', p[5])


def p_statement_list(p):
    '''statement_list : statement_list statement
                      | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_statement(p):
    '''statement : assignment SEMICOLON
                 | function_call SEMICOLON
                 | read_statement SEMICOLON
                 | write_statement SEMICOLON
                 | if_statement
                 | while_statement
                 | for_statement
                 | return_statement SEMICOLON'''
    p[0] = p[1]


def p_assignment(p):
    '''assignment : ID ASSIGN expression
                  | ID LBRACKET expression RBRACKET ASSIGN expression'''
    if len(p) == 4:
        p[0] = ('assignment', p[1], p[3])
    else:
        p[0] = ('assignment', p[1], p[3], p[6])


def p_function_call(p):
    '''function_call : ID LPAREN arg_list RPAREN'''
    p[0] = ('function_call', p[1], p[3])


def p_arg_list(p):
    '''arg_list : arg_list COMMA expression
                | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_read_statement(p):
    '''read_statement : READ id_list'''
    p[0] = ('read', p[2])


def p_write_statement(p):
    '''write_statement : WRITE LPAREN write_list RPAREN'''
    p[0] = ('write', p[3])


def p_write_list(p):
    '''write_list : write_list COMMA expression
                  | STRING
                  | ID COMMA expression'''
    if len(p) == 4:
        p[0] = p[1] + [(p[3])]
    else:
        p[0] = [(p[1])]


def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN THEN LBRACE statement_list RBRACE
                    | IF LPAREN expression RPAREN THEN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE'''
    if len(p) == 9:
        p[0] = ('if', p[3], p[7])
    else:
        p[0] = ('if_else', p[3], p[7], p[11])


def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN DO LBRACE statement_list RBRACE'''
    p[0] = ('while', p[3], p[7])


def p_for_statement(p):
    '''for_statement : FOR ID LBRACKET expression TO expression RBRACKET DO LBRACE statement_list RBRACE'''
    p[0] = ('for', p[2], p[4], p[6], p[10])


def p_return_statement(p):
    '''return_statement : RETURN LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('return', p[3])


def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression EQ term
                  | expression NE term
                  | expression LT term
                  | expression LE term
                  | expression GT term
                  | expression GE term
                  | expression AND term
                  | expression OR term
                  | term
                  | STRING'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | function_call
            | factor'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | ID
              | ID LBRACKET expression RBRACKET
              | INTEGER
              | FLOATING_POINT'''
    if len(p) == 4:
        p[0] = ('array', p[1], p[3])
    else:
        p[0] = p[1]


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        line_start = max(p.lexer.lexdata.rfind('\n', 0, p.lexpos), 0)
        line_end = p.lexer.lexdata.find('\n', p.lexpos, len(p.lexer.lexdata))
        if line_end < 0:
            line_end = len(p.lexer.lexdata)
        line = p.lexer.lexdata[line_start:line_end]
        print("Syntax error at line %d, column %d: Unexpected token %s of type %s" %
              (p.lineno, find_column(p), p.value, type(p.value).__name__))
        print("Line of input: %s" % line.strip())
    else:
        print("Syntax error: Unexpected end of input")


def find_column(token):
    last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


# Build the parser
parser = yacc.yacc()
