"""
test_analyser.py
Unit tests for the Charge Code Analyser.
Tests core functions in analyser.py to ensure correctness, error handling and edge case behaviour using Python's built-in unittest framework.
"""

import unittest # Built-in Python testing framework
import os # Used to construct file paths for test data
from analyser import (
    load_forecast,
    load_actuals,
    calculate_variance,
    calculate_employee_spend
)

class TestAnalyser(unittest.TestCase):
    """
    Test class for the Charge Code Analyser.
    Uses unittest.TestCase to test core functions in analyser.py against known inputs and expected outputs.
    Following the Arrange, Act, Assert pattern for each test.
    """

    def test_load_forecast_returns_dictionary(self):
        """
        Tests that load_forecast correctly loads the forecast CSV file and returns a dictionary with the correct
        number of categories and amounts.
        """
        # Arrange
        filepath = os.path.join('data', 'forecast_2026_03.csv')

        # Act
        result = load_forecast(filepath)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 10)
        self.assertIn('Travel - Rail', result)
        self.assertEqual(result['Travel - Rail'], 2750.00)