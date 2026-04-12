"""
analyser.py
Contains main business logic for the Charge Code Analyser.
Reads actual and forecast expense data from CSV files, calculates variances and generates a summary JSON report.
"""

import csv # Read and parse CSV input files
import json # Write the structured JSON report
import os # Check file paths and create directories
from datetime import datetime # Timestamp the report