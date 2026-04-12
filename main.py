"""
main.py
Entry point for the Charge Code Analyser.
Loads forecast and actual expense data from CSV files, runs the analysis and generates a JSON summary report. 
"""

import os
from analyser import load_forecast, load_actuals, generate_report # Import core analysis functions from analyser module
