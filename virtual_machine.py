import logging

logging.basicConfig(filename='vm_logs.txt',
                    level=logging.INFO, format='%(message)s')


class VirtualMachine:
    def __init__(self, program, symbol_table, function_table):
        self.vars = {var: 0 if type == 'int' else 0.0 for var,
                     type in symbol_table.items()}
        self.functions = function_table
        self.stack = []
        self.params = []
        self.program = [line.strip()
                        for line in program.split('\n') if line.strip()]
        self.pc = 0

    def run(self):
        while self.pc < len(self.program):
            line = self.program[self.pc]
            try:
                if line.startswith('DECLARE'):
                    _, type, var = line.split()
                    self.vars[var] = 0 if type == 'int' else 0.0

                elif line.startswith('FUNCTION'):
                    logging.info(f"Processing function definition: {line}")
                    _, return_type, rest = line.split(maxsplit=2)
                    func_name, params = rest.split('(', 1)
                    func_name = func_name.strip()  # Remove leading/trailing whitespace
                    params = params.split(')')[0].split(
                        ',')  # Split the parameters by comma
                    # Extract the parameter names
                    params = [param.split()[2] for param in params]
                    # Add this line
                    logging.info(f"Extracted parameter names: {params}")
                    # Find the end of the function definition
                    start_pc = self.pc + 1
                    while not self.program[self.pc].startswith('END FUNCTION'):
                        self.pc += 1
                    self.functions[func_name] = {
                        'return_type': return_type, 'start_pc': start_pc, 'params': params}
                    # Print the updated self.functions dictionary
                    logging.info(f"Updated self.functions: {self.functions}")
                    # Set the program counter to the line after the function definition
                    self.pc += 1
                    continue

                elif '=' in line:
                    logging.info(f"Processing assignment: {line}")
                    var, expr = line.split(' = ')
                    if expr.startswith('callfunc'):
                        logging.info(f"Processing function call: {expr}")
                        _, func_name, num_params = expr.split(maxsplit=2)
                        # Push the parameters onto the stack
                        if func_name not in self.functions:
                            raise ValueError(
                                f"Function '{func_name}' is not defined.")
                        logging.info(
                            f"Pushing {num_params} parameters onto the stack")
                        for _ in range(int(num_params)):
                            logging.info(f"Popping parameter from the stack")
                            self.stack.append(self.params.pop(0))
                        return_address = self.pc  # Save the return address
                        logging.info(
                            f"Setting program counter to {self.functions[func_name]['start_pc']}")
                        self.pc = self.functions[func_name]['start_pc']
                        logging.info(f"Executing function {func_name}")
                        return_value = self.execute_function(
                            func_name, int(num_params))
                        self.vars[var] = return_value
                        # Set the program counter to the line after the function call
                        self.pc = return_address + 1
                        continue
                    else:
                        self.vars[var] = eval(
                            expr, {'true': True, 'false': False}, self.vars)

                elif line.startswith('RETURN'):
                    continue

                elif line.startswith('if'):
                    parts = line.split()
                    if 'not' in parts:
                        _, _, condition, _, label = parts
                        if not eval(condition, {'true': True, 'false': False}, self.vars):
                            self.pc = self.find_label(label)
                            continue
                    else:
                        _, condition, _, label = parts
                        if eval(condition, {'true': True, 'false': False}, self.vars):
                            self.pc = self.find_label(label)
                            continue
                elif line.startswith('goto'):
                    _, label = line.split()
                    self.pc = self.find_label(label)
                    continue
                elif line.startswith('param'):
                    _, value = line.split(maxsplit=1)
                    self.params.append(
                        eval(value, {'true': True, 'false': False}, self.vars))
                elif line.startswith('call print'):
                    print(*self.params, end=' ')
                    self.params = []  # Clear the parameters list
                elif line.startswith('L') and ':' in line:
                    pass  # This is a label, do nothing
            except ValueError as e:
                raise ValueError(
                    f"Error processing line {self.pc + 1}: {line}. Original error: {str(e)}")
            self.pc += 1

    def define_function(self, func_name, return_type, param_types, start_pc):
        # In the function definition processing
        params = params.split(')')[0].split(
            ',')  # Split the parameters by comma
        params = [param.split()[2] for param in params if param.startswith(
            'DECLARE')]  # Extract the parameter names
        logging.info(f"Extracted parameter names: {params}")  # Add this line
        self.functions[func_name] = {
            'return_type': return_type, 'param_types': param_types, 'start_pc': start_pc}

    def execute_function(self, func_name, num_params):
        # Save the current program counter and variable space
        saved_pc = self.pc
        saved_vars = self.vars.copy()

        # Create a new variable space for the function
        self.vars = {}

        # Get the start of the function from the functions dictionary
        self.pc = self.functions[func_name]['start_pc']

        # Get the parameters from the stack
        params = [self.stack.pop() for _ in range(num_params)]
        params.reverse()  # Reverse the order of the parameters

        # Print the reversed parameters
        logging.info(f"Reversed parameters: {params}")

       # Get the function's argument names
        arg_names = self.functions[func_name]['params']

        # Assign the parameters to the function's arguments
        for arg_name, param in zip(arg_names, params):
            self.vars[arg_name] = param
            logging.info(f"Assigned {arg_name} = {param}")

        # Print the function's argument names
        logging.info(f"Function's argument names: {arg_names}")

        # Print the function's variables
        logging.info(f"Function's variables: {self.vars}")

        # Assign the parameters to the function's arguments
        # Assign the parameters to the function's arguments
        for i, param in enumerate(params):
            line = self.program[self.pc + i]
            if line.startswith('DECLARE'):
                _, _, var = line.split()
                self.vars[var] = param
                logging.info(f"Assigned {var} = {param}")
            else:
                break  # Stop the loop when we reach a line that's not a parameter declaration

        # Debugging line
        logging.info(f"Current vars after parameter assignment: {self.vars}")
        # logging.info(f"Assigned {var} = {params[i]}")

        # Run the function
        while not self.program[self.pc].startswith('RETURN'):
            line = self.program[self.pc]
            if line.startswith('DECLARE'):
                _, type, var = line.split()
                self.vars[var] = 0 if type == 'int' else 0.0
            elif '=' in line:
                var, expr = line.split(' = ')
                self.vars[var] = eval(
                    expr, {'true': True, 'false': False}, self.vars)
            self.pc += 1

        # Get the return value
        _, result_var = self.program[self.pc].split()
        result = self.vars[result_var]

        # Restore the program counter and variable space
        self.pc = saved_pc
        self.vars = saved_vars

        # Return the result
        return result

    def find_label(self, label):
        for i, line in enumerate(self.program):
            if line == label + ':':
                return i
        raise RuntimeError(f'Label not found: {label}')
