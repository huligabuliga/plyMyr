# imports
from MyR_parser import parser
from semantic_analysis import check_types
from semantic_analysis import symbol_table

# code generation for the compiler
label_counter = 0
temp_counter = 0


def generate_code(node):
    global label_counter
    global temp_counter
    code = []

    if isinstance(node, str):
        return node

    node_type = node[0]

    if node_type == 'program':
        _, _, vars_node, functions_node, main_node = node
        if vars_node is not None:
            code.append(generate_code(vars_node))
        if functions_node is not None:
            code.append(generate_code(functions_node))
        code.append(generate_code(main_node))
        return "\n".join(code)

    elif node_type == 'vars':
        _, var_declarations = node
        for var_type, var_names in var_declarations:
            for var_name in var_names:
                code.append(f"DECLARE {var_type} {var_name}")

    elif node_type == 'main':
        _, statements = node
        for statement in statements:
            statement_code = generate_code(statement)
            if isinstance(statement_code, tuple):
                code.extend(statement_code[0].split('\n'))
            else:
                code.append(statement_code)

    elif node_type == 'assignment':
        var_name, expr = node[1], node[2]
        if isinstance(expr, tuple):
            expr_code, expr_var = generate_code(expr)
            code.append(expr_code)
            code.append(f"{var_name} = {expr_var}")
        else:
            code.append(f"{var_name} = {expr}")

    elif node_type == 'binop':
        operator, operand1, operand2 = node[1], node[2], node[3]
        if isinstance(operand1, tuple):
            operand1_code, operand1_var = generate_code(operand1)
            code.append(operand1_code)
            operand1 = operand1_var
        if isinstance(operand2, tuple):
            operand2_code, operand2_var = generate_code(operand2)
            code.append(operand2_code)
            operand2 = operand2_var
        temp_counter += 1
        temp_var = f"T{temp_counter}"
        code.append(f"{temp_var} = {operand1} {operator} {operand2}")
        return "\n".join(code), temp_var

    elif node_type == 'if':
        condition, statements = node[1], node[2]
        condition_code, condition_var = generate_code(condition)
        temp_counter += 1
        temp_var = f"TB{temp_counter}"
        code.append(f"{temp_var} = {condition_var}")
        code.append(f"if {temp_var} goto L{label_counter+1}")
        code.append(f"goto L{label_counter+2}")
        code.append(f"L{label_counter+1}:")
        for statement in statements:
            statement_code = generate_code(statement)
            code.append(statement_code)
        code.append(f"L{label_counter+2}:")
        label_counter += 2

    elif node_type == 'if_else':
        condition, if_statements, else_statements = node[1:]
        condition_code, condition_var = generate_code(condition)
        code.append(condition_code)
        code.append(f"if {condition_var} goto L{label_counter+1}")
        code.append(f"goto L{label_counter+2}")
        code.append(f"L{label_counter+1}:")
        for statement in if_statements:
            statement_code = generate_code(statement)
            code.append(statement_code)
        code.append(f"goto L{label_counter+3}")
        code.append(f"L{label_counter+2}:")
        for statement in else_statements:
            statement_code = generate_code(statement)
            code.append(statement_code)
        code.append(f"L{label_counter+3}:")
        label_counter += 3

    elif node_type == 'write':
        _, args = node
        for arg in args:
            if isinstance(arg, tuple):
                arg_code, arg_var = generate_code(arg)
                code.append(arg_code)
                code.append(f"param {arg_var}")
            else:
                code.append(f"param {arg}")
        code.append(f"call print, {len(args)}")

    return "\n".join(code)
