class MemoryMap:
    def __init__(self, size):
        self.memory = [0] * size
        self.global_vars = {}
        self.local_vars = []
        self.stack = []
        self.temp_vars_int = {}
        self.temp_vars_float = {}
        self.temp_vars_bool = {}
        self.temp_return_index = 80  # return temporal variable index
        self.next_local_address = 0

    def allocate_global(self, name):
        address = len(self.global_vars)
        self.global_vars[name] = address
        return address

    def allocate_global_array(self, name, size):
        start_address = len(self.global_vars)
        for i in range(size):
            self.global_vars[f"{name}_{i}"] = start_address + i
        return start_address, size

    def allocate_local(self, name):
        # Use the counter instead of the length of the current scope's dictionary
        address = self.next_local_address
        # Add the variable to the current scope
        self.local_vars[-1][name] = address
        self.next_local_address += 1  # Increment the counter after allocating an address
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

    def get_global_array(self, name, size):
        start_address = self.global_vars[f"{name}_0"]
        return start_address, size

    def get_local(self, name):
        try:
            return self.local_vars[-1][name]
        except KeyError:
            raise ValueError(f"Local variable {name} is not defined")

    def set_value(self, address, value):
        self.memory[address] = value

    def set_array_value(self, name, value, index):
        key = f"{name}_{index}"
        if key in self.global_vars:
            self.memory[self.global_vars[key]] = value
        else:
            raise ValueError(
                f"Global array {name} at index {index} is not defined")

    def set_local_value(self, name, value):
        try:
            # Get the address of the local variable
            address = self.local_vars[-1][name]
            # Use the address to set the value in the memory
            self.memory[address] = value
        except KeyError:
            raise ValueError(f"Local variable {name} is not defined")

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
        print("Entering scope")
        # Save the current state of the local variables
        self.local_vars.append(
            self.local_vars[-1].copy() if self.local_vars else {})

    def exit_scope(self):
        # Restore the saved state of the local variables
        self.local_vars.pop()
        # Reset the next local address to the end of the current local variables
        self.next_local_address = len(
            self.local_vars[-1]) if self.local_vars else 0

    def set_value(self, address, value):
        self.memory[address] = value

    def pointer_assign(self, pointer_name, value):
        if pointer_name not in self.global_vars:
            raise ValueError(f"Pointer {pointer_name} is not defined")
        self.memory[self.global_vars[pointer_name]] = value

    def get_array_value(self, array_name, index):
        key = f"{array_name}_{index}"
        if key not in self.global_vars:
            raise ValueError(
                f"Array {array_name} at index {index} is not defined")
        return self.memory[self.global_vars[key]]
