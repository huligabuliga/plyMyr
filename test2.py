class QuadrupleGenerator:
    def __init__(self):
        self.quadruples = []
        self.temp_count = 1

    def generate_quadruples(self, ast):
        self.visit_program(ast)

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def visit_program(self, node):
        for declaration in node[2]:
            if declaration[0] == 'function':
                self.visit_function(declaration)

    def visit_function(self, node):
        function_name = node[2]
        self.quadruples.append(f"{function_name}:")

        # Generate quadruples for the function body
        for statement in node[4]:
            self.visit_statement(statement)

    def visit_statement(self, node):
        if node[0] == 'assignment':
            self.visit_assignment(node)
        elif node[0] == 'if_else':
            self.visit_if_else(node)
        elif node[0] == 'return':
            self.visit_return(node)
        elif node[0] == 'write':
            self.visit_write(node)

    def visit_assignment(self, node):
        target = node[1]
        expression = self.visit_expression(node[2])
        self.quadruples.append(f"= {expression} {target}")

    def visit_if_else(self, node):
        condition = self.visit_expression(node[1])
        label_false = self.new_temp()
        self.quadruples.append(f"gotoF {condition} {label_false}")

        # Generate quadruples for the true branch
        for statement in node[2]:
            self.visit_statement(statement)

        # Generate quadruples for the false branch
        if len(node) == 4:
            label_end = self.new_temp()
            self.quadruples.append(f"goto {label_end}")
            self.quadruples.append(f"{label_false}:")
            for statement in node[3]:
                self.visit_statement(statement)
            self.quadruples.append(f"{label_end}:")

        else:
            self.quadruples.append(f"{label_false}:")

    def visit_return(self, node):
        expression = self.visit_expression(node[1])
        self.quadruples.append(f"return {expression}")

    def visit_write(self, node):
        expression = self.visit_expression(node[1])
        self.quadruples.append(f"write {expression}")

    def visit_expression(self, node):
        if isinstance(node, tuple):
            if node[0] == 'binop':
                left = self.visit_expression(node[1])
                right = self.visit_expression(node[3])
                operator = node[2]
                result_temp = self.new_temp()
                self.quadruples.append(
                    f"{operator} {left} {right} {result_temp}")
                return result_temp
            elif node[0] == 'function_call':
                function_name = node[1]
                args = [self.visit_expression(arg) for arg in node[2]]
                result_temp = self.new_temp()
                self.quadruples.append(f"ERA {function_name}")
                for arg in args:
                    self.quadruples.append(f"param {arg}")
                self.quadruples.append(f"Gosub {function_name}")
                self.quadruples.append(f"= {function_name} {result_temp}")
                return result_temp
        else:
            return node


# Example usage:
ast = ('program', 'pelos', ('vars', [('int', ['i', 'j', 'k'])]),
       [('function', 'int', 'uno', [('int', 'j')], ('vars', [('int', ['i'])]),
        [('assignment', 'i', ('binop', '+', 'j', ('paren_expression', ('binop', '+', ('binop', '-', 'k', ('binop', '*', 'j', '2')), 'j')))),
         ('if_else', ('binop', '>', 'j', '0'), ('return', ('function_call', 'uno', [('binop', '-', 'i', 'j')])),
          ('return', ('binop', '+', 'i', 'k')))]),
        ('function', 'void', 'dos', [('int', 'i'), ('int', 'j')],
         ('vars', [('int', ['x', 'y'])]),
         [('assignment', 'x', ('binop', '+', 'i', 'j')),
          ('if_else', ('binop', '>', 'x', ('binop', '*', 'j', 'k')),
           [('write', [('function_call', 'uno', [('binop', '-', 'x', 'k')])])],
           [('write', [('function_call', 'uno', ['j'])])])]),
        ('main', [('read', '('), ('assignment', 'i', '5'),
                  ('assignment', 'j', ('binop', '+', ('binop', '*', 'i', '2'), 'i')),
                  ('function_call', 'dos', [('binop', '-', 'j', 'i'), 'j'])])])

generator = QuadrupleGenerator()
generator.generate_quadruples(ast)

for quadruple in generator.quadruples:
    print(quadruple)
