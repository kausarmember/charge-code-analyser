"""
analyser.py
Contains main business logic for the Charge Code Analyser.
Reads actual and forecast expense data from CSV files, calculates variances and generates a summary JSON report.
"""

import csv # Read and parse CSV input files
import json # Write the structured JSON report
import os # Check file paths and create directories
from datetime import datetime # Timestamp the report

def load_forecast(filepath):
    """
    Opens the forecast CSV file and stores each category and its budgeted amount in a dictionary.
    Dictionary is used for fast lookups when matching categories against actual expense entries.
    """
    forecast = {}

    # Check file exists before attempting to open
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Forecast file not found: {filepath}"
        )

    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check required fields exist
                if 'category' not in row or \
                   'forecast_amount' not in row:
                    raise ValueError(
                        "Forecast CSV is missing required columns"
                    )
                # Convert amount from string to float
                try:
                    forecast[row['category']] = float(
                        row['forecast_amount']
                    )
                except ValueError:
                    raise ValueError(
                        f"Invalid forecast amount for "
                        f"{row['category']}: "
                        f"{row['forecast_amount']}"
                    )
    except csv.Error as e:
        raise csv.Error(f"Error reading forecast CSV: {e}")

    return forecast