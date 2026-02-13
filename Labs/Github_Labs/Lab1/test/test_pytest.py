# test_calculator_pytest.py
import pytest
from src import calculator


def test_add_positive_numbers():
    assert calculator.add(10, 5) == 15
    assert calculator.add(100, 250) == 350


def test_add_negative_numbers():
    assert calculator.add(-5, -3) == -8
    assert calculator.add(-10, 10) == 0


def test_add_floats():
    assert calculator.add(2.5, 3.7) == pytest.approx(6.2)
    assert calculator.add(0.1, 0.2) == pytest.approx(0.3)


def test_subtract_basic():
    assert calculator.subtract(10, 3) == 7
    assert calculator.subtract(0, 5) == -5


def test_subtract_negatives():
    assert calculator.subtract(-5, -3) == -2
    assert calculator.subtract(5, 10) == -5


def test_multiply_integers():
    assert calculator.multiply(4, 5) == 20
    assert calculator.multiply(-3, 4) == -12
    assert calculator.multiply(0, 100) == 0


def test_multiply_floats():
    assert calculator.multiply(2.5, 4) == 10.0
    assert calculator.multiply(-1.5, 2) == -3.0


def test_divide_basic():
    assert calculator.divide(10, 2) == 5.0
    assert calculator.divide(9, 3) == 3.0
    assert calculator.divide(-10, 2) == -5.0


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculator.divide(10, 0)


def test_divide_floats():
    assert calculator.divide(7, 2) == pytest.approx(3.5)
    assert calculator.divide(1, 3) == pytest.approx(0.333333, rel=1e-5)


def test_power_basic():
    assert calculator.power(2, 3) == 8
    assert calculator.power(5, 2) == 25
    assert calculator.power(10, 0) == 1


def test_power_negative_exponent():
    assert calculator.power(2, -1) == 0.5
    assert calculator.power(10, -2) == 0.01


def test_invalid_types():
    with pytest.raises(TypeError):
        calculator.add("5", 3)
    with pytest.raises(TypeError):
        calculator.multiply(None, 5)