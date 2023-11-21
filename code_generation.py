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
    code = []  # quadruples

    try:
        if isinstance(node, str):
            return node

        node_type = node[0]
        if node_type == 'program':
            _, _, vars_node, functions_node, main_node = node
            # reset temp counter
            code = ["goto\t\t\tmain"]
            temp_counter = 0
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
                    # vars_code.append(f"DECLARE {var_type} {var_name}")
            if vars_code:  # Check if vars_code is not an empty list
                print("p6", vars_code)
                code.extend(vars_code)

        elif node_type == 'function':
            return_type, function_name, params, vars_node, body_nodes = node[1:]
            param_names = [param[1] for param in params]
            param_types = [param[0] for param in params]
            param_declarations = [f"DECLARE {param_type} {param_name}" for param_type, param_name in zip(
                param_types, param_names)]
            # reset temp counter
            temp_counter = 0
            body_code = []
            for body_node in body_nodes:
                body_node_code = generate_code(body_node)
                if isinstance(body_node_code, tuple):
                    # Check for recursive call
                    if body_node[0] == 'function_call' and body_node[1] == function_name:
                        temp_counter += 1  # Increment temp counter
                        temp_var = f"T{temp_counter}"  # Create temp variable
                        body_code.append(
                            f"{temp_var} = callfunc {function_name} {len(body_node[2])}")
                    else:
                        body_code.extend(body_node_code[0].split('\n'))
                elif body_node_code is not None:  # Check if body_node_code is not None
                    body_code.append(body_node_code)

            return_code = ""
            for i, body_node in enumerate(body_nodes):
                if body_node[0] == 'return':
                    del body_nodes[i]
                    break

            function_code = [
                f"FUNCTION {return_type} {function_name}({', '.join(param_declarations)})",
            ]
            function_code = []  # Initialize function_code as an empty list
            if vars_node is not None:
                vars_code = generate_code(vars_node)
                if vars_code:  # Check if vars_code is not an empty string
                    function_code.append(vars_code)
            function_code.extend(body_code)
            # Append the return code without splitting it
            function_code.append(return_code)
            function_code.append("EndFunc")
            return "\n".join(function_code)

        elif node_type == 'function_call':
            function_name = node[1]
            args = node[2] if len(node) > 2 else []  # Adjust this line
            code.append(f"ERA\t\t\t{function_name}")
            for i, arg in enumerate(args):
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    code.append(arg_code)  # Add this line
                    if isinstance(arg_code, tuple):
                        code.extend(arg_code[0].split('\n'))
                        arg = arg_var
                else:
                    arg_var = arg  # arg is a variable, not an operation
                code.append(f"param\t{arg_var}\t\tpar{i+1}")
            code.append(f"gosub\t\t\t{function_name}")
            temp_counter += 1  # Increment temp counter
            temp_var = f"T{temp_counter}"  # Create temp variable
            code.append(f"= \t {function_name}\t\t{temp_var}")
            # code.append(f"return\t\t\t{temp_var}")
            return "\n".join(code), temp_var

        elif node_type == 'main':
            _, statements = node
            # reset temp counter
            temp_counter = 0

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
            code.append(f"EndProg")

        elif node_type == 'function_call':
            function_name = node[1]
            args = node[2] if len(node) > 2 else []  # Adjust this line
            code.append(f"ERA\t\t\t{function_name}")
            for i, arg in enumerate(args):
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    code.append(arg_code)  # Add this line
                    if isinstance(arg_code, tuple):
                        code.extend(arg_code[0].split('\n'))
                        arg = arg_var
                else:
                    arg_var = arg  # arg is a variable, not an operation
                code.append(f"param\t{arg_var}\t\tpar{i+1}")
            code.append(f"gosub\t\t\t{function_name}")
            if node[0] == 'function_call':
                temp_counter += 1  # Increment temp counter only if function call is part of an operation
            temp_var = f"T{temp_counter}"  # Create temp variable
            code.append(f"= {function_name}\t\t{temp_var}")
            return "\n".join(code), temp_var
        elif node_type == 'return':
            _, expr = node
            if isinstance(expr, tuple):
                expr_code, expr_var = generate_code(expr)
                code.append(expr_code)
                code.append(f"return\t\t\t{expr_var}")
            else:
                code.append(f"return\t\t\t{expr}")
        elif node_type == 'assignment':
            var_name, expr = node[1], node[2]
            if isinstance(expr, tuple):
                if expr[0] == 'function_call':
                    # generate code for function call
                    func_call_code, func_call_var = generate_code(expr)
                    code.append(func_call_code)
                    code.append(f"=\t{func_call_var}\t{var_name}")
                else:
                    expr_code, expr_var = generate_code(expr)
                    code.append(expr_code)
                    code.append(f"=\t{expr_var}\t \t{var_name}")
            else:
                code.append(f"=\t{expr}\t{var_name}")

        elif node_type == 'binop':
            operator, operand1, operand2 = node[1], node[2], node[3]
            if isinstance(operand1, tuple):
                if operand1[0] == 'paren_expression':
                    operand1_code, operand1_var = generate_code(operand1[1])
                    code.append(operand1_code)
                    operand1_var = f"{operand1_var}"
                else:
                    operand1_code, operand1_var = generate_code(operand1)
                    code.append(operand1_code)
            else:
                operand1_var = operand1  # operand1 is a variable, not an operation

            # Do the same for operand2
            if isinstance(operand2, tuple):
                if operand2[0] == 'paren_expression':
                    operand2_code, operand2_var = generate_code(operand2[1])
                    code.append(operand2_code)
                    operand2_var = f"{operand2_var}"
                else:
                    operand2_code, operand2_var = generate_code(operand2)
                    code.append(operand2_code)
            else:
                operand2_var = operand2  # operand2 is a variable, not an operation

            temp_counter += 1  # Increment temp counter
            temp_var = f"T{temp_counter}"  # Create temp variable
            code.append(
                f"{operator}\t{operand1_var}\t{operand2_var}\t{temp_var}")
            return "\n".join(code), temp_var

        elif node_type == 'if':
            condition, if_statements = node[1:]
            condition_code, condition_var = generate_code(condition)
            code.append(condition_code)
            code.append(f"gotoF\t{condition_var}\tL{label_counter+1}")
            for statement in if_statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                elif statement_code is not None:  # Check if statement_code is not None
                    code.append(statement_code)
            code.append(f"L{label_counter+1}:")
            label_counter += 1

        elif node_type == 'if_else':
            condition, if_statements, else_statements = node[1:]
            condition_code, condition_var = generate_code(condition)
            code.append(condition_code)
            code.append(f"gotoF\t{condition_var}\t \tL{label_counter+2}")
            for statement in if_statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                elif statement_code is not None:  # Check if statement_code is not None
                    code.append(statement_code)
            code.append(f"goto\t\t\tL{label_counter+3}")
            code.append(f"L{label_counter+2}:")
            for statement in else_statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                elif statement_code is not None:  # Check if statement_code is not None
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
            temp_counter += 1  # Increment the counter
            temp_var = f"T{temp_counter}"
            code.append(f"= \t{start_expr}\t\t{temp_var}")
            code.append(f"= \t {temp_var}\t\t{var_name}")

            # Start label
            code.append(f"L{start_label}:")

            # Generate code for the loop condition
            temp_counter += 1  # Increment the counter
            temp_var = f"T{temp_counter}"

            code.append(f"<= \t {var_name}\t{end_expr}\t{temp_var}")

            # Check the loop condition
            code.append(f"gotoF {temp_var}\t\tL{end_label}")

            # Generate code for the statements inside the loop
            for statement in statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                else:
                    code.append(statement_code)

            # Increment the loop variable
            temp_counter += 1
            temp_var2 = f"T{temp_counter}"
            code.append(f"+ {var_name}\t1\t{temp_var2}")
            code.append(f"= {temp_var2}\t\t{var_name}")

            # Go back to the start label
            code.append(f"goto\t\t\tL{start_label}")

            # End label
            code.append(f"L{end_label}:")

        elif node_type == 'while':
            condition, statements = node[1], node[2]
            start_label = label_counter
            end_label = label_counter + 1
            label_counter += 2

            # Generate code for the loop condition
            condition_code, condition_var = generate_code(condition)
            code.append(condition_code)

            # Go to end label if condition is false
            code.append(f"gotoF\t{condition_var}\t\tL{end_label}")

            # Start label
            code.append(f"L{start_label}:")

            # Generate code for the statements inside the loop
            for statement in statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0].split('\n'))
                else:
                    code.append(statement_code)

            # Go back to the start label
            code.append(f"goto\t\t\tL{start_label}")

            # End label
            code.append(f"L{end_label}:")

        elif node_type == 'write':
            _, args = node
            for arg in args:
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    code.append(arg_code)
                    code.append(f"param \t\t\t{arg_var}")
                else:
                    code.append(f"param \t\t\t {arg}")
            code.append(f"write \t\t\t {len(args)}")

        return "\n".join(code)
    except Exception as e:
        print(f"Error occurred during code generation: {e}")
        raise ValueError(f"Unhandled node type: {node[0]}")
        return None
