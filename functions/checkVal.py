def checkVal(num: int, num2: int, num3: int, operator: str) -> bool:
    '''check if <num> == <num2> <operator> <num3> \n
    for example, check if 6 == 2 * 3: \n
    checkVal(6, 2, 3, "*")'''
    if operator == "+":
        if num == num2 + num3:
            return True
        else:
            return False
    elif operator == "-":
        if num == num2 - num3:
            return True
        else:
            return False
    elif operator == ".":
        if num == num2 * num3:
            return True
        else:
            return False
    elif operator == "/":
        if num == 0:
            return
        if num == num2 / num3:
            return True
        else:
            return False