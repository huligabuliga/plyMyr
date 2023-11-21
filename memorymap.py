class MemoryMap:
    def __init__(self, size):
        self.memory = [0] * size
        self.global_vars = {}
        self.local_vars = {}
        self.stack = []
        self.temp_vars = {}

    def allocate_global(self, name):
        address = len(self.global_vars)
        self.global_vars[name] = address
        return address

    def allocate_local(self, name):
        address = len(self.local_vars)
        self.local_vars[name] = address
        return address

    def get_global(self, name):
        return self.global_vars[name]

    def get_local(self, name):
        return self.local_vars[name]

    def set_value(self, address, value):
        self.memory[address] = value

    def get_value(self, address):
        return self.memory[address]

    def push_stack(self, value):
        self.stack.append(value)

    def pop_stack(self):
        return self.stack.pop()

    def declare_temp(self, name):
        if name not in self.temp_vars:
            address = len(self.memory)
            self.temp_vars[name] = address
            # Add a new slot in memory for the temporary variable
            self.memory.append(0)

    def get_temp(self, name):
        return self.temp_vars[name]
