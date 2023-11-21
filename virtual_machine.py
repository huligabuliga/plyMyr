from memorymap import MemoryMap

# Description: Virtual machine for the compiler


class VirtualMachine:
    def __init__(self, code, memory_map, function_table, symbol_table):
        self.code = code
        self.memory_map = memory_map
        self.pc = 0  # Program counter
        self.stack = []  # Stack for function calls

    def run(self):
        while self.pc < len(self.code):
            op, arg1, arg2, result = self.code[self.pc]
            self.pc += 1
            if isinstance(result, str) and result.startswith('T'):
                # Declare it as a temporary variable
                self.memory_map.declare_temp(result)
            if op == "=":
                self.memory_map.set_value(
                    self.memory_map.get_global(result), arg1)  # Use get_local instead of get_global
            # Add similar modifications for the other operations

            elif op == "call":
                # Push the current MemoryMap object onto the stack
                self.stack.append(self.memory_map)
                # Create a new MemoryMap object for the called function
                self.memory_map = MemoryMap()

            if op == "=":
                print("equal node detected")
                print("arg1: ", arg1)
                print("arg2: ", arg2)
                print("result: ", result)
                if result in self.memory_map.global_vars:
                    print("Assigning value to global variable")
                    if arg1 in self.memory_map.temp_vars:
                        arg1 = self.memory_map.get_value(
                            self.memory_map.get_temp(arg1))
                    self.memory_map.set_value(
                        self.memory_map.get_global(result), arg1)
                    print("Value of ", result, " is now ", self.memory_map.get_value(
                        self.memory_map.get_global(result)))
            elif op == "+":
                print("plus node detected")
                if result in self.memory_map.temp_vars:
                    self.memory_map.set_value(
                        self.memory_map.get_temp(result),
                        int(self.memory_map.get_value(self.memory_map.get_global(arg1))) +
                        int(self.memory_map.get_value(self.memory_map.get_global(arg2))))
                print("memory_map: ", self.memory_map.memory)
            elif op == "-":
                self.memory_map.set_value(self.memory_map.get_global(result), self.memory_map.get_value(
                    self.memory_map.get_global(arg1)) - self.memory_map.get_value(self.memory_map.get_global(arg2)))
            elif op == ">":
                self.memory_map.set_value(self.memory_map.get_global(result), self.memory_map.get_value(
                    self.memory_map.get_global(arg1)) > self.memory_map.get_value(self.memory_map.get_global(arg2)))
            elif op == "gotoF":
                if not self.memory_map.get_value(self.memory_map.get_global(arg1)):
                    self.pc = int(arg2[1:])
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
                if result in self.memory_map.global_vars:
                    self.stack.append(self.memory_map.get_value(
                        self.memory_map.get_global(result)))
                elif result in self.memory_map.temp_vars:
                    self.stack.append(self.memory_map.get_value(
                        self.memory_map.get_temp(result)))
                else:
                    # If result is not a variable, push it directly onto the stack
                    # This allows for strings, bools, ints, floats to be printed
                    self.stack.append(result)
                print("stack: ", self.stack)

                # debug stack

            elif op == "call":
                self.stack.append(self.pc)
                self.pc = int(arg1[1:])
            elif op == "return":
                self.pc = self.stack.pop()
                if result:
                    self.memory_map.set_value(
                        self.memory_map.get_global(result), self.stack.pop())
            elif op == "write":
                values = [self.stack.pop() for _ in range(result)]
                for value in reversed(values):
                    print(value, end=' ')
                print()

                # ------ Functions------#
                # handle function local variables

            elif op == "return":
                self.pc = self.stack.pop()
                # Pop the MemoryMap object of the called function from the stack
                self.memory_map = self.stack.pop()
                if result:
                    self.memory_map.set_value(
                        self.memory_map.get_local(result), self.stack.pop())  # Use get_local instead of get_global
