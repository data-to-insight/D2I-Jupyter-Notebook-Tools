import pytest
# run these in the cmd line using python -m pytest <filepath>


def sum_xy(x, y):
    return x + y

def prod_xy(x, y):
    return x * y

def sumprod(x, y):
    return sum_xy(x, y), prod_xy(x,y)

def addition_xy(x, y):
    if ((type(x) == float) | (type(x) == int)) & ((type(y) == float) | (type(y) == int)):
        return x + y
    elif (type(x) == str) | (type(y) == str):
        if type(x) == str:
            raise TypeError('x was a string, expected a float or int')
        if type(y) == str:
            raise TypeError('y was a string, expected a float or int')

def test_sum_xy():
    assert sum_xy(1, 1) == 2 

def test_sumprod():
    sum, prod = sumprod(1, 1)

    assert sum == 2
    assert prod == 1