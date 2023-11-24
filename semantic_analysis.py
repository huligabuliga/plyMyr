# Import the parser module and the parse_program function
from MyR_parser import parser
from MyR_lexer import tokens
from memorymap import MemoryMap

# Define the symbol table
symbol_table = {}
# define symbol table stack for local variables
symbol_table_stack = [{}]
# define function table
function_table = {}

# define scope of symbol table

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
    # memory map
    memory_map = MemoryMap(50)  # Adjust the size as needed
    if node is None:
        return
    if isinstance(node, int):
        return 'int'
    print('Processing node:', node)
    node_type = node[0]

    if node_type == 'program':
        # Check the types of all nodes
        for child in node[1:]:
            if isinstance(child, tuple):
                if child[0] == 'function':
                    # Process function nodes
                    check_types(child)
                elif child[0] == 'vars':
                    # Process variable nodes
                    check_types(child)
                elif child[0] == 'main':
                    # Process the main part
                    check_types(child)
            elif isinstance(child, list):
                # Process lists of function declarations
                for function in child:
                    check_types(function)

        # Process variables after functions
        for child in node[1:]:
            if isinstance(child, tuple) and child[0] == 'vars':
                # Process variable nodes
                check_types(child)

        # Process the main part after functions and variables
        for child in node[1:]:
            if isinstance(child, tuple) and child[0] == 'main':
                # Process the main part
                check_types(child)

    elif node_type == 'function':
        print(f"Processing function node: {node}")
        # add local variables to symbol table

        # symbol_table_stack.append({})
        # for param in node[3]:  # Assuming node[3] contains the function parameters
        #     param_type, param_name = param
        #     symbol_table_stack[-1][param_name] = param_type
        #     memory_map.allocate_local(param_name)
        #     print(
        #         f"Allocated local variable {param_name} at address {memory_map.get_local(param_name)}")
        # print('Finished processing node:', node)
        # print('Symbol table stack:', symbol_table_stack)

        # Add the function to the function table
        if node and len(node) > 1:
            print(f"Processing function node: {node}")
            # Add the function to the function table
            (_, return_type, function_name, params, vars, body) = node
            param_types = [param[0] for param in params]
            # Extract the names of the parameters
            param_names = [param[1] for param in params]
            param_types = [param[0] for param in params]
            # Check if vars is None before trying to access its elements
            vars_value = vars[1] if vars is not None else ""
            function_table[function_name] = {
                'return_type': return_type,
                'param_types': param_types,
                'params': param_names,
                'vars': vars_value,
            }
            # Add the parameters to the symbol table
            # for param in params:
            #     param_type, param_name = param
            #     symbol_table[param_name] = param_type
            # Add the variable name to the function table

            print('Finished processing node:', node)
            # print function table
            print('Function table:', function_table)

    # vars
    elif node_type == 'vars':
        # Add the variables to the symbol table
        for var_declaration in node[1]:
            var_type, var_names = var_declaration
            for var_name in var_names:
                if isinstance(var_name, tuple):
                    # This is an array declaration
                    array_name, array_size = var_name
                    # Convert the size to an integer
                    array_size = int(array_size)
                    symbol_table[array_name] = (var_type, array_size)
                    # memory_map.allocate_global_array(array_name, array_size)  # Commented out
                    # start_address, array_size = memory_map.get_global_array(array_name, array_size)  # Commented out
                    # print(f"Allocated global array {array_name} of size {array_size} at address {start_address}")  # Commented out
                else:
                    # This is a single variable declaration
                    symbol_table[var_name] = var_type
                    # memory_map.allocate_global(var_name)  # Commented out
                    # print(f"Allocated global variable {var_name} at address {memory_map.get_global(var_name)}")  # Commented out
        print('Finished processing node:', node)
        print('Symbol table:', symbol_table)

    elif node_type == 'assignment':
        # Check that the type of the expression matches the type of the variable
        var_name = node[1]
        expression = node[2]
        if isinstance(expression, tuple) and expression[0] == 'function_call':
            # Handle function calls
            function_name = expression[1]
            function_args = expression[2] if len(
                expression) > 2 else []  # Add this line
            # Look up the function in the function table and check the arguments
            # Check if the function has been declared
            if function_name not in function_table:
                raise NameError(f"Function '{function_name}' not declared")
            function_info = function_table[function_name]
            expected_param_types = function_info['param_types']
            if len(function_args) != len(expected_param_types):
                raise TypeError(
                    'Incorrect number of arguments in function call')
            for arg, expected_type in zip(function_args, expected_param_types):
                if arg not in symbol_table:
                    raise TypeError(f"Variable '{arg}' not defined")
                arg_type = symbol_table[arg]
                if arg_type != expected_type:
                    raise TypeError('Type mismatch in function call')
            # The type of the expression is the return type of the function
            expression_type = function_info['return_type']
        elif isinstance(expression, str):
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
        # if expression_type != symbol_table[var_name]:
        #     raise TypeError('Type mismatch in assignment')
        # Return the type of the variable
        return symbol_table[var_name]

    elif node_type == 'function_call':
        function_name = node[1]
        function_args = node[2] if len(node) > 2 else []

        # Look up the function in the function table and check the arguments
        if function_name not in function_table:
            raise NameError(f"Function '{function_name}' not declared")

        function_info = function_table[function_name]
        expected_param_types = function_info['param_types']

        if len(function_args) != len(expected_param_types):
            raise TypeError('Incorrect number of arguments in function call')

        for arg, expected_type in zip(function_args, expected_param_types):
            if isinstance(arg, tuple) and arg[0] == 'binop':
                # Handle binary operation
                left_operand = arg[2]
                right_operand = arg[3]

                # Check types of operands
                left_type = symbol_table.get(left_operand)
                right_type = symbol_table.get(right_operand)

                if left_type is None or right_type is None:
                    raise TypeError(f"Variable '{arg}' not defined")

                # Check if the types of the operands match the expected type
                if left_type != expected_type or right_type != expected_type:
                    raise TypeError('Type mismatch in function call')
            else:
                # Handle variable
                arg_type = symbol_table.get(arg)

                if arg_type is None:
                    raise TypeError(f"Variable '{arg}' not defined")

                # Check if the type of the argument matches the expected type
                if arg_type != expected_type:
                    raise TypeError('Type mismatch in function call')

        # The type of the expression is the return type of the function
        expression_type = function_info['return_type']
        return expression_type

    elif node_type == 'binop':
        operator = node[1]
        operand1 = node[2]
        operand2 = node[3]
        # Get the types of the operands
        if isinstance(operand1, tuple):
            if operand1[0] == 'function_call':
                function_name = operand1[1]
                operand1_type = function_table[function_name]['return_type']
            else:
                operand1_type = check_types(operand1)
        elif isinstance(operand1, str):
            if operand1.isdigit():
                operand1_type = 'int'
            elif is_float(operand1):
                operand1_type = 'float'
            elif operand1.lower() in ['true', 'false']:
                operand1_type = 'bool'
            else:
                operand1_type = symbol_table[operand1]
        if isinstance(operand2, tuple):
            if operand2[0] == 'function_call':
                function_name = operand2[1]
                operand2_type = function_table[function_name]['return_type']
            else:
                operand2_type = check_types(operand2)
        elif isinstance(operand2, str):
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

    # if statement
    elif node_type == 'if':
        # Check the types of the condition and the body
        condition = node[1]
        body = node[2]
        condition_type = check_types(condition)
        if condition_type != 'bool':
            raise TypeError('Condition in if statement must be boolean')
        for statement in body:
            check_types(statement)

    # for statement
    elif node_type == 'for':
        # The loop variable is a temporary variable used only inside the for loop
        var_name = node[1]
        symbol_table[var_name] = 'int'

        # Check that the start and end expressions are integers
        start_expr = node[2]
        end_expr = node[3]
        if not start_expr.isdigit() or not end_expr.isdigit():
            raise TypeError(f"Invalid loop range {start_expr} to {end_expr}")

        # Check that the statements inside the loop are valid and well-formed
        for statement in node[4]:
            check_types(statement)

        # Remove the loop variable from the symbol table after the loop
        del symbol_table[var_name]

    else:
        # Recursively check the types of the children of the node
        for child in node[1:]:
            if child[0] not in ['assignment', 'vars']:
                check_types(child)

    # print whats in memory map
    print('Memory map:', memory_map)
    # print variables that are in the memory map
    print('Global variables in memory map:', memory_map.global_vars)
    print('Local variables in memory map:', memory_map.local_vars)

    # Assuming symbol_table and memory_map are defined and initialized
    for var_name, var_type in symbol_table.items():
        if isinstance(var_type, tuple):
            # This is an array declaration
            array_type, array_size = var_type
            memory_map.allocate_global_array(var_name, array_size)
            start_address, array_size = memory_map.get_global_array(
                var_name, array_size)
            print(
                f"Allocated global array {var_name} of size {array_size} at address {start_address}")
        else:
            # This is a single variable declaration
            memory_map.allocate_global(var_name)
            print(
                f"Allocated global variable {var_name} at address {memory_map.get_global(var_name)}")

    # Assuming function_table and memory_map are defined and initialized
    # for function_name, function_info in function_table.items():
    #     for param_name in function_info['params']:
    #         memory_map.allocate_local(param_name)

    return memory_map
