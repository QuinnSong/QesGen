import random
import re
import itertools
import math

# Regex patterns to check if exp is valid
MD_PATTERN = '(\d+(\*|/)\d+)'  ## * AND /
AM_PATTERN = '(\d+(\+|-)\d+)'  ## + AND -
BRA_PATTERN = '.*?(\([^)(]+\))'  ## ( AND )


def replace_mul_div(exp, pattern, num_limit, student_special_mode):
    """
    1) for * and /, make sure all ops result is in range limit
    2) for /, make sure there is no reminder
    3) finally replace * and / with actual result values
    If student special mode is on, then num_limit = 10 for * and / ops
    :param exp: math expression
    :param pattern: regex pattern to parse expression like a[+-*/]b
    :param num_limit: max value allowed
    :param student_special_mode: True for student special mode; False otherwise
    :return: math expression with the parsed exp calculated; None if invalid
    """
    while re.findall(pattern, exp):
        md = re.findall(pattern, exp)
        if md[0][1] in ['+', '-']:
            if eval(md[0][0]) not in range(0, num_limit + 1):
                exp = None
                break
        elif student_special_mode:
            if len(md[0][0]) > 3 or eval(md[0][0]) >= 10:
                exp = None
                break
        if md[0][1] == '/':
            i, j = md[0][0].split('/')
            if int(i) % int(j) != 0:
                exp = None
                break
        if exp:
            exp = exp.replace(md[0][0], str(eval(md[0][0])))
    return exp


def replace_bras(exp, num_limit, student_special_mode):
    """
    1) for (), make sure all ops result is in range limit
    2) finally replace () with actual result values
    :param exp: math expression
    :param num_limit: max value allowed
    :param student_special_mode: True for student special mode; False otherwise
    :return: math expression without (); None if invalid
    """
    while re.findall(BRA_PATTERN, exp):
        bras = re.findall(BRA_PATTERN, exp)
        if any(eval(a) not in range(0, num_limit + 1) for a in bras):
            exp = None
            break
        for b in bras:
            tmp = check_in_bras(b.strip(')('), num_limit, student_special_mode)
            if not tmp:
                exp = None
                break
            else:
                exp = exp.replace(b, str(eval(b)))
        if not exp: break
    return exp


def check_in_bras(exp, num_limit, student_special_mode):
    """
    Check if the exp inside () is valid
    :param exp: math expression
    :param num_limit: max value allowed
    :param student_special_mode: True for student special mode; False otherwise
    :return: True if the exp inside () is valid; False otherwise
    """
    exp = replace_mul_div(exp, MD_PATTERN, num_limit, student_special_mode)
    if not exp:
        return False
    exp = replace_mul_div(exp, AM_PATTERN, num_limit, student_special_mode)
    return True if exp else False


def isExpValid(exp, num_limit, student_special_mode):
    """
    Main function to validate a expression
    :param exp: math expression
    :param num_limit: max value allowed
    :param student_special_mode: True for student special mode; False otherwise
    :return: True if valid; False otherwise
    """
    if eval(exp) not in range(0, num_limit + 1):
        return False

    exp = replace_bras(exp, num_limit, student_special_mode)
    if exp and check_in_bras(exp, num_limit, student_special_mode):
        return True
    else:
        return False


# def isCarryOrBorrow (exp):
#     """
#     If there is carry or borrow in tens, return the result of expression;
#     else return 0.
#     Applicable only to addition and subtraction
#     """
#     v = re.sub('(\d*)(\d)', r'\2', exp)
#     print v
#     return eval(exp) if eval(v) >= 10 or eval(v) < 0 else 0
#
# def calCarryOrBorrow (exp, num_limit):
#     """
#     Use while loop for each operation
#     """
#     res = 0
#     while len(re.findall(r'[\+-]', exp)) >= 1:
#         part = re.findall('^\d+[\+-]\d+', exp)[0]
#         res = isCarryOrBorrow(part)
#         if res <= 0 or res > num_limit : break
#         else:
#             exp = re.sub ('^\d+[\+-]\d+', str(res), exp)
#     return res > 0 and res <= num_limit

def convertToDecimal(exp, seed, num_decimal=2):
    """
    Convert an integer expression to decimal expression
    :param exp: math expression
    :param seed: decimal list
    :param num_decimal: decimal digits
    :return:
    """
    nums = re.findall('\d+', exp)
    ops = re.findall('[^\d]+', exp)

    mask = lambda x: int(x) * random.choice(seed)
    nums_mask = [str(mask(i)) for i in nums]
    if len(nums) <= len(ops):
        k = ''.join([j for i in map(None, ops, nums_mask) for j in i if j])
    else:
        k = ''.join([j for i in map(None, nums_mask, ops) for j in i if j])
    return k


def hasCarryOrBorrow(exp):
    """
    Check expression to see if carry or borrow is required
    :param exp: math expression
    :return: True if carry/borrow is required; False otherwise
    """
    sign = re.findall('(\d+)([+*/-])(\d+)', exp)
    if sign[0][1] == '/':
        return False
    elif sign[0][1] == '*':
        return any([int(x) * int(y) >= 10 for x in list(sign[0][0]) for y in list(sign[0][2])])
    else:
        if eval(exp) < 0:
            return True
        else:
            grp = re.findall('(\d+)(.)(\d+)', exp)
            qty = min(len(grp[0][0]), len(grp[0][2]))
            pair = zip(list(grp[0][0][len(grp[0][0]) - qty:]), list(grp[0][2][len(grp[0][2]) - qty:]))
            # print pair
            return any([eval(x + grp[0][1] + y) >= 10 or eval(x + grp[0][1] + y) < 0 for x, y in pair])


if __name__ == '__main__':
    s1 = '23+18'
    s2 = '51-27'
    s3 = '60-26-19'
    s4 = '66-27+45'
    s0 = '31-99'
    s11 = '333-9'
    a = '(212 + 2) - (71 - 811)'
    # print isExpValid('((5+2)*1+3-10)+2*3', 5)
    # print isExpValid('6+(3-2)+5', 6)
    # print isExpValid('(6-3)*6', 10)
    # print calCarryOrBorrow (s3)
    # print convertToDecimal(a, [0.1,0.2, 0.3, 0.4])
    # print replace_mul_div('44-30*5', MD_PATTERN, 100, True)
    # print isExpValid('93+45-97', 100, True)
    # print hasCarryOrBorrow('82*1113')
    # print calCarryOrBorrow('8-8+9', 10)
    print isExpValid('7/(1+7)*6', 100, True)
