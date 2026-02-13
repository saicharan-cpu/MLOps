import sys
import os
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src import calculator


class TestAddition(unittest.TestCase):

    def test_positive_numbers(self):
        self.assertEqual(calculator.add(7, 8), 15)
        self.assertEqual(calculator.add(100, 50), 150)

    def test_negative_numbers(self):
        self.assertEqual(calculator.add(-4, -6), -10)
        self.assertEqual(calculator.add(-15, 15), 0)

    def test_decimal_numbers(self):
        self.assertAlmostEqual(calculator.add(1.5, 2.3), 3.8, places=5)


class TestSubtraction(unittest.TestCase):

    def test_basic_subtraction(self):
        self.assertEqual(calculator.subtract(15, 7), 8)
        self.assertEqual(calculator.subtract(0, 10), -10)

    def test_negative_results(self):
        self.assertEqual(calculator.subtract(5, 15), -10)
        self.assertEqual(calculator.subtract(-5, 5), -10)


class TestMultiplication(unittest.TestCase):

    def test_positive_multiplication(self):
        self.assertEqual(calculator.multiply(6, 7), 42)
        self.assertEqual(calculator.multiply(12, 3), 36)

    def test_zero_multiplication(self):
        self.assertEqual(calculator.multiply(0, 50), 0)
        self.assertEqual(calculator.multiply(25, 0), 0)

    def test_negative_multiplication(self):
        self.assertEqual(calculator.multiply(-4, 5), -20)
        self.assertEqual(calculator.multiply(-3, -3), 9)


class TestDivision(unittest.TestCase):

    def test_basic_division(self):
        self.assertEqual(calculator.divide(20, 4), 5.0)
        self.assertEqual(calculator.divide(15, 3), 5.0)

    def test_division_with_remainder(self):
        self.assertAlmostEqual(calculator.divide(10, 3), 3.333333, places=5)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(5, 0)


class TestPower(unittest.TestCase):

    def test_positive_exponents(self):
        self.assertEqual(calculator.power(3, 4), 81)
        self.assertEqual(calculator.power(2, 10), 1024)

    def test_zero_exponent(self):
        self.assertEqual(calculator.power(5, 0), 1)
        self.assertEqual(calculator.power(100, 0), 1)

    def test_negative_exponents(self):
        self.assertEqual(calculator.power(2, -2), 0.25)
        self.assertAlmostEqual(calculator.power(5, -1), 0.2, places=5)


class TestTypeErrors(unittest.TestCase):

    def test_string_inputs(self):
        with self.assertRaises(TypeError):
            calculator.add("hello", 5)

    def test_none_inputs(self):
        with self.assertRaises(TypeError):
            calculator.multiply(None, 10)


if __name__ == '__main__':
    unittest.main()