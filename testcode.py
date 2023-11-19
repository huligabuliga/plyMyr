
from code_generation import generate_code

test_case = ('function', 'int', 'factorial', [('int', 'n')], None, [
    ('if', ('binop', '==', 'n', 0), [
        ('return', 1)
    ]),
    ('return', ('binop', '*', 'n', ('function_call',
     'factorial', [('binop', '-', 'n', 1)])))
])

print(generate_code(test_case))
