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


def main():
    """
    Main function that orchestrates the charge code analysis.
    Loads forecast and actuals data from CSV files, generates a JSON summary report and prints a formatted summary 
    to the console including total forecast, actual spend, variance and any flagged overspends or unbudgeted items.
    """
    print("Charge Code Analyser")
    print("=" * 40)

    # Load forecast data from CSV
    print(f"\nLoading forecast data from {FORECAST_FILE}...")
    forecast = load_forecast(FORECAST_FILE)
    print(f"Loaded {len(forecast)} forecast categories")

    # Load actuals data from CSV
    print(f"\nLoading actuals data from {ACTUALS_FILE}...")
    actuals = load_actuals(ACTUALS_FILE)
    print(f"Loaded {len(actuals)} expense entries")

    # Generate the summary report
    print(f"\nGenerating report...")
    report = generate_report(forecast, actuals, OUTPUT_FILE)

    # Print summary to console
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    print(f"Charge Code:     {report['charge_code']}")
    print(f"Period:          {report['period']}")
    print(f"Total Forecast:  £{report['summary']['total_forecast']:,.2f}")
    print(f"Total Actual:    £{report['summary']['total_actual']:,.2f}")
    print(f"Total Variance:  £{report['summary']['total_variance']:,.2f}")
    print(f"Status:          {report['summary']['overall_status']}")

    # Print any flagged items to console for immediate review
    if report['flagged_items']:
        print("\n" + "=" * 40)
        print("FLAGGED ITEMS")
        print("=" * 40)
        for item in report['flagged_items']:
            if 'OVERSPEND' in item:
                print(f"  ! OVERSPEND: {item.split('OVERSPEND: ')[1]}")
            elif 'UNDERSPEND' in item:
                print(f"  v UNDERSPEND: {item.split('UNDERSPEND: ')[1]} ")
            elif 'UNBUDGETED' in item:
                print(f"  ? UNBUDGETED: {item.split('UNBUDGETED: ')[1]}")

    print(f"\nFull report saved to {OUTPUT_FILE}")

"""
Entry point guard — ensures main() is only called when this script is run directly, 
not when imported as a module by another script such as test_analyser.py
"""
if __name__ == "__main__":
    main()