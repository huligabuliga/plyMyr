# imports
from MyR_parser import parser
from semantic_analysis import check_types
from semantic_analysis import symbol_table

# code generation for the compiler


def generate_code(node):
    print(f"Processing node: {node}")

    if isinstance(node, str):
        # If the node is a string, just return it
        return node

    node_type = node[0]

    if node_type == 'program':
        children = node[1:]
        children_codes = [generate_code(child)
                          for child in children if child is not None]
        code = '\n'.join(children_codes)
        print(f"Generated code: {code}")
        return code

    elif node_type == 'assignment':
        var_name = node[1]
        value = node[2]
        if isinstance(value, tuple):
            value = generate_code(value)
        code = f"{var_name} = {value}"
        print(f"Generated code: {code}")
        return code

    elif node_type == 'binop':
        operator = node[1]
        operand1 = node[2]
        operand2 = node[3]
        code = f"{operand1} {operator} {operand2}"
        print(f"Generated code: {code}")
        return code

    elif node_type == 'variable':
        var_name = node[1]
        code = var_name
        print(f"Generated code: {code}")
        return code

    elif node_type == 'write':
        # Get the list of arguments
        args = node[1]
        # Generate code for each argument
        generated_args = [generate_code(arg) for arg in args]
        # Join the generated code for the arguments with commas
        args_code = ', '.join(generated_args)
        # Return the generated code for the write statement
        return f"print({args_code})"

    elif node_type == 'vars':
        vars = node[1]
        code = '\n'.join(
            f"DECLARE {var_type} {', '.join(names)}" for var_type, names in vars)
        print(f"Generated code: {code}")
        return code

    elif node_type == 'string':
        value = node[1]
        # Ensure that the value is enclosed in double quotes
        value = f'"{value}"'
        print(f"Generated code: {value}")
        return value

    elif node_type == 'main':
        statements = node[1]
        statements_code = [generate_code(stmt) for stmt in statements]
        code = '\n'.join(statements_code)
        print(f"Generated code: {code}")
        return code

    raise TypeError(f'Unknown node type: {node_type}')
