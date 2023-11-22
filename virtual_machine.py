from memorymap import MemoryMap

# Description: Virtual machine for the compiler
from semantic_analysis import symbol_table
from semantic_analysis import function_table


class VirtualMachine:
    def __init__(self, code, memory_map, function_table, symbol_table):
        self.code = code
        self.memory_map = memory_map
        self.pc = 0  # Program counter
        self.stack = []  # Stack for function calls
        self.return_value = None  # Return value of a function
        self.call_stack = []  # Stack for function calls
        self.function_name_stack = []  # stack of function names

    # local and global getters

    def is_local(self, var):
        return var in self.memory_map.local_vars

    def is_global(self, var):
        return var in self.memory_map.global_vars

    # helper functions for repetitve code

    def get_value(self, arg):
        try:
            return float(arg) if '.' in arg else int(arg)
        except ValueError:
            if arg.startswith(('Ti', 'Tf', 'Tb')):
                arg_value = self.memory_map.get_value(
                    self.memory_map.get_temp(arg))
                return float(arg_value) if '.' in str(arg_value) else int(arg_value)
            else:
                if self.memory_map.local_vars and arg in self.memory_map.local_vars[-1]:
                    arg_value = self.memory_map.get_value(
                        self.memory_map.get_local(arg))
                    return float(arg_value) if '.' in str(arg_value) else int(arg_value)
                elif arg in self.memory_map.global_vars:
                    arg_value = self.memory_map.get_value(
                        self.memory_map.get_global(arg))
                    return float(arg_value) if '.' in str(arg_value) else int(arg_value)
                else:
                    print(
                        f"Variable {arg} is not defined in global_vars or local_vars")
                    return None

    def perform_operation(self, op, result, arg1, arg2):
        print(f"{op} node detected")
        if result.startswith(('Ti', 'Tf', 'Tb')) and not self.memory_map.exists_temp(result):
            print("new temporal variable detected")
            self.memory_map.declare_temp(result)
            print("Declared temp variable: ", result)

        if result in self.memory_map.temp_vars_int or result in self.memory_map.temp_vars_float or result in self.memory_map.temp_vars_bool:
            arg1_value = self.get_value(arg1)
            arg2_value = self.get_value(arg2)

            if arg1_value is not None and arg2_value is not None:
                if op == "+":
                    self.memory_map.set_value(self.memory_map.get_temp(
                        result), arg1_value + arg2_value)
                elif op == "-":
                    self.memory_map.set_value(self.memory_map.get_temp(
                        result), arg1_value - arg2_value)
                elif op == "*":
                    self.memory_map.set_value(self.memory_map.get_temp(
                        result), arg1_value * arg2_value)
                elif op == "/":
                    self.memory_map.set_value(self.memory_map.get_temp(
                        result), arg1_value / arg2_value)

    def get_arg_value(self, arg):
        if isinstance(arg, str) and not arg.isdigit():
            if self.memory_map.get_local(arg):
                return self.memory_map.get_value(self.memory_map.get_local(arg))
            else:
                return self.memory_map.get_value(self.memory_map.get_global(arg))
        else:
            return int(arg) if isinstance(arg, str) else arg

    def perform_comparison(self, op, result, arg1, arg2):
        arg1_value = self.get_value(arg1)
        arg2_value = self.get_value(arg2)
        if arg1_value is None or arg2_value is None:
            print("Error: One of the arguments is None")
            return
        self.memory_map.declare_temp(result)

        if op == "==":
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value == arg2_value)
        elif op == "!=":
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value != arg2_value)
        elif op == ">":
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value > arg2_value)
        elif op == "<":
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value < arg2_value)
        elif op == ">=":
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value >= arg2_value)
        elif op == "<=":
            self.memory_map.set_value(self.memory_map.get_temp(
                result), arg1_value <= arg2_value)

    def run(self):
        while self.pc < len(self.code):
            op, arg1, arg2, result = self.code[self.pc]
            self.pc += 1
            print("pc = ", self.pc)

            if op == "=":
                print("equal node detected")
                print("arg1: ", arg1)
                print("arg2: ", arg2)
                print("result: ", result)
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
                        print(
                            f"Error: {arg1} is not a valid number or variable")
                        continue

                # Check if the result is a temporary variable and declare it if it's not already declared
                if result.startswith(('Ti', 'Tf')) and not self.memory_map.exists_temp(result):
                    print("Declaring temp variable: ", result)
                    self.memory_map.declare_temp(result)

                # Assign the value to the result
                if result.startswith(('Ti', 'Tf')):
                    print("Assigning value to a temporal variable")
                    self.memory_map.set_value(
                        self.memory_map.get_temp(result), arg1_value)
                    print("Value of ", result, " is now ", self.memory_map.get_value(
                        self.memory_map.get_temp(result)))
                elif result in self.memory_map.global_vars:
                    print("Assigning value to global variable")
                    self.memory_map.set_value(
                        self.memory_map.get_global(result), arg1_value)
                    print("Value of ", result, " is now ", self.memory_map.get_value(
                        self.memory_map.get_global(result)))
                elif self.memory_map.local_vars and result in self.memory_map.local_vars[-1]:
                    print("Assigning value to local variable")
                    self.memory_map.set_value(
                        self.memory_map.get_local(result), arg1_value)
                    print("Value of ", result, " is now ", self.memory_map.get_value(
                        self.memory_map.get_local(result)))
                    # print local vars to debug
                    print("local_vars: ", self.memory_map.local_vars)
                    # prints local memory map to debug
                    print("local memory map: ", self.memory_map.memory)
                else:
                    print(f"Error: Variable {result} is not defined")

            # ------ Arithmetic Operations ------#
            # ------ + - * / ------#
            elif op == "+":
                self.perform_operation(op, result, arg1, arg2)
            elif op == "-":
                self.perform_operation(op, result, arg1, arg2)
            elif op == "*":
                self.perform_operation(op, result, arg1, arg2)
            elif op == "/":
                self.perform_operation(op, result, arg1, arg2)

            # ------ boolean Operations ------#
            # ------ and or ------#
            # ------ > >= <= < == != ------#
            # ------ gotoF goto label ------#
            elif op == ">":
                self.perform_comparison(op, result, arg1, arg2)
            elif op == ">=":
                self.perform_comparison(op, result, arg1, arg2)
            elif op == "<":
                self.perform_comparison(op, result, arg1, arg2)
            elif op == "<=":
                self.perform_comparison(op, result, arg1, arg2)
            elif op == "==":
                self.perform_comparison(op, result, arg1, arg2)
            elif op == "!=":
                self.perform_comparison(op, result, arg1, arg2)

            # ------ for and while Operations ------#
            elif op == 'for':
                # Enter a new scope and declare the loop variable
                self.memory_map.enter_scope()
                self.memory_map.allocate_local(result)
                self.pc += 1
            elif op == 'endfor':
                # Exit the current scope
                self.memory_map.exit_scope()
                # self.pc += 1

            elif op == "gotoF":
                print("gotoF node detected")
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
                print("goto node detected")
                # Find the index of the label in the code
                label_index = next(i for i, instruction in enumerate(
                    self.code) if instruction[0] == "label" and instruction[3] == result)
                self.pc = label_index

            elif op == "label":
                pass

            elif op == "param":
                print("param node detected")
                # print memory map to debug
                print("memory_map: ", self.memory_map.memory)
                # print stack to debug
                print("stack: ", self.stack)
                # print result to debug
                print("result: ", result)
                # print arg1 to debug
                print("arg1: ", arg1)
                # print arg2 to debug
                print("arg2: ", arg2)
                # print global vars to debug
                print("global_vars: ", self.memory_map.global_vars)
                # print local vars to debug
                print("local_vars: ", self.memory_map.local_vars)
                # print temp vars to debug
                print("temp_vars: ", self.memory_map.temp_vars_int,
                      self.memory_map.temp_vars_float, self.memory_map.temp_vars_bool)

                if arg1 != '':
                    # If arg1 is not an empty string, check if it exists in global_vars
                    if arg1 in self.memory_map.global_vars:
                        print("found in global_vars")
                        # If arg1 exists in global_vars, get its value and push it onto the stack
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_global(arg1)))
                    elif arg1 in self.memory_map.local_vars[-1]:
                        print("found in local_vars")
                        # If arg1 exists in local_vars, get its value and push it onto the stack
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_local_value(arg1)))
                    elif arg1 in self.memory_map.temp_vars_int or arg1 in self.memory_map.temp_vars_float or arg1 in self.memory_map.temp_vars_bool:
                        print("found in temp_vars")
                        # If arg1 exists in temp_vars, get its value and push it onto the stack
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_temp(arg1)))
                    else:
                        # If arg1 does not exist in global_vars, treat it as a literal value and push it onto the stack
                        print("adding arg1 to stack: ", arg1)
                        self.stack.append(arg1)
                else:
                    # If arg1 is an empty string, push the value of result directly onto the stack
                    # If arg1 is an empty string, push the value of result directly onto the stack
                    if result.startswith('"') and result.endswith('"'):
                        # If result is a string literal (enclosed in quotes), push it directly onto the stack
                        self.stack.append(result)
                    elif result in self.memory_map.global_vars:
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_global(result)))
                    elif result in self.memory_map.local_vars[-1]:
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_local(result)))
                    elif result in self.memory_map.temp_vars_int or result in self.memory_map.temp_vars_float or result in self.memory_map.temp_vars_bool:
                        self.stack.append(self.memory_map.get_value(
                            self.memory_map.get_temp(result)))

                    else:
                        self.stack.append(result)
                print("stack: ", self.stack)

                # debug stack

            elif op == "write":
                values = [self.stack.pop() for _ in range(result)]
                for value in reversed(values):
                    print(value, end=' ')
                print()

                # ------ Functions------#
                # handle function local variables
            elif op == "ERA":
                print("ERA node detected")
                # Enter a new scope
                self.memory_map.enter_scope()
                # Add the local variables for the function to the MemoryMap
                function_info = function_table[arg1]
                print("function info", function_info)
                for var_name in function_info['params']:
                    print("adding var_name: ", var_name)
                    self.memory_map.allocate_local(var_name)
                for var_type, var_names in function_info['vars']:
                    for var_name in var_names:
                        print("adding var: ", var_name)
                        self.memory_map.allocate_local(var_name)

            elif op == "gosub":
                # Pop the parameters off the stack and assign them to the function's parameters
                function_info = function_table[result]
                for var_name in reversed(function_info['params']):
                    address = self.memory_map.allocate_local(
                        var_name)  # Allocate a new local variable
                    if self.stack:  # Check if the stack is not empty
                        param_value = self.stack.pop()  # Pop the parameter value from the stack
                        # Assign the parameter value to the local variable
                        self.memory_map.set_value(address, param_value)
                        print(
                            f"Assigning {param_value} value to param {var_name}")
                    else:
                        raise ValueError("Error: stack is empty")
                # push the return address onto the stack
                self.call_stack.append(self.pc)
                print("call stack: ", self.call_stack)

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
                print("function_name_stack: ", self.function_name_stack)

                # Get the return type of the function
                return_type = function_info['return_type']

                # Generate a prefix for the temporary variable based on the return type
                if return_type == 'int':
                    temp_var_prefix = 'Ti'
                elif return_type == 'float':
                    temp_var_prefix = 'Tf'
                elif return_type == 'bool':
                    temp_var_prefix = 'Tb'
                else:
                    raise ValueError(f"Unsupported return type: {return_type}")

                # Generate a name for the new temporary variable
                temp_var_name = temp_var_prefix + \
                    str(self.memory_map.next_temp_index)

                # Allocate the new temporary variable
                temp_var = self.memory_map.allocate_temp(temp_var_name)

                # Store the return value in the new temporary variable
                self.memory_map.set_value(temp_var, return_value)

            elif op == "return":
                print("return node detected")

                # print local vars to debug
                print("local_vars: ", self.memory_map.local_vars)
                # print global vars to debug
                print("global_vars: ", self.memory_map.global_vars)
                # Evaluate the expression that's being returned
                if result.startswith(('Ti', 'Tf', 'Tb')) and self.memory_map.exists_temp(result):
                    return_value = self.memory_map.get_value(
                        self.memory_map.get_temp(result))
                elif result in self.memory_map.local_vars[-1]:
                    address = self.memory_map.get_local(result)
                    return_value = self.memory_map.get_value(address)
                elif result in self.memory_map.global_vars:
                    address = self.memory_map.get_global(result)
                    return_value = self.memory_map.get_value(address)
                else:
                    return_value = None

                    # print global variable being declared
                    print("global_vars: ", self.memory_map.global_vars)

                print("return_value: ", return_value)
                self.stack.append(return_value)
                print("stack: ", self.stack)

            elif op == "EndFunc":
                print("EndFunc node detected")
                print("call stack: ", self.call_stack)
                # jump to call stack position
                if self.call_stack:
                    # Pop the return address from the call_stack
                    return_address = self.call_stack.pop()
                    # Set the program counter (pc) to the return address

                    print("going to return address: ", return_address)
                    self.pc = return_address
                    print("pc: ", self.pc)
                    # print op, arg1, arg2, result of return address
                    print("code: ", self.code[return_address])
                else:
                    print("Error: call_stack is empty")
                # pop the current memory map off the stack
                self.memory_map.exit_scope()

                # Check if function_name_stack is not empty
                if self.function_name_stack:
                    # Pop the function name from function_name_stack
                    function_name = self.function_name_stack.pop()
                    print("function_name: ", function_name)

                    # Check if stack is not empty
                    if self.stack:
                        # Pop the value from the stack
                        value = self.stack.pop()

                        # Create a global variable with the function's name and assign it the value
                        address = self.memory_map.allocate_global(
                            function_name)
                        self.memory_map.set_value(address, value)
                        print("assining value to global variable: ", value)
                        print("global_vars: ", self.memory_map.global_vars)
                    else:
                        print("Error: stack is empty")
                else:
                    print("Error: function_name_stack is empty")

        # endprogram
            elif op == "EndProg":
                print("EndProg node detected")
                break
