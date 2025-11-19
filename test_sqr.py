# Write a Python3 function *sqr(n)* that returns the square of its numeric parameter *n*.
"""Sample code
def sqr(n):
    return n * n
"""


from exercise_1 import sqr
def test_sqr1():
  assert sqr(2) == 4
def test_sqr2():
  assert sqr(-2) == 4
def test_sqr3():
  assert sqr(0) == 0
