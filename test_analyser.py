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