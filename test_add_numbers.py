# Write a Python3 function *add_numbers(x, y)* that returns the sum of two numeric values parameter *x* and *y*.

from exercise_2 import add_numbers
def test_add_numbers1():
  assert add_numbers(2,2) == 4
def test_add_numbers2():
  assert add_numbers(-2,-2) == -4
def test_add_numbers3():
  assert add_numbers(0,0) == 0
