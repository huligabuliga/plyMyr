# imports
from MyR_parser import parser
from semantic_analysis import check_types
from semantic_analysis import symbol_table
from semantic_analysis import function_table

# code generation for the compiler
label_counter = 0
temp_counter = 0
temp_counter_int = 0
temp_counter_float = 0
temp_counter_bool = 0

# stacks for the compiler
# local variables
local_stack = []
# global variables
global_stack = []
# temp variables
temp_int_stack = []
temp_float_stack = []
temp_bool_stack = []
# constant variables
constant_stack = []
# function variables
function_stack = []


# void functions:


# def flatten(lst):
#     result = []
#     for i in lst:
#         if isinstance(i, (list, tuple)):
#             result.extend(flatten(i))
#         else:
#             result.append(i)
#     return result


def is_void(function_name, function_table):
    return function_table[function_name]['return_type'] == 'void'


def generate_code(node):
    print(f"Processing node in generation: {node}")
    global label_counter
    global temp_counter
    global temp_counter_int
    global temp_counter_float
    global temp_counter_bool
    code = []  # quadruples

    try:
        if isinstance(node, str):
            return node

        node_type = node[0]
        if node_type == 'program':
            _, _, vars_node, functions_node, main_node = node
            # reset temp counter
            code = [("goto", "", "", "start_main")]
            temp_counter = 0
            temp_int_counter = 0
            temp_float_counter = 0
            temp_bool_counter = 0
            if vars_node is not None:
                print("p1", vars_node)
                code.extend(generate_code(vars_node))
            if functions_node is not None:
                for function_node in functions_node:
                    print("p2", function_node)
                    code.append(("label", "", "", function_node[2]))
                    function_code = generate_code(function_node)
                    if function_code is not None:
                        print("p3", function_code)
                        code.extend(function_code)
            print("p4", main_node)
            code.extend(generate_code(main_node))
            return code

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
            param_declarations = [(param_type, param_name, "", "")
                                  for param_type, param_name in zip(param_types, param_names)]
            # Flatten the list of param_declarations
            param_declarations = [
                item for sublist in param_declarations for item in sublist]
            # reset temp counter
            temp_counter = 0
            body_code = []
            for body_node in body_nodes:
                body_node_code = generate_code(body_node)
                if body_node_code is not None:  # Check if body_node_code is not None
                    body_code.extend(body_node_code)

            return_code = []
            for i, body_node in enumerate(body_nodes):
                if body_node[0] == 'return':
                    del body_nodes[i]
                    break

            # Skip adding the function declaration to the quadruples
            function_code = []
            if vars_node is not None:
                vars_code = generate_code(vars_node)
                if vars_code:  # Check if vars_code is not an empty list
                    function_code.extend(vars_code)
            function_code.extend(body_code)
            # Append the return code without splitting it
            function_code.extend(return_code)
            function_code.append(("EndFunc", "", "", ""))
            return function_code

        elif node_type == 'function_call':
            function_name = node[1]
            function_args = node[2]
            args = node[2] if len(node) > 2 else []  # Adjust this line
            code.append(("ERA", function_name, "", ""))
            for i, arg in enumerate(args):
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    code.extend(arg_code)  # Add this line
                    arg = arg_var
                else:
                    arg_var = arg  # arg is a variable, not an operation
                code.append(("param", arg_var, "", f"par{i+1}"))
            code.append(("gosub", "", "", function_name))

            # Determine the type of the temporary variable
            function_return_type = function_table.get(
                function_name, {}).get('return_type', 'unknown')
            if function_return_type == 'int':
                temp_counter_int += 1
                temp_var = f"Ti{temp_counter_int}"
            elif function_return_type == 'float':
                temp_counter_float += 1
                temp_var = f"Tf{temp_counter_float}"
            elif function_return_type == 'bool':
                temp_counter_bool += 1
                temp_var = f"Tb{temp_counter_bool}"
            elif function_return_type == 'void':
                temp_var = None
            else:
                raise ValueError(
                    f"Unsupported return type: {function_return_type}")

            if not is_void(function_name, function_table):
                code.append(("=", function_name, "", temp_var))
                return code, temp_var
            else:
                return code

        elif node_type == 'main':
            _, statements = node
            # reset temp counter
            temp_counter = 0

            label_counter += 1  # Increment label counter

            # Initialize code as an empty list
            code = [("label", "", "", "start_main")]
            for statement in statements:
                print("p18", statement)
                statement_code = generate_code(statement)
                print("p19", statement_code)
                if statement_code is not None:  # Check if statement_code is not None
                    code.append(statement_code)
                    print("p20", code)

            label_counter += 1  # Increment label counter
            code.append(("EndProg", "", "", ""))
            return code

        elif node_type == 'return':
            _, expr = node
            code = []
            if isinstance(expr, tuple):
                expr_code, expr_var = generate_code(expr)
                if expr_code is not None:  # Check if expr_code is not None
                    code.extend(expr_code)
                code.append(("return", "", "", expr_var))
            else:
                code.append(("return", "", "", expr))
            return code

        elif node_type == 'assignment':
            if len(node) == 4:
                # This is an array assignment
                array_name, array_index, expr = node[1], node[2], node[3]
                code = []
                # Check if the array index is a single digit
                if isinstance(array_index, str) and array_index.isdigit():
                    # The index is a single digit, use it directly
                    index_var = array_index
                else:
                    # The index is not a single digit, generate code for it
                    index_code, index_var = generate_code(array_index)
                    if index_code is not None:
                        code.append(index_code)
                # Generate code for the expression
                if isinstance(expr, tuple) and expr[0] == 'binop':
                    # Create a pointer for the array at the specific index
                    pointer_name = f"tp{index_var}"
                    code.append(
                        ("pointer_assign", pointer_name, array_name, index_var))
                    # Perform the binary operation
                    binop_code, binop_var = generate_code(expr)
                    if binop_code is not None:
                        code.append(binop_code)
                    # Assign the result to the pointer
                    code.append(
                        ("assign_pointer", pointer_name, "", binop_var))
                else:
                    # Generate code for the array assignment
                    code.append(("array_assign", array_name, index_var, expr))
            else:
                # This is a non-array assignment
                var_name, expr = node[1], node[2]
                code = []
                if isinstance(expr, tuple):
                    expr_code, expr_var = generate_code(expr)
                    if expr_code is not None:  # Check if expr_code is not None
                        code.append(expr_code)
                    code.append(("=", expr_var, "", var_name))
                else:
                    code.append(("=", expr, "", var_name))
            return code

        elif node_type == 'binop':
            operator, operand1, operand2 = node[1], node[2], node[3]
            code = []
            if isinstance(operand1, tuple):
                if operand1[0] == 'paren_expression':
                    operand1_code, operand1_var = generate_code(operand1[1])
                    if operand1_code is not None:  # Check if operand1_code is not None
                        code.extend(operand1_code)
                else:
                    operand1_code, operand1_var = generate_code(operand1)
                    if operand1_code is not None:  # Check if operand1_code is not None
                        code.extend(operand1_code)
            else:
                operand1_var = operand1  # operand1 is a variable, not an operation

            # Do the same for operand2
            if isinstance(operand2, tuple):
                if operand2[0] == 'paren_expression':
                    operand2_code, operand2_var = generate_code(operand2[1])
                    if operand2_code is not None:  # Check if operand2_code is not None
                        code.extend(operand2_code)
                else:
                    operand2_code, operand2_var = generate_code(operand2)
                    if operand2_code is not None:  # Check if operand2_code is not None
                        code.extend(operand2_code)
            else:
                operand2_var = operand2  # operand2 is a variable, not an operation

            operand1_type = symbol_table.get(operand1_var, 'unknown')
            operand2_type = symbol_table.get(operand2_var, 'unknown')

            # Determine the type of the temporary variable
            if operator in ['==', '!=', '<', '>', '<=', '>=']:  # Boolean operations
                temp_counter_bool += 1
                temp_var = f"Tb{temp_counter_bool}"
            elif operator in ['+', '-', '*', '/']:  # Arithmetic operations
                # If either operand is a float, the result will be a float
                if operand1_type == 'float' or operand2_type == 'float':
                    temp_counter_float += 1
                    temp_var = f"Tf{temp_counter_float}"
                else:  # Otherwise, the result will be an int
                    temp_counter_int += 1
                    temp_var = f"Ti{temp_counter_int}"
            else:
                raise ValueError(f"Unsupported operator: {operator}")

            code.append((operator, operand1_var, operand2_var, temp_var))
            return code, temp_var

        elif node_type == 'if':
            condition, if_statements = node[1:]
            condition_code, condition_var = generate_code(condition)
            if condition_code is not None:  # Check if condition_code is not None
                code.extend(condition_code)
            code.append(("gotoF", condition_var, "", f"L{label_counter+1}"))
            for statement in if_statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, list):
                    code.extend(statement_code)
                elif statement_code is not None:  # Check if statement_code is not None
                    code.append(statement_code)
            code.append(("label", "", "", f"L{label_counter+1}"))
            label_counter += 1

        elif node_type == 'if_else':
            condition, if_statements, else_statements = node[1:]
            condition_code, condition_var = generate_code(condition)
            if condition_code is not None:  # Check if condition_code is not None
                code.extend(condition_code)
            code.append(("gotoF", condition_var, "", f"L{label_counter+2}"))
            for statement in if_statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0])
                elif statement_code is not None:  # Check if statement_code is not None
                    code.append(statement_code)
            code.append(("goto", "", "", f"L{label_counter+3}"))
            code.append(("label", "", "", f"L{label_counter+2}"))
            for statement in else_statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0])
                elif statement_code is not None:  # Check if statement_code is not None
                    code.append(statement_code)
            code.append(("label", "", "", f"L{label_counter+3}"))
            label_counter += 3

        # for loops

         # for loops
        elif node_type == 'for':
            var_name, start_expr, end_expr, statements = node[1:]
            start_label = label_counter
            end_label = label_counter + 1
            label_counter += 2
            # start for loop
            code.append(("for", "", "", var_name))
            # Initialize the loop variable
            code.append(("=", start_expr, "", var_name))

            # Start label
            code.append(("label", "", "", f"L{start_label}"))

            # Generate code for the loop condition
            temp_counter_int += 1  # Increment temp counter
            temp_var = f"Ti{temp_counter_int}"  # Create temp variable
            code.append(("<=", var_name, end_expr, temp_var))

            # Check the loop condition
            code.append(("gotoF", temp_var, "", f"L{end_label}"))

            # Generate code for the statements inside the loop
            for statement in statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0])
                elif statement_code is not None:  # Check if statement_code is not None
                    code.append(statement_code)

            # Increment the loop variable
            temp_counter_int += 1  # Increment temp counter
            temp_var = f"Ti{temp_counter_int}"  # Create temp variable
            code.append(("+", var_name, "1", temp_var))
            code.append(("=", temp_var, "", var_name))

            # Go back to the start label
            code.append(("goto", "", "", f"L{start_label}"))

            # End label
            code.append(("label", "", "", f"L{end_label}"))

            # end for
            code.append(("endfor", "", "", var_name))

        elif node_type == 'while':
            condition, statements = node[1], node[2]
            start_label = label_counter
            end_label = label_counter + 1
            label_counter += 2

            # Start label
            code.append(("label", "", "", f"L{start_label}"))

            # Generate code for the loop condition
            condition_code, condition_var = generate_code(condition)
            if condition_code is not None:  # Check if condition_code is not None
                code.extend(condition_code)

            # Go to end label if condition is false
            code.append(("gotoF", condition_var, "", f"L{end_label}"))

            # Generate code for the statements inside the loop
            for statement in statements:
                statement_code = generate_code(statement)
                if isinstance(statement_code, tuple):
                    code.extend(statement_code[0])
                elif statement_code is not None:  # Check if statement_code is not None
                    code.append(statement_code)

            # Go back to the start label
            code.append(("goto", "", "", f"L{start_label}"))

            # End label
            code.append(("label", "", "", f"L{end_label}"))

        elif node_type == 'write':
            _, args = node
            for arg in args:
                if isinstance(arg, tuple):
                    if arg[0] == 'array_element':
                        # Generate code to load array element into a temporary variable
                        array_name, index = arg[1], arg[2]
                        temp_counter_int += 1
                        # assign int temp variable
                        temp_var = f"Ti{temp_counter_int }"
                        code.append(("load", array_name, index, temp_var))
                        code.append(("param", "", "", temp_var))
                    else:
                        arg_code, arg_var = generate_code(arg)
                        if arg_code is not None:  # Check if arg_code is not None
                            code.extend(arg_code)
                        code.append(("param", "", "", arg_var))
                else:
                    code.append(("param", "", "", arg))
            code.append(("write", "", "", len(args)))

        elif node_type == 'read':
            _, args = node
            for arg in args:
                code.append(("read", "", "", arg))

        # ---- grafics -------- #

        elif node_type == 'circle':
            _, args = node
            if isinstance(args, str):  # If there's only one argument and it's a string
                args = [args]  # Convert it to a list
            for arg in args:
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    if arg_code is not None:  # Check if arg_code is not None
                        code.extend(arg_code)
                    code.append(("param", "", "", arg_var))
                else:
                    code.append(("param", "", "", arg))
            code.append(("circle", "", "", len(args)))

        elif node_type == 'line':
            _, args = node
            if isinstance(args, str):  # If there's only one argument and it's a string
                args = [args]  # Convert it to a list
            for arg in args:
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    if arg_code is not None:  # Check if arg_code is not None
                        code.extend(arg_code)
                    code.append(("param", "", "", arg_var))
                else:
                    code.append(("param", "", "", arg))
            code.append(("line", "", "", len(args)))

        elif node_type == 'color':
            _, args = node
            if isinstance(args, str):
                # Remove the double quotes from the color string
                args = [args.strip('"')]
            for arg in args:
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    if arg_code is not None:
                        code.extend(arg_code)
                    code.append(("param", "", "", arg_var))
                else:
                    code.append(("param", "", "", arg))
            code.append(("color", "", "", len(args)))

        elif node_type == 'point':
            _, args = node
            if isinstance(args, str):  # If there's only one argument and it's a string
                args = [args]  # Convert it to a list
            for arg in args:
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    if arg_code is not None:  # Check if arg_code is not None
                        code.extend(arg_code)
                    code.append(("param", "", "", arg_var))
                else:
                    code.append(("param", "", "", arg))
            code.append(("point", "", "", len(args)))

        elif node_type == 'thickness':
            _, args = node
            if isinstance(args, str):
                args = [args]
            for arg in args:
                if isinstance(arg, tuple):
                    arg_code, arg_var = generate_code(arg)
                    if arg_code is not None:
                        code.extend(arg_code)
                    code.append(("param", "", "", arg_var))
                else:
                    code.append(("param", "", "", arg))
            code.append(("thickness", "", "", len(args)))

        elif node_type == 'penup':
            code.append(("penup", "", "", ""))

        elif node_type == 'pendown':
            code.append(("pendown", "", "", ""))

        return (code)
    except Exception as e:
        print(f"Error occurred during code generation: {e}")
        print(f"Node causing the error: {node}")
        raise e
        raise ValueError(f"Unhandled node type: {node[0]}")
        return None
