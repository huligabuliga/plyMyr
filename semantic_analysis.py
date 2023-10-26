# Import the parser module and the parse_program function
from MyR_parser import parser
from MyR_lexer import tokens

# Define the symbol table
symbol_table = {}

# Define the semantic cube
semantic_cube = {
    ('int', 'int', '+'): 'int',
    ('int', 'float', '+'): 'float',
    ('float', 'int', '+'): 'float',
    ('float', 'float', '+'): 'float',
    ('int', 'int', '-'): 'int',
    ('int', 'float', '-'): 'float',
    ('float', 'int', '-'): 'float',
    ('float', 'float', '-'): 'float',
    ('int', 'int', '*'): 'int',
    ('int', 'float', '*'): 'float',
    ('float', 'int', '*'): 'float',
    ('float', 'float', '*'): 'float',
    ('int', 'int', '/'): 'float',
    ('int', 'float', '/'): 'float',
    ('float', 'int', '/'): 'float',
    ('float', 'float', '/'): 'float',
    ('int', 'int', '<'): 'bool',
    ('int', 'float', '<'): 'bool',
    ('float', 'int', '<'): 'bool',
    ('float', 'float', '<'): 'bool',
    ('int', 'int', '>'): 'bool',
    ('int', 'float', '>'): 'bool',
    ('float', 'int', '>'): 'bool',
    ('float', 'float', '>'): 'bool',
    ('int', 'int', '=='): 'bool',
    ('int', 'float', '=='): 'bool',
    ('float', 'int', '=='): 'bool',
    ('float', 'float', '=='): 'bool',
    ('int', 'int', '!='): 'bool',
    ('int', 'float', '!='): 'bool',
    ('float', 'int', '!='): 'bool',
    ('float', 'float', '!='): 'bool',
    ('bool', 'bool', '&&'): 'bool',
    ('bool', 'bool', '||'): 'bool',
    ('int', 'int', '&&'): 'int',
    ('int', 'int', '||'): 'int',
    ('float', 'float', '&&'): 'float',
    ('float', 'float', '||'): 'float',
    ('int', 'bool', '&&'): 'int',
    ('int', 'bool', '||'): 'int',
    ('float', 'bool', '&&'): 'float',
    ('float', 'bool', '||'): 'float',
    ('bool', 'int', '&&'): 'int',
    ('bool', 'int', '||'): 'int',
    ('bool', 'float', '&&'): 'float',
    ('bool', 'float', '||'): 'float',
    ('bool', 'bool', '+'): 'bool',
    ('bool', 'bool', '-'): 'bool',
    ('bool', 'bool', '*'): 'bool',
    ('bool', 'bool', '/'): 'bool',
    ('bool', 'bool', '<'): 'bool',
    ('bool', 'bool', '>'): 'bool',
    ('bool', 'bool', '=='): 'bool',
    ('bool', 'bool', '!='): 'bool',
}


def check_types_ast(ast, symbol_table=symbol_table, semantic_cube=semantic_cube):
    """
    Check the types of the AST nodes recursively.
    """
    node_type = ast[0]

    if node_type == 'program':
        # Check types of vars and main
        check_types_ast(ast[2], symbol_table, semantic_cube)
        check_types_ast(ast[4], symbol_table, semantic_cube)

    elif node_type == 'vars':
        # Add variables to symbol table
        for var in ast[1]:
            var_type, var_names = var
            for var_name in var_names:
                symbol_table[var_name] = var_type

    elif node_type == 'main':
        # Check types of statements in main
        for statement in ast[1]:
            check_types_ast(statement, symbol_table, semantic_cube)

    elif node_type == 'assignment':
        # Check types of expression and variable
        var_name = ast[1]
        var_type = symbol_table.get(var_name)
        expr_type = check_types_ast(ast[2], symbol_table, semantic_cube)

        if var_type is None:
            # Variable not defined
            print(f"Error: Variable '{var_name}' not defined.")
        elif var_type != expr_type:
            # Type mismatch
            print(
                f"Error: Type mismatch in assignment to variable '{var_name}'.")

    elif node_type == 'write':
        # Check types of expression
        check_types_ast(ast[1], symbol_table, semantic_cube)

    elif node_type == 'binop':
        # Check types of left and right expressions
        left_type = check_types_ast(ast[2], symbol_table, semantic_cube)
        right_type = check_types_ast(ast[3], symbol_table, semantic_cube)
        op = ast[1]
        result_type = semantic_cube.get((left_type, right_type, op))

        if result_type is None:
            # Invalid operation
            print(
                f"Error: Invalid operation '{op}' between types '{left_type}' and '{right_type}'.")
            return None
        else:
            return result_type

    elif node_type == 'unop':
        # Check type of expression
        expr_type = check_types_ast(ast[2], symbol_table, semantic_cube)
        op = ast[1]

        if op == '-':
            if expr_type not in ['int', 'float']:
                # Invalid operation
                print(
                    f"Error: Invalid operation '{op}' on type '{expr_type}'.")
                return None
            else:
                return expr_type
        elif op == '!':
            if expr_type != 'bool':
                # Invalid operation
                print(
                    f"Error: Invalid operation '{op}' on type '{expr_type}'.")
                return None
            else:
                return 'bool'

    elif node_type == 'var':
        # Check if variable is defined
        var_name = ast[1]
        var_type = symbol_table.get(var_name)

        if var_type is None:
            # Variable not defined
            print(f"Error: Variable '{var_name}' not defined.")
            return None
        else:
            return var_type

    elif node_type == 'const':
        # Return type of constant
        const_type = ast[1]

        if const_type in ['int', 'float', 'bool', 'string']:
            return const_type
        else:
            # Invalid constant type
            print(f"Error: Invalid constant type '{const_type}'.")
            return None

    else:
        # Invalid node type
        print(f"Error: Invalid node type '{node_type}'.")
        return None
