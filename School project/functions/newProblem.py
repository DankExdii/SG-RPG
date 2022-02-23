import random

def newProblem(op:str) -> tuple:
    '''function for generating 2 numbers and 1 operator'''

    if op == "+" or op == "-":
        i1 = random.randint(1, 100)
        i2 = random.randint(1, 100)
        if op == "-" and i1 < i2:
            i1 += random.randint(0, 100 - i2) +i2 - i1
    else:
        i1 = random.randint(1, 10)
        i2 = random.randint(1, 10)

    if op == "/":
        if not i2 == 0 and i1 % i2 != 0:
            while i1 % i2 != 0:
                i1 = random.randint(1, 10)
                i2 = random.randint(1, 10)

    return i1, i2, op