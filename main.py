"""
main.py
Entry point for the Charge Code Analyser.
Loads forecast and actual expense data from CSV files, runs the analysis and generates a JSON summary report. 
"""

import os
# Import core analysis functions from analyser module
from analyser import load_forecast, load_actuals, generate_report

# Define file paths for input and output
FORECAST_FILE = os.path.join('data', 'forecast_2026_03.csv')
ACTUALS_FILE = os.path.join('data', 'actuals_2026_03.csv')
OUTPUT_FILE = os.path.join('output', 'report_2026_03.json')


def main():
    """
    Orchestrates the charge code analysis pipeline.
    Loads forecast and actuals data from CSV files, generates
    a JSON summary report and plain text summary and prints
    a formatted summary to the console including total forecast,
    actual spend, variance and flagged items.

    Raises:
        FileNotFoundError: If input CSV files are not found.
        ValueError: If input data is invalid or malformed.
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

    # Print any flagged items to console for review
    if report['flagged_items']:
        print("\n" + "=" * 40)
        print("FLAGGED ITEMS")
        print("=" * 40)

        # Filter overspends and calculate total
        overspends = [i for i in report['flagged_items']
                      if 'OVERSPEND' in i]

        if overspends:
            # Extract amounts from flagged strings for total
            overspend_total = sum(
                float(i.split('£')[1])
                for i in overspends
            )

            print(f"\n  OVERSPENDS "
                  f"({len(overspends)} "
                  f"{'item' if len(overspends) == 1 else 'items'} | "
                  f"Total: £{overspend_total:,.2f}):")
            for item in overspends:
                print(f"    ! {item.split('OVERSPEND: ')[1]}")

        # Filter underspends and calculate total
        underspends = [i for i in report['flagged_items']
                       if 'UNDERSPEND' in i]
        if underspends:
            underspend_total = sum(
                  float(i.split('£')[1])
                  for i in underspends
            )
            print(f"\n  UNDERSPENDS "
                  f"({len(underspends)} "
                  f"{'item' if len(underspends) == 1 else 'items'} | "
                  f"Total: £{underspend_total:,.2f}):")
            for item in underspends:
                print(f"    v {item.split('UNDERSPEND: ')[1]}")

        # Filter unbudgeted items and calculate total
        unbudgeted = [i for i in report['flagged_items']
                      if 'UNBUDGETED' in i]
        if unbudgeted:
            unbudgeted_total = sum(
                float(i.split('£')[1])
                for i in unbudgeted
            )
            print(f"\n  UNBUDGETED "
                  f"({len(unbudgeted)} "
                   f"{'item' if len(unbudgeted) == 1 else 'items'} | "
                  f"Total: £{unbudgeted_total:,.2f}):")
            for item in unbudgeted:
                print(f"    ? {item.split('UNBUDGETED: ')[1]}")

    # Derive text output path from JSON path to keep filenames consistent
    txt_output = OUTPUT_FILE.replace('.json', '.txt')
    with open(txt_output, 'w', encoding='utf-8') as f:
        f.write("Charge Code Analyser\n")
        f.write("=" * 40 + "\n")
        f.write(f"Charge Code:     {report['charge_code']}\n")
        f.write(f"Period:          {report['period']}\n")
        f.write(f"Generated:       {report['generated_at']}\n")
        f.write("=" * 40 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total Forecast:  £{report['summary']['total_forecast']:,.2f}\n")
        f.write(f"Total Actual:    £{report['summary']['total_actual']:,.2f}\n")
        # Negative variance = overspend, positive = underspend
        f.write(f"Total Variance:  £{report['summary']['total_variance']:,.2f}\n")
        f.write(f"Status:          {report['summary']['overall_status']}\n")

        if report['flagged_items']:
            f.write("\n" + "=" * 40 + "\n")
            f.write("FLAGGED ITEMS\n")
            f.write("=" * 40 + "\n")

            # split('£')[1] extracts the numeric amount from the flagged string
            overspends = [i for i in report['flagged_items']
                         if 'OVERSPEND' in i]
            if overspends:
                overspend_total = sum(
                    float(i.split('£')[1])
                    for i in overspends
                )
                f.write(f"\n  OVERSPENDS "
                        f"({len(overspends)} "
                        f"{'item' if len(overspends) == 1 else 'items'} | "
                        f"Total: £{overspend_total:,.2f}):\n")
                for item in overspends:
                    f.write(f"    ! {item.split('OVERSPEND: ')[1]}\n")

            underspends = [i for i in report['flagged_items']
                          if 'UNDERSPEND' in i]
            if underspends:
                underspend_total = sum(
                    float(i.split('£')[1])
                    for i in underspends
                )
                f.write(f"\n  UNDERSPENDS "
                        f"({len(underspends)} "
                        f"{'item' if len(underspends) == 1 else 'items'} | "
                        f"Total: £{underspend_total:,.2f}):\n")
                for item in underspends:
                    f.write(f"    v {item.split('UNDERSPEND: ')[1]}\n")

            # Unbudgeted items flagged as they were not forecast 
            # and require investigation by the charge code owner
            unbudgeted = [i for i in report['flagged_items']
                         if 'UNBUDGETED' in i]
            if unbudgeted:
                unbudgeted_total = sum(
                    float(i.split('£')[1])
                    for i in unbudgeted
                )
                f.write(f"\n  UNBUDGETED "
                        f"({len(unbudgeted)} "
                        f"{'item' if len(unbudgeted) == 1 else 'items'} | "
                        f"Total: £{unbudgeted_total:,.2f}):\n")
                for item in unbudgeted:
                    f.write(f"    ? {item.split('UNBUDGETED: ')[1]}\n")

    print(f"\nJSON report saved to {OUTPUT_FILE}")
    print(f"Text summary saved to {txt_output}")

# Entry point guard — ensures main() is only called when
# this script is run directly, not when imported as a module
if __name__ == "__main__":
    main()