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

# Define a helper function for checking if a string is a float


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


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
        if isinstance(expression, str):
            if expression.isdigit():
                expression_type = 'int'
            elif is_float(expression):
                expression_type = 'float'
            elif expression.lower() in ['true', 'false']:
                expression_type = 'bool'
            else:
                expression_type = check_types(expression)
        else:
            expression_type = check_types(expression)
        if expression_type != symbol_table[var_name]:
            raise TypeError('Type mismatch in assignment')
        # Return the type of the variable
        return symbol_table[var_name]

    elif node_type == 'binop':
        operator = node[1]
        operand1 = node[2]
        operand2 = node[3]
        # Get the types of the operands
        if isinstance(operand1, str):
            if operand1.isdigit():
                operand1_type = 'int'
            elif is_float(operand1):
                operand1_type = 'float'
            elif operand1.lower() in ['true', 'false']:
                operand1_type = 'bool'
            else:
                operand1_type = symbol_table[operand1]
        if isinstance(operand2, str):
            if operand2.isdigit():
                operand2_type = 'int'
            elif is_float(operand2):
                operand2_type = 'float'
            elif operand2.lower() in ['true', 'false']:
                operand2_type = 'bool'
            else:
                operand2_type = symbol_table[operand2]
        # Use the semantic cube to determine the type of the result
        result_type = semantic_cube.get(
            (operand1_type, operand2_type, operator))
        if result_type is None:
            raise TypeError('Invalid operation for types')
        print(f"Generated code: {operand1} {operator} {operand2}")
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

    elif node_type == 'if':
        # Check the types of the condition and the body
        condition = node[1]
        body = node[2]
        condition_type = check_types(condition)
        if condition_type != 'bool':
            raise TypeError('Condition in if statement must be boolean')
        for statement in body:
            check_types(statement)

    else:
        # Recursively check the types of the children of the node
        for child in node[1:]:
            check_types(child)
