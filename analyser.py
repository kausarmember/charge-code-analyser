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

def load_actuals(filepath):
    """
    Reads each expense entry from the actuals CSV file into a list of dictionaries.
    List is used as the order of entries matters - expenses are processed in the order they were incurred.
    Each row is validated to ensure all required fields are present and the amount is a valid number before being added to the list.
    """
    actuals = []

    # Check file exists before attempting to open
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Actuals file not found: {filepath}"
        )

    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Define all fields that must be present
                required_fields = [
                    'employee_name',
                    'charge_code',
                    'category',
                    'amount',
                    'date'
                ]
                # Check each required field exists and is not empty
                for field in required_fields:
                    if field not in row or row[field].strip() == '':
                        raise ValueError(
                            f"Missing or empty field '{field}' "
                            f"in actuals CSV"
                        )
                # Convert amount from string to float
                try:
                    row['amount'] = float(row['amount'])
                except ValueError:
                    raise ValueError(
                        f"Invalid amount for "
                        f"{row['employee_name']}: "
                        f"{row['amount']}"
                    )
                actuals.append(row)
    except csv.Error as e:
        raise csv.Error(f"Error reading actuals CSV: {e}")

    return actuals

def calculate_variance(forecast, actuals):
    """
    Calculates variance between forecast and actual spend per category. Returns a dictionary containing:
    - forecast amount
    - actual amount
    - variance (negative = overspend, positive = underspend)
    - status flag (OVERSPENT, UNDERSPENT, ON BUDGET or UNBUDGETED)
    """
    # Initialise results dictionary with forecast data
    results = {}
    for category, amount in forecast.items():
        results[category] = {
            'forecast': amount,
            'actual': 0.0,
            'variance': 0.0,
            'status': 'NO SPEND'
        }

    # Accumulate actual spend per category
    for entry in actuals:
        category = entry['category']
        amount = entry['amount']

        # Handle entries with categories not in forecast
        if category not in results:
            results[category] = {
                'forecast': 0.0,
                'actual': 0.0,
                'variance': 0.0,
                'status': 'UNBUDGETED'
            }
        results[category]['actual'] += amount

    # Calculate variance and set status for each category
    for category, data in results.items():
        # Skip categories already marked as unbudgeted
        if data['status'] == 'UNBUDGETED':
            continue
        variance = data['forecast'] - data['actual']
        results[category]['variance'] = round(variance, 2)

        if data['actual'] == 0.0 and data['forecast'] == 0.0:
            results[category]['status'] = 'NO SPEND'
        elif variance < 0:
            # Actual spend exceeded forecast
            results[category]['status'] = 'OVERSPENT'
        elif variance > 0:
            # Actual spend came in under forecast
            results[category]['status'] = 'UNDERSPENT'
        else:
            results[category]['status'] = 'ON BUDGET'

    return results

def calculate_employee_spend(actuals):
    """
    Calculates total spend per employee.
    Uses a dictionary keyed by employee name for efficient grouping and aggregation of expense entries.
    """
    employee_spend = {}

    for entry in actuals:
        name = entry['employee_name']
        amount = entry['amount']
        category = entry['category']

        # Create a new entry for the employee if not already present in the dictionary
        if name not in employee_spend:
            employee_spend[name] = {
                'total': 0.0,
                'breakdown': {}
            }

        # Add amount to employee total
        employee_spend[name]['total'] += amount
        employee_spend[name]['total'] = round(
            employee_spend[name]['total'], 2
        )

        # Track spend by category per employee
        if category not in employee_spend[name]['breakdown']:
            employee_spend[name]['breakdown'][category] = 0.0

        # Add amount to category breakdown
        employee_spend[name]['breakdown'][category] += amount
        employee_spend[name]['breakdown'][category] = round(
            employee_spend[name]['breakdown'][category], 2
        )

    return employee_spend

def generate_report(forecast, actuals, output_path):
    """
    Generates a JSON summary report containing:
    - Total forecast vs actual spend
    - Variance by category with status flags
    - Spend breakdown by employee
    - List of flagged overspends and unbudgeted items
    Saves the report to the specified output path.
    """
    variance_data = calculate_variance(forecast, actuals)
    employee_data = calculate_employee_spend(actuals)

    # Calculate totals
    total_forecast = round(sum(forecast.values()), 2)
    total_actual = round(
        sum(entry['amount'] for entry in actuals), 2
    )
    total_variance = round(total_forecast - total_actual, 2)

    # Determine overall status
    if total_variance < 0:
        overall_status = 'OVERSPENT'
    elif total_variance > 0:
        overall_status = 'UNDERSPENT'
    else:
        overall_status = 'ON BUDGET'

    # Build flagged items list including overspends, underspends and unbudgeted items for review
    flagged = []
    for category, data in variance_data.items():
        if data['status'] == 'OVERSPENT':
            flagged.append(
                f"OVERSPEND: {category} exceeded forecast "
                f"by £{abs(data['variance']):.2f}"
            )
        elif data['status'] == 'UNDERSPENT' :
            flagged.append(
                f"UNDERSPEND: {category} underspent by " 
                f"£{abs(data['variance']):.2f}"
            )
        elif data['status'] == 'UNBUDGETED':
            flagged.append(
                f"UNBUDGETED: {category} had no forecast "
                f"but incurred £{data['actual']:.2f}"
            )

    # Assemble report dictionary
    report = {
        'charge_code': actuals[0]['charge_code'],
        'period': actuals[0]['period'],
        'generated_at': datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        ),
        'summary': {
            'total_forecast': total_forecast,
            'total_actual': total_actual,
            'total_variance': total_variance,
            'overall_status': overall_status
        },
        'variance_by_category': variance_data,
        'spend_by_employee': employee_data,
        'flagged_items': flagged
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write report to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)

    return report
