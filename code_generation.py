# imports
from MyR_parser import parser
from semantic_analysis import check_types
from semantic_analysis import symbol_table
from semantic_analysis import function_table

# code generation for the compiler
label_counter = 0
temp_counter = 0


def generate_code(node):
    print(f"Processing node in generation: {node}")
    global label_counter
    global temp_counter
    code = []

    try:
        if isinstance(node, str):
            return node

        node_type = node[0]

        if node_type == 'program':
            _, _, vars_node, functions_node, main_node = node
            if vars_node is not None:
                print("p1", vars_node)
                code.append(generate_code(vars_node))
            # code.append("goto L1")
            if functions_node is not None:
                for function_node in functions_node:
                    print("p2", function_node)
                    function_code = generate_code(function_node)
                    if function_code is not None:
                        print("p3", function_code)
                        code.append(function_code)
            print("p4", main_node)
            code.append(generate_code(main_node))
            return "\n".join(code)

        elif node_type == 'vars':
            _, var_declarations = node
            vars_code = []
            for var_type, var_names in var_declarations:
                for var_name in var_names:
                    print("p5", var_name)
                    vars_code.append(f"DECLARE {var_type} {var_name}")
            if vars_code:  # Check if vars_code is not an empty list
                print("p6", vars_code)
                code.extend(vars_code)

        elif node_type == 'function':
            return_type, function_name, params, vars_node, body_nodes = node[1:]
            param_names = [param[1] for param in params]
            param_types = [param[0] for param in params]
            param_declarations = [f"DECLARE {param_type} {param_name}" for param_type, param_name in zip(
                param_types, param_names)]

            body_code = []
            for body_node in body_nodes:
                print("p7", body_node)
                body_node_code = generate_code(body_node)
                if isinstance(body_node_code, tuple):
                    # Check for recursive call
                    if body_node[0] == 'function_call' and body_node[1] == function_name:
                        temp_counter += 1  # Increment temp counter
                        temp_var = f"T{temp_counter}"  # Create temp variable
                        print("p8", temp_var)
                        body_code.append(
                            f"{temp_var} = callfunc {function_name} {len(body_node[2])}")
                    else:
                        print("p9", body_node_code[0].split('\n'))
                        body_code.extend(body_node_code[0].split('\n'))
                elif body_node_code is not None:  # Check if body_node_code is not None
                    print("p10", body_node_code)
                    body_code.append(body_node_code)

            return_code = ""
            for i, body_node in enumerate(body_nodes):
                if body_node[0] == 'return':
                    # return_code = generate_code(body_node)[0]
                    print("p11", return_code)
                    del body_nodes[i]
                    break

            function_code = [
                f"FUNCTION {return_type} {function_name}({', '.join(param_declarations)})",
            ]
            if vars_node is not None:
                vars_code = generate_code(vars_node)
                print("p12", vars_code)
                if vars_code:  # Check if vars_code is not an empty string
                    function_code.append(vars_code)
                    print("p13", function_code)
            function_code.extend(body_code)
            print("p14", function_code)
            # Append the return code without splitting it
            function_code.append(return_code)
            print("p15", function_code)
            function_code.append("END FUNCTION")
            print("p16", function_code)
            print("p17", "\n".join(function_code))
            return "\n".join(function_code)

        elif node_type == 'return':
            return_var = node[1]
            if isinstance(return_var, tuple):
                return_var_code, return_var = generate_code(return_var)
                print(return_var_code + "\nRETURN " + return_var)
                return f"{return_var_code}\nRETURN {return_var}"

            else:
                print("RETURN " + return_var)
                return f"RETURN {return_var}"

        elif node_type == 'main':
            _, statements = node
            label_counter += 1  # Increment label counter
            # Use label counter to create label
            # code.append(f"L{label_counter}:")
            for statement in statements:
                print("p18", statement)
                statement_code = generate_code(statement)
                print("p19", statement_code)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                    print("p20", code)
                else:
                    code.append(statement_code)
                    print("p21", code)
            label_counter += 1  # Increment label counter
            # Use label counter to create label
            code.append(f"END PROGRAM")

        elif node_type == 'function_call':
            function_name = node[1]
            args = node[2] if len(node) > 2 else []  # Adjust this line
            for arg in args:
                arg_code = generate_code(arg)
                if isinstance(arg_code, tuple):
                    code.extend(arg_code[0].split('\n'))
                    arg = arg_code[1]
                code.append(f"param {arg}")

            temp_counter += 1  # Increment temp counter
            temp_var = f"T{temp_counter}"  # Create temp variable
            code.append(f"{temp_var} = callfunc {function_name} {len(args)}")
            return "\n".join(code), temp_var

        elif node_type == 'assignment':
            var_name, expr = node[1], node[2]
            if isinstance(expr, tuple):
                if expr[0] == 'function_call':
                    # generate code for function call
                    func_call_code, func_call_var = generate_code(expr)
                    code.append(func_call_code)
                    code.append(f"{var_name} = {func_call_var}")
                else:
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
            else:
                operand1_var = operand1

            if isinstance(operand2, tuple):
                operand2_code, operand2_var = generate_code(operand2)
                code.append(operand2_code)
            else:
                operand2_var = operand2

            temp_counter += 1
            temp_var = f"T{temp_counter}"
            code.append(
                f"{temp_var} = {operand1_var} {operator} {operand2_var}")
            return "\n".join(code), temp_var

        elif node_type == 'if':
            condition, if_statements = node[1:]
            condition_code, condition_var = generate_code(condition)
            code.append(condition_code)
            code.append(f"if {condition_var} goto L{label_counter+1}")
            code.append(f"goto L{label_counter+2}")
            code.append(f"L{label_counter+1}:")
            for statement in if_statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                else:
                    code.append(statement_code)
            code.append(f"goto L{label_counter+2}")
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
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                else:
                    code.append(statement_code)
            code.append(f"goto L{label_counter+3}")
            code.append(f"L{label_counter+2}:")
            for statement in else_statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                else:
                    code.append(statement_code)
            code.append(f"L{label_counter+3}:")
            label_counter += 3

        # for loops
        elif node_type == 'for':
            var_name, start_expr, end_expr, statements = node[1:]
            start_label = label_counter
            end_label = label_counter + 1
            label_counter += 2

            # Initialize the loop variable
            code.append(f"{var_name} = {start_expr}")

            # Start label
            code.append(f"L{start_label}:")

            # Generate code for the loop condition
            temp_counter += 1  # Increment the counter
            temp_var = f"T{temp_counter}"

            code.append(f"{temp_var} = {var_name} >= {end_expr}")

            # Check the loop condition
            code.append(f"if {temp_var} goto L{end_label}")

            # Generate code for the statements inside the loop
            for statement in statements:
                statement_code = generate_code(statement)
                code.append(statement_code)

            # Go back to the start label
            code.append(f"goto L{start_label}")

            # End label
            code.append(f"L{end_label}:")

        elif node_type == 'while':
            condition, statements = node[1], node[2]
            start_label = label_counter
            end_label = label_counter + 1
            label_counter += 2

            # Start label
            code.append(f"L{start_label}:")

            # Generate code for the loop condition
            condition_code, condition_var = generate_code(condition)
            code.append(condition_code)
            code.append(f"if not {condition_var} goto L{end_label}")

            # Generate code for the statements inside the loop
            for statement in statements:
                statement_code = generate_code(statement)
                code.append(statement_code)

            # Go back to the start label
            code.append(f"goto L{start_label}")

            # End label
            code.append(f"L{end_label}:")

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
    except Exception as e:
        print(f"Error occurred during code generation: {e}")
        raise ValueError(f"Unhandled node type: {node[0]}")
        return None
