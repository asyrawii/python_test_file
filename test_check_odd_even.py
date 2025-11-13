from exercise_4 import check_odd_even
import pytest

@pytest.mark.parametrize("num, expected", [
    (2, "Even"),
    (7, "Odd"),
    (0, "Even"),
    (-3, "Odd"),
    (10, "Even")
])
def test_check_odd_even(num, expected):
    assert check_odd_even(num) == expected
