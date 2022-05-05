# https://stackoverflow.com/questions/30926323/how-to-do-a-calculation-on-python-with-a-random-operator
import operator
import random

operators = [('+', operator.add), ('-', operator.sub), ('*', operator.mul)]

for i in range(10):
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op, fn = random.choice(operators)
    print("{} {} {} = {}".format(a, op, b, fn(a, b)))