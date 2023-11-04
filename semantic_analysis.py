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

# Define a helper function for checking types


def check_types(node):
    if node is None:
        return
    if isinstance(node, int):
        return 'int'
    print('Processing node:', node)
    node_type = node[0]

    if node_type == 'program':
        # Check the types of the global variables, functions, and main
        for child in node[2:]:
            check_types(child)

    # vars
    elif node_type == 'vars':
        # Add the variables to the symbol table
        for var_declaration in node[1]:
            var_type, var_names = var_declaration
            for var_name in var_names:
                symbol_table[var_name] = var_type
        print('Finished processing node:', node)
        print('Symbol table:', symbol_table)

    # function
    elif node_type == 'function':
        if node and len(node) > 1:
            # Add the parameters to the symbol table
            for function in node[1]:
                if len(function) >= 2:
                    function_type, function_name = function
                    symbol_table[function_name] = function_type
            print('Finished processing node:', node)

    elif node_type == 'assignment':
        # Check that the type of the expression matches the type of the variable
        var_name = node[1]
        expression = node[2]
        if isinstance(expression, str) and expression.isdigit():  # Modify this line
            expression_type = 'int'  # Add this line
        else:
            expression_type = check_types(expression)
        if expression_type != symbol_table[var_name]:
            raise TypeError('Type mismatch in assignment')
        # Return the type of the variable
        return symbol_table[var_name]

    elif node_type == 'binop':
        # Check that the operation is valid for the types of the operands
        operator = node[1]
        left = node[2]
        right = node[3]
        left_type = check_types(left)
        right_type = check_types(right)
        result_type = semantic_cube.get((left_type, right_type, operator))
        if result_type is None:
            raise TypeError('Invalid operation for types')
        return result_type

    elif node_type == 'variable':
        # Check that the variable is in the symbol table
        var_name = node[1]
        if var_name not in symbol_table:
            raise NameError('Undefined variable')
        return symbol_table[var_name]

    elif node_type == 'constant':
        # Return the type of the constant
        return node[1]

    else:
        # Recursively check the types of the children of the node
        for child in node[1:]:
            check_types(child)
