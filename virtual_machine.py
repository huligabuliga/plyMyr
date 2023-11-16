class VirtualMachine:
    def __init__(self, program):
        self.vars = {}
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
                elif '=' in line:
                    var, expr = line.split(' = ')
                    self.vars[var] = eval(
                        expr, {'true': True, 'false': False}, self.vars)
                elif line.startswith('if'):
                    _, condition, _, label = line.split()
                    if eval(condition, {'true': True, 'false': False}, self.vars):
                        self.pc = self.find_label(label)
                        continue
                elif line.startswith('goto'):
                    _, label = line.split()
                    self.pc = self.find_label(label)
                    continue
                elif line.startswith('param'):
                    _, value = line.split(maxsplit=1)
                    print(
                        eval(value, {'true': True, 'false': False}, self.vars), end=' ')
                elif line.startswith('call print'):
                    pass  # already printed in 'param' command
                elif line.startswith('L') and ':' in line:
                    pass  # This is a label, do nothing
            except ValueError as e:
                raise ValueError(
                    f"Error processing line {self.pc + 1}: {line}. Original error: {str(e)}")
            self.pc += 1

    def find_label(self, label):
        for i, line in enumerate(self.program):
            if line == label + ':':
                return i
        raise RuntimeError(f'Label not found: {label}')
