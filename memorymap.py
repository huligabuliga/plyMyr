class MemoryMap:
    def __init__(self, size):
        self.memory = [0] * size
        self.global_vars = {}
        self.local_vars = []
        self.stack = []
        self.temp_vars_int = {}
        self.temp_vars_float = {}
        self.temp_vars_bool = {}
        self.temp_return_index = 0  # return temporal variable index

    def allocate_global(self, name):
        address = len(self.global_vars)
        self.global_vars[name] = address
        return address

    def allocate_local(self, name):
        # Get the length of the current scope's dictionary
        address = len(self.local_vars[-1])
        # Add the variable to the current scope
        self.local_vars[-1][name] = address
        return address

    def allocate_temp(self, name):
        if name.startswith('Ti'):
            temp_vars = self.temp_vars_int
        elif name.startswith('Tf'):
            temp_vars = self.temp_vars_float
        elif name.startswith('Tb'):
            temp_vars = self.temp_vars_bool
        else:
            raise ValueError(f"Unsupported temporary variable type: {name}")

        address = len(temp_vars)
        temp_vars[name] = address
        return address

    def get_local_value(self, name):
        try:
            # Get the address of the local variable
            address = self.local_vars[-1][name]
            # Use the address to get the value from the memory
            value = self.memory[address]
            return value
        except KeyError:
            raise ValueError(f"Local variable {name} is not defined")

    def next_temp_index(self):
        # Increment the temporary variable index and return the new value
        self.temp_index += 1
        return self.temp_index

    def get_global(self, name):
        try:
            return self.global_vars[name]
        except KeyError:
            raise ValueError(f"Global variable {name} is not defined")

    def get_local(self, name):
        try:
            return self.local_vars[-1][name]
        except KeyError:
            raise ValueError(f"Local variable {name} is not defined")

    def set_value(self, address, value):
        self.memory[address] = value

    def get_value(self, address):
        return self.memory[address]

    def push_stack(self, value):
        self.stack.append(value)

    def pop_stack(self):
        return self.stack.pop()

    def declare_temp(self, name):
        if name.startswith('Ti'):
            temp_vars = self.temp_vars_int
        elif name.startswith('Tf'):
            temp_vars = self.temp_vars_float
        elif name.startswith('Tb'):
            temp_vars = self.temp_vars_bool
        else:
            raise ValueError(f"Unsupported temporary variable type: {name}")

        if name not in temp_vars:
            address = len(self.memory)
            temp_vars[name] = address
            # Add a new slot in memory for the temporary variable
            self.memory.append(0)

    def get_temp(self, name):
        if name.startswith('Ti'):
            temp_vars = self.temp_vars_int
        elif name.startswith('Tf'):
            temp_vars = self.temp_vars_float
        elif name.startswith('Tb'):
            temp_vars = self.temp_vars_bool
        else:
            raise ValueError(f"Unsupported temporary variable type: {name}")

        return temp_vars[name]

    def exists_temp(self, name):
        if name.startswith('Ti'):
            return name in self.temp_vars_int
        elif name.startswith('Tf'):
            return name in self.temp_vars_float
        elif name.startswith('Tb'):
            return name in self.temp_vars_bool
        else:
            raise ValueError(f"Unsupported temporary variable type: {name}")

    def enter_scope(self):
        self.local_vars.append({})

    def exit_scope(self):
        self.local_vars.pop()

    def set_value(self, address, value):
        self.memory[address] = value
