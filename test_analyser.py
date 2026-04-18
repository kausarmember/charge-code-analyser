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
    Unit test suite for the Charge Code Analyser.
    Tests core functions in analyser.py against known inputs
    and expected outputs following the Arrange, Act, Assert
    pattern throughout.
    """

    def test_load_forecast_returns_dictionary(self):
        """
        Tests that load_forecast correctly loads the forecast
        CSV file and returns a dictionary with the correct
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

    def test_load_actuals_returns_list(self):
        """
        Tests that load_actuals correctly loads the actuals
        CSV file and returns a list of dictionaries with
        the correct number of entries and required fields.
        """
        # Arrange
        filepath = os.path.join('data', 'actuals_2026_03.csv')

        # Act
        result = load_actuals(filepath)

        # Assert
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('employee_name', result[0])
        self.assertIn('category', result[0])
        self.assertIn('amount', result[0])
        self.assertIsInstance(result[0]['amount'], float)

    def test_calculate_variance_correct_calculation(self):
        """
        Tests that calculate_variance correctly calculates
        the variance between forecast and actual spend.
        Uses simple known values to verify the calculation
        is correct and status flags are assigned correctly.
        """
        # Arrange
        forecast = {
            'Travel - Rail': 1000.00,
            'Subsistence': 500.00,
            'Training': 750.00
        }
        actuals = [
            {
                'employee_name': 'Test Employee',
                'charge_code': 'CC-1234',
                'category': 'Travel - Rail',
                'amount': 1200.00,
                'date': '2026-03-01',
                'description': 'Test entry',
                'period': '2026-03'
            },
            {
                'employee_name': 'Test Employee',
                'charge_code': 'CC-1234',
                'category': 'Subsistence',
                'amount': 300.00,
                'date': '2026-03-01',
                'description': 'Test entry',
                'period': '2026-03'
            }
        ]

        # Act
        result = calculate_variance(forecast, actuals)

        # Assert
        self.assertEqual(result['Travel - Rail']['status'], 'OVERSPENT')
        self.assertEqual(result['Travel - Rail']['variance'], -200.00)
        self.assertEqual(result['Subsistence']['status'], 'UNDERSPENT')
        self.assertEqual(result['Subsistence']['variance'], 200.00)
        self.assertEqual(result['Training']['status'], 'UNDERSPENT')
        self.assertEqual(result['Training']['variance'], 750.00)

    def test_load_forecast_missing_file_raises_error(self):
        """
        Tests that load_forecast raises a FileNotFoundError
        when the specified file does not exist.
        This verifies the defensive programming and error
        handling built into the function.
        """
        # Arrange
        filepath = 'data/nonexistent_file.csv'

        # Act and Assert
        with self.assertRaises(FileNotFoundError):
            load_forecast(filepath)

    def test_load_actuals_missing_file_raises_error(self):
        """
        Tests that load_actuals raises a FileNotFoundError
        when the specified file does not exist.
        This verifies the defensive programming and error
        handling built into the function.
        """
        # Arrange
        filepath = 'data/nonexistent_file.csv'

        # Act and Assert
        with self.assertRaises(FileNotFoundError):
            load_actuals(filepath)

    def test_calculate_employee_spend_correct_grouping(self):
        """
        Tests that calculate_employee_spend correctly groups
        expense entries by employee and calculates totals.
        Verifies both the total spend and category breakdown
        are calculated correctly for each employee.
        """
        # Arrange
        actuals = [
            {
                'employee_name': 'James Smith',
                'charge_code': 'CC-1234',
                'category': 'Travel - Rail',
                'amount': 320.00,
                'date': '2026-03-03',
                'description': 'Train to Manchester',
                'period': '2026-03'
            },
            {
                'employee_name': 'James Smith',
                'charge_code': 'CC-1234',
                'category': 'Subsistence',
                'amount': 45.00,
                'date': '2026-03-03',
                'description': 'Lunch Manchester',
                'period': '2026-03'
            },
            {
                'employee_name': 'Sarah Jones',
                'charge_code': 'CC-1234',
                'category': 'Travel - Rail',
                'amount': 190.00,
                'date': '2026-03-04',
                'description': 'Train to London',
                'period': '2026-03'
            }
        ]

        # Act
        result = calculate_employee_spend(actuals)

        # Assert
        self.assertIn('James Smith', result)
        self.assertIn('Sarah Jones', result)
        self.assertEqual(result['James Smith']['total'], 365.00)
        self.assertEqual(
            result['James Smith']['breakdown']['Travel - Rail'],
            320.00
        )
        self.assertEqual(
            result['James Smith']['breakdown']['Subsistence'],
            45.00
        )
        self.assertEqual(result['Sarah Jones']['total'], 190.00)

    def test_calculate_variance_unbudgeted_category(self):
        """
        Tests that calculate_variance correctly identifies
        and flags categories that appear in actuals but have
        no corresponding forecast entry. This verifies the
        tool handles unexpected expense categories gracefully.
        """
        # Arrange
        forecast = {
            'Travel - Rail': 1000.00
        }
        actuals = [
            {
                'employee_name': 'Test Employee',
                'charge_code': 'CC-1234',
                'category': 'Travel - Rail',
                'amount': 500.00,
                'date': '2026-03-01',
                'description': 'Test entry',
                'period': '2026-03'
            },
            {
                'employee_name': 'Test Employee',
                'charge_code': 'CC-1234',
                'category': 'Unplanned Expense',
                'amount': 150.00,
                'date': '2026-03-01',
                'description': 'Unbudgeted item',
                'period': '2026-03'
            }
        ]

        # Act
        result = calculate_variance(forecast, actuals)

        # Assert
        self.assertIn('Unplanned Expense', result)
        self.assertEqual(
            result['Unplanned Expense']['status'],
            'UNBUDGETED'
        )
        self.assertEqual(
            result['Unplanned Expense']['actual'],
            150.00
        )

# Run all tests when this file is executed directly
if __name__ == '__main__':
    unittest.main()