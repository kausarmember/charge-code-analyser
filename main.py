"""
main.py
Entry point for the Charge Code Analyser.
Loads forecast and actual expense data from CSV files, runs the analysis and generates a JSON summary report. 
"""

import os
from analyser import load_forecast, load_actuals, generate_report # Import core analysis functions from analyser module

# Define file paths for input and output
FORECAST_FILE = os.path.join('data', 'forecast_2026_03.csv')
ACTUALS_FILE = os.path.join('data', 'actuals_2026_03.csv')
OUTPUT_FILE = os.path.join('output', 'report_2026_03.json')