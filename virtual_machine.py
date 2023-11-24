from memorymap import MemoryMap

# Description: Virtual machine for the compiler
from semantic_analysis import symbol_table
from semantic_analysis import function_table

import turtle  # for turtle graphics


class VirtualMachine:
    def __init__(self, code, memory_map, function_table, symbol_table):
        self.code = code
        self.memory_map = memory_map
        self.pc = 0  # Program counter
        self.stack = []  # Stack for function calls
        self.return_value = None  # Return value of a function
        self.call_stack = []  # Stack for function calls
        self.function_name_stack = []  # stack of function names
        self.log = []

    # logging
    def log_message(self, *args):
        message = ' '.join(str(arg) for arg in args)
        self.log.append(message)

    def write_log_to_file(self, filename):
        with open(filename, 'w') as f:
            for message in self.log:
                f.write(message + '\n')

    # local and global getters

    def is_local(self, var):
        return var in self.memory_map.local_vars

    def is_global(self, var):
        return var in self.memory_map.global_vars

    # helper functions for repetitve code

    def get_value(self, arg):
        self.log_message("get_value started")
        self.log.append("memory_map in get value: " +
                        str(self.memory_map.memory))
        self.log_message("receiving, getting value of ", arg)
        try:
            return float(arg) if '.' in arg else int(arg)
        except ValueError:
            if arg.startswith(('Ti', 'Tf', 'Tb')):
                arg_value = self.memory_map.get_value(
                    self.memory_map.get_temp(arg))
                if arg_value is None:
                    raise ValueError(
                        f"Temporary variable {arg} is not defined")
            else:
                if arg in self.memory_map.local_vars[-1]:
                    self.log_message("get_value: found in local_vars")
                    address = self.memory_map.get_local(arg)
                    self.log_message("get_Value: address", address)
                    arg_value = self.memory_map.get_value(address)
                    if arg_value is None:
                        raise ValueError(
                            f"Local variable {arg} is not defined")
                elif arg in self.memory_map.global_vars:
                    arg_value = self.memory_map.get_value(
                        self.memory_map.get_global(arg))
                    if arg_value is None:
                        raise ValueError(
                            f"Global variable {arg} is not defined")
                else:
                    raise ValueError(
                        f"Variable {arg} is not defined in global_vars or local_vars")
            return float(arg_value) if '.' in str(arg_value) else int(arg_value)

    def perform_operation(self, op, result, arg1, arg2):

        self.log_message("perform_operation ended")
        self.log_message(f"{op} node detected")
        if result.startswith(('Ti', 'Tf', 'Tb')) and not self.memory_map.exists_temp(result):
            self.log_message("new temporal variable detected")
            self.memory_map.declare_temp(result)
            self.log_message("Declared temp variable: ", result)

        if result in self.memory_map.temp_vars_int or result in self.memory_map.temp_vars_float or result in self.memory_map.temp_vars_bool:
            arg1_value = self.get_value(arg1)
            self.log_message("getting arg1 value: ", arg1_value)
            arg2_value = self.get_value(arg2)
            self.log_message("getting arg2 value: ", arg2_value)

            if arg1_value is not None and arg2_value is not None:
                if op == "+":
                    self.memory_map.set_value(self.memory_map.get_temp(
                        result), arg1_value + arg2_value)
                    self.log_message("arg1_value", arg1_value, "arg2_value:",
                                     arg2_value, "sum is", arg1_value + arg2_value)
                elif op == "-":
                    self.memory_map.set_value(self.memory_map.get_temp(
                        result), arg1_value - arg2_value)
                    self.log.append(
                        "memory_map in perform_operation get  +: " + str(self.memory_map.memory))
                    self.log_message("arg1_value", arg1_value, "arg2_value:",
                                     arg2_value, "difference is", arg1_value - arg2_value)
                elif op == "*":
                    self.memory_map.set_value(self.memory_map.get_temp(
                        result), arg1_value * arg2_value)
                    self.log_message("arg1_value", arg1_value, "arg2_value:",
                                     arg2_value, "product is", arg1_value * arg2_value)
                elif op == "/":
                    self.memory_map.set_value(self.memory_map.get_temp(
                        result), arg1_value / arg2_value)
                    self.log_message("arg1_value", arg1_value, "arg2_value:",
                                     arg2_value, "quotient is", arg1_value / arg2_value)

    # def get_arg_value(self, arg):
    #     if isinstance(arg, str) and not arg.isdigit():
    #         if self.memory_map.get_local(arg):
    #             return self.memory_map.get_value(self.memory_map.get_local(arg))
    #         else:
    #             return self.memory_map.get_value(self.memory_map.get_global(arg))
    #     else:
    #         return int(arg) if isinstance(arg, str) else arg

    def perform_comparison(self, op, result, arg1, arg2):
        self.log_message("perform_comparison started")

        arg1_value = self.get_value(arg1)
        arg2_value = self.get_value(arg2)
        if arg1_value is None or arg2_value is None:
            self.log_message("Error: One of the arguments is None")
            return
        self.memory_map.declare_temp(result)

        if op == "==":
            self.log_message("== node detected")
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value == arg2_value)
            self.log_message("arg1_value", arg1_value, "arg2_value:",
                             arg2_value, "== is", arg1_value == arg2_value)
        elif op == "!=":
            self.log_message("!= node detected")
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value != arg2_value)
        elif op == ">":
            self.log_message("> node detected")
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value > arg2_value)
        elif op == "<":
            self.log_message("< node detected")
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value < arg2_value)
        elif op == ">=":
            self.log_message(">= node detected")
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value >= arg2_value)
        elif op == "<=":
            self.log_message("<= node detected")
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value <= arg2_value)

    def run(self):
        self.log_message("run started")
        # enter scope
        # self.memory_map.enter_scope()
        while self.pc < len(self.code):
            op, arg1, arg2, result = self.code[self.pc]
            self.pc += 1
            self.log_message("pc = ", self.pc)
        # when done exit scope
        # self.memory_map.exit_scope()
            if op == "=":
                self.log_message("equal node detected")
                self.log_message("arg1: ", arg1)
                self.log_message("arg2: ", arg2)
                self.log_message("result: ", result)
                # Determine where to get the value from for arg1
                if arg1.lower() == 'true':
                    arg1_value = True
                elif arg1.lower() == 'false':
                    arg1_value = False
                elif arg1.startswith(('Ti', 'Tf')):
                    arg1_value = self.memory_map.get_value(
                        self.memory_map.get_temp(arg1))
                    if '.' in str(arg1_value):
                        arg1_value = float(arg1_value)
                    else:
                        arg1_value = int(arg1_value)
                elif arg1 in self.memory_map.global_vars or (self.memory_map.local_vars and arg1 in self.memory_map.local_vars[-1]):
                    arg1_value = self.memory_map.get_value(
                        self.memory_map.get_global(arg1) if arg1 in self.memory_map.global_vars else self.memory_map.get_local(arg1))
                else:
                    try:
                        arg1_value = float(arg1) if '.' in arg1 else int(arg1)
                    except ValueError:
                        self.log_message(
                            f"Error: {arg1} is not a valid number or variable")
                        continue

                # Check if the result is a temporary variable and declare it if it's not already declared
                if result.startswith(('Ti', 'Tf')) and not self.memory_map.exists_temp(result):
                    self.log_message("Declaring temp variable: ", result)
                    self.memory_map.declare_temp(result)

                # Assign the value to the result
                if result.startswith(('Ti', 'Tf')):
                    self.log_message("Assigning value to a temporal variable")
                    self.memory_map.set_value(
                        self.memory_map.get_temp(result), arg1_value)
                    self.log_message("Value of ", result, " is now ", self.memory_map.get_value(
                        self.memory_map.get_temp(result)))
                elif result in self.memory_map.global_vars:
                    self.log_message("Assigning value to global variable")
                    self.memory_map.set_value(
                        self.memory_map.get_global(result), arg1_value)
                    self.log_message("Value of ", result, " is now ", self.memory_map.get_value(
                        self.memory_map.get_global(result)))
                elif self.memory_map.local_vars and result in self.memory_map.local_vars[-1]:
                    self.log_message("Assigning value to local variable")
                    self.memory_map.set_value(
                        self.memory_map.get_local(result), arg1_value)
                    self.log_message("Value of ", result, " is now ", self.memory_map.get_value(
                        self.memory_map.get_local(result)))
                    # print local vars to debug
                    self.log_message(
                        "local_vars: ", self.memory_map.local_vars)
                    # prints local memory map to debug
                    self.log_message("memory map after =: ",
                                     self.memory_map.memory)
                else:
                    self.log_message(
                        f"Error: Variable {result} is not defined")
                self.log_message("equal node end")
            # ------ Arithmetic Operations ------#
            # ------ + - * / ------#
            elif op == "+":
                self.log_message("add node detected")

                self.perform_operation(op, result, arg1, arg2)
            elif op == "-":
                self.log_message("subtract node detected")

                self.perform_operation(op, result, arg1, arg2)
            elif op == "*":
                self.log_message("multiply node detected")

                self.perform_operation(op, result, arg1, arg2)
            elif op == "/":
                self.log_message("divide node detected")

                self.perform_operation(op, result, arg1, arg2)

            # ------ boolean Operations ------#
            # ------ and or ------#
            # ------ > >= <= < == != ------#
            # ------ gotoF goto label ------#
            elif op == ">":
                self.log_message("greater than node detected")
                self.perform_comparison(op, result, arg1, arg2)
            elif op == ">=":
                self.log_message("greater than or equal node detected")
                self.perform_comparison(op, result, arg1, arg2)
            elif op == "<":
                self.log_message("less than node detected")
                self.perform_comparison(op, result, arg1, arg2)
            elif op == "<=":
                self.log_message("less than or equal node detected")
                self.perform_comparison(op, result, arg1, arg2)
            elif op == "==":
                self.log_message("equal node detected")
                self.perform_comparison(op, result, arg1, arg2)
            elif op == "!=":
                self.log_message("not equal node detected")
                self.perform_comparison(op, result, arg1, arg2)

            # ------ for and while Operations ------#
            elif op == 'for':
                self.log_message("for node detected")
                # Enter a new scope and declare the loop variable
                self.memory_map.enter_scope()
                self.memory_map.allocate_local(result)
                # self.pc += 1
            elif op == 'endfor':
                self.log_message("endfor node detected")
                # Exit the current scope
                self.memory_map.exit_scope()
                # self.pc += 1

            elif op == "gotoF":
                self.log_message("gotoF node detected")
                if arg1 in self.memory_map.temp_vars_int or arg1 in self.memory_map.temp_vars_float or arg1 in self.memory_map.temp_vars_bool:
                    arg1_value = self.memory_map.get_value(
                        self.memory_map.get_temp(arg1))
                else:
                    arg1_value = self.memory_map.get_value(
                        self.memory_map.get_global(arg1))
                if not arg1_value:
                    # Find the index of the label in the code
                    label_index = next(i for i, instruction in enumerate(
                        self.code) if instruction[0] == "label" and instruction[3] == result)
                    self.pc = label_index
                continue
                break

            elif op == "goto":
                self.log_message("goto node detected")
                # Find the index of the label in the code
                label_index = next(i for i, instruction in enumerate(
                    self.code) if instruction[0] == "label" and instruction[3] == result)
                self.pc = label_index

            elif op == "label":
                self.log_message("label node detected")
                pass

            elif op == "param":
                self.log_message("param node start")
                # print memory map to debug
                self.log_message("memory_map: ", self.memory_map.memory)
                # print stack to debug
                self.log_message("stack: ", self.stack)
                # print result to debug
                self.log_message("result: ", result)
                # print arg1 to debug
                self.log_message("arg1: ", arg1)
                # print arg2 to debug
                self.log_message("arg2: ", arg2)
                # print global vars to debug
                self.log_message("global_vars: ", self.memory_map.global_vars)
                # print local vars to debug
                self.log_message("local_vars: ", self.memory_map.local_vars)
                # print temp vars to debug
                self.log_message("temp_vars: ", self.memory_map.temp_vars_int,
                                 self.memory_map.temp_vars_float, self.memory_map.temp_vars_bool)

                if arg1 != '':
                    # If arg1 is not an empty string, check if it exists in global_vars
                    if arg1 in self.memory_map.local_vars[-1]:
                        self.log_message("get_value: found in local_vars")
                        address = self.memory_map.get_local(arg1)
                        self.log_message("get_Value: address", address)
                        arg_value = self.memory_map.get_value(address)
                        self.log_message("get_Value: arg_value", arg_value)
                        self.stack.append(arg_value)

                    elif arg1 in self.memory_map.global_vars:
                        self.log_message("arg 1 found in global_vars", arg1)
                        # If arg1 exists in global_vars, get its value and push it onto the stack
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_global(arg1)))

                    elif arg1 in self.memory_map.temp_vars_int or arg1 in self.memory_map.temp_vars_float or arg1 in self.memory_map.temp_vars_bool:
                        self.log_message("found in temp_vars")
                        # If arg1 exists in temp_vars, get its value and push it onto the stack
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_temp(arg1)))
                    else:
                        # If arg1 does not exist in global_vars, treat it as a literal value and push it onto the stack
                        self.log_message("adding arg1 to stack: ", arg1)
                        self.stack.append(arg1)
                else:
                    # If arg1 is an empty string, push the value of result directly onto the stack
                    # If arg1 is an empty string, push the value of result directly onto the stack
                    if result.startswith('"') and result.endswith('"'):
                        # If result is a string literal (enclosed in quotes), push it directly onto the stack
                        self.stack.append(result)
                    # elif result in self.memory_map.local_vars[-1]:
                    #     self.log_message("get_value: found in local_vars")
                    #     address = self.memory_map.get_local(result)
                    #     self.log_message("get_Value: address", address)
                    #     arg_value = self.memory_map.get_value(address)
                    #     self.log_message("get_Value: arg_value", arg_value)
                    #     self.stack.append(arg_value)

                    elif result in self.memory_map.global_vars:
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_global(result)))
                    elif result in self.memory_map.temp_vars_int or result in self.memory_map.temp_vars_float or result in self.memory_map.temp_vars_bool:
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_temp(result)))

                    else:
                        self.stack.append(result)
                self.log_message("stack: ", self.stack)
                self.log_message("memory_map after param: ",
                                 self.memory_map.memory)
                self.log_message("param node end")
                # debug stack

            # ------ read and write Operations ------#
            elif op == "write":
                # self.log("memory_map in write: ", self.memory_map.memory)
                self.log_message("write node detected")
                values = [self.stack.pop() for _ in range(result)]
                for value in reversed(values):
                    print(value, end=' ')
                print()
                # self.log("memory_map after write: ", self.memory_map.memory)
            elif op == "read":
                # Get user input
                value = int(input("Enter a value for " + result + ": "))
                # Check if the result is a temporary variable and declare it if it's not already declared
                if result.startswith(('Ti', 'Tf')) and not self.memory_map.exists_temp(result):
                    self.memory_map.declare_temp(result)
                    # Assign the value to the result
                    self.memory_map.set_value(
                        self.memory_map.get_temp(result), value)
                elif result in self.memory_map.global_vars:
                    self.memory_map.set_value(
                        self.memory_map.get_global(result), value)
                elif result in self.memory_map.local_vars[-1]:
                    self.memory_map.set_value(
                        self.memory_map.get_local(result), value)
                else:
                    raise ValueError(
                        f"Variable {result} is not defined in global_vars or local_vars")

            # ------ turtle Operations ------#
            elif op == "circle":
                self.log_message("circle node detected")
                values = [self.stack.pop() for _ in range(result)]
                for value in reversed(values):
                    turtle.circle(value)
            elif op == "line":
                self.log_message("line node detected")
                values = [self.stack.pop() for _ in range(result)]
                for value in reversed(values):
                    turtle.forward(value)
            elif op == "color":
                self.log_message("color node detected")
                values = [self.stack.pop() for _ in range(result)]
                for value in reversed(values):
                    turtle.color(value)
            elif op == "point":
                self.log_message("point node detected")
                values = [self.stack.pop() for _ in range(result)]
                for value in reversed(values):
                    turtle.dot(value)
            elif op == "penup":
                self.log_message("penup node detected")
                turtle.penup()
            elif op == "pendown":
                self.log_message("pendown node detected")
                turtle.pendown()
            elif op == "thickness":
                self.log_message("thickness node detected")
                values = [self.stack.pop() for _ in range(result)]
                for value in reversed(values):
                    turtle.pensize(value)

                # ------ Functions------#
                # handle function local variables
            elif op == "ERA":
                self.log_message("ERA node detected")
                self.log_message("memory map before ERA: ",
                                 self.memory_map.memory)
                self.log_message("memory_map: ", self.memory_map.memory)
                # Enter a new scope
                self.memory_map.enter_scope()
                self.log_message("function info", function_table[arg1])
                # log memory map
                self.log_message("memory_map after era: ",
                                 self.memory_map.memory)
                self.log_message("local_vars: ", self.memory_map.local_vars)
                # Add the local variables for the function to the MemoryMap
                function_info = function_table[arg1]
                self.log_message("function info", function_info)
                for var_name in function_info['params']:
                    self.log_message("checking var_name: ", var_name)
                    if var_name not in self.memory_map.local_vars[-1]:
                        self.log_message("adding var_name: ", var_name)
                        self.memory_map.allocate_local(var_name)
                for var_type, var_names in function_info['vars']:
                    for var_name in var_names:
                        self.log_message("checking var: ", var_name)
                        if var_name not in self.memory_map.local_vars[-1]:
                            self.log_message("adding var: ", var_name)
                            self.memory_map.allocate_local(var_name)

            elif op == "gosub":
                # enter scope
                self.log_message("gosub node start")
                self.log.append("memory_map in gosub: " +
                                str(self.memory_map.memory))
                # Pop the parameters off the stack and assign them to the function's parameters
                function_info = function_table[result]
                for var_name in reversed(function_info['params']):
                    address = self.memory_map.allocate_local(
                        var_name)  # Allocate a new local variable
                    self.log.append("memory_map in after allocating local variable: " +
                                    str(self.memory_map.memory))
                    if self.stack:  # Check if the stack is not empty
                        param_value = self.stack.pop()  # Pop the parameter value from the stack
                        # Assign the parameter value to the local variable
                        self.memory_map.set_value(address, param_value)
                        self.log_message(
                            f"Assigning {param_value} value to param {var_name}")
                        self.log.append("memory_map in after setting value: " +
                                        str(self.memory_map.memory))
                        self.log_message(
                            f"Value of {var_name} is now {self.memory_map.get_value(address)}")
                    else:
                        raise ValueError("Error: stack is empty")
                # push the return address onto the stack
                self.call_stack.append(self.pc)
                self.log_message("call stack: ", self.call_stack)

                # Jump to the function
                if result:
                    self.pc = next(i for i, instruction in enumerate(
                        self.code) if instruction[0] == "label" and instruction[3] == result)
                else:
                    raise ValueError(
                        "No function name provided for gosub operation")

                # After the function finishes executing, retrieve the return value from the return_value field of your VirtualMachine
                return_value = self.return_value

                # add to function name stack
                self.function_name_stack.append(result)
                self.log.append("memory_map in after appending result: " +
                                str(self.memory_map.memory))
                self.log_message("function_name_stack: ",
                                 self.function_name_stack)

                # Get the return type of the function
                return_type = function_info['return_type']

                # If the function is not a void function, handle the return value as usual
                if return_type != "void":
                    # Generate a prefix for the temporary variable based on the return type
                    if return_type == 'int':
                        temp_var_prefix = 'Ti'
                    elif return_type == 'float':
                        temp_var_prefix = 'Tf'
                    elif return_type == 'bool':
                        temp_var_prefix = 'Tb'
                    else:
                        raise ValueError(
                            f"Unsupported return type: {return_type}")

                    # Generate a name for the new temporary variable
                    temp_var_name = temp_var_prefix + \
                        str(self.memory_map.next_temp_index)

                    # Allocate the new temporary variable
                    temp_var = self.memory_map.allocate_temp(temp_var_name)
                    self.log.append("memory_map after allocating temp: " + str(
                        self.memory_map.memory))

                    # # Store the return value in the new temporary variable
                    # self.memory_map.set_value(temp_var, return_value)
                    # self.log.append("memory_map after setting value: " + str(
                    #     self.memory_map.memory))
                    # Push the new temporary variable onto the stack
                    self.stack.append(temp_var)
                    self.log.append("memory_map after gosub: " + str(
                        self.memory_map.memory))

                # If the function is a void function, do not handle a return value
                else:
                    pass
                self.log.append("memory_map after pass: " + str(
                    self.memory_map.memory))
                self.log_message("gosub node end")

            elif op == "return":
                self.log_message("return node detected")
                self.log_message(
                    "memory_map in return before exit: ", self.memory_map.memory)
                # print local vars to debug
                self.log_message("local_vars: ", self.memory_map.local_vars)
                # print global vars to debug
                self.log_message("global_vars: ", self.memory_map.global_vars)
                # Evaluate the expression that's being returned
                if result.startswith(('Ti', 'Tf', 'Tb')) and self.memory_map.exists_temp(result):
                    return_value = self.memory_map.get_value(
                        self.memory_map.get_temp(result))
                    self.log_message("temp return_value: ", return_value)
                    # print temp vars to debug
                    self.log_message("temp_vars: ", self.memory_map.temp_vars_int,
                                     self.memory_map.temp_vars_float, self.memory_map.temp_vars_bool)
                elif result in self.memory_map.local_vars[-1]:
                    address = self.memory_map.get_local(result)
                    return_value = self.memory_map.get_value(address)
                    self.log_message("local return_value: ", return_value)
                elif result in self.memory_map.global_vars:
                    address = self.memory_map.get_global(result)
                    return_value = self.memory_map.get_value(address)
                    self.log_message("global return_value: ", return_value)
                else:
                    # Try to convert result to an int, float, or bool
                    try:
                        if '.' in result:
                            return_value = float(result)
                        elif result.lower() == 'true':
                            return_value = True
                        elif result.lower() == 'false':
                            return_value = False
                        else:
                            return_value = int(result)
                    except ValueError:
                        raise ValueError(
                            f"Error: {result} is not a valid number or variable")

                    # print global variable being declared
                    self.log_message(
                        "global_vars bein dececlared during return: ", self.memory_map.global_vars)

                self.log_message("return_value: ", return_value)
                self.memory_map.exit_scope()
                self.log_message("memory map after exit: ",
                                 self.memory_map.memory)
                self.stack.append(return_value)
                self.log_message("stack: ", self.stack)

            elif op == "EndFunc":
                self.log_message("EndFunc node detected")
                self.log_message("call stack: ", self.call_stack)
                # jump to call stack position
                if self.call_stack:
                    # Pop the return address from the call_stack
                    return_address = self.call_stack.pop()
                    # Set the program counter (pc) to the return address

                    self.log_message(
                        "going to return address: ", return_address)
                    self.pc = return_address
                    self.log_message("pc: ", self.pc)
                    # print op, arg1, arg2, result of return address
                    self.log_message("code: ", self.code[return_address])
                else:
                    self.log_message("Error: call_stack is empty")
                # pop the current memory map off the stack
                # self.memory_map.exit_scope()

                # Check if function_name_stack is not empty
                if self.function_name_stack:
                    # Pop the function name from function_name_stack
                    function_name = self.function_name_stack.pop()
                    self.log_message("function_name: ", function_name)

                    # Check if stack is not empty
                    if self.stack:
                        # Pop the value from the stack
                        value = self.stack.pop()

                        # Create a global variable with the function's name and assign it the value
                        address = self.memory_map.allocate_global(
                            function_name)
                        self.memory_map.set_value(address, value)
                        self.log_message(
                            "assining value to global variable: ", value)
                        self.log_message(
                            "global_vars: ", self.memory_map.global_vars)
                    else:
                        self.log_message("Error: stack is empty")
                else:
                    self.log_message("Error: function_name_stack is empty")

            # ------ Arrays ------#
            elif op == 'array_assign':
                print("array_assign node detected")
                array_name = arg1
                index = int(arg2)
                value = int(result)  # directly use result as the value
                self.memory_map.set_array_value(array_name, value, index)
                print("assigning value to array: ", array_name,
                      "index: ", index, "value: ", value)
                print("array_assign node end")

            elif op == 'pointer_assign':
                pointer_name = arg1
                value = self.memory_map.get_value(
                    self.memory_map.get_temp(result))
                self.memory_map.pointer_assign(pointer_name, value)

            elif op == 'load':
                array_name = arg1
                index = int(arg2)
                if result.startswith(('Ti', 'Tf', 'Tb')) and not self.memory_map.exists_temp(result):
                    self.log_message("new temporal variable detected")
                    self.memory_map.declare_temp(result)
                    self.log_message("Declared temp variable: ", result)
                result_address = self.memory_map.get_temp(result)
                self.memory_map.set_value(
                    result_address, self.memory_map.get_array_value(array_name, index))

        # endprogram
            elif op == "EndProg":
                self.log_message("EndProg node detected")
                break
        # Keep the turtle window open until the user closes it
        turtle.done()
