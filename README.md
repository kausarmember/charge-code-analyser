
# Charge Code Analyser

## 1. Project Overview

The **Charge Code Analyser** is a Python-based command-line tool that automates the monthly expense reconciliation process for charge code owners at Accenture.

Each month, charge code owners are required to manually compare actual expenses against forecasts, categorise spend by employee and expense type, calculate variances, and identify overspends or underspends. This process is repeated across thousands of charge codes organisation-wide, representing a significant and error-prone manual overhead. 

This tool reads actual and forecast expense data from CSV files, calculates variances automatically, categorises spend by employee and category and outputs a structured summary report — reducing manual effort and improving accuracy at scale.

### Target Audience

- **Charge Code Owners** – to automate monthly reconciliation
- **Project Managers** – to monitor budget performance across projects
- **Finance Teams** – to identify spending anomalies across charge codes

### Problem Statement

Monthly charge code reconciliation is currently performed manually in spreadsheets, leading to time-consuming processes and a significant risk of human error across thousands of charge codes organisation-wide. This tool automates that reconciliation, flagging variances and anomalies instantly and consistently.

---

## 2. Setup & Run Instructions

**Prerequisites:** Python 3.x (no external libraries required)

### Clone the repository

```bash
git clone https://github.com/kausarmember/charge-code-analyser.git
cd charge-code-analyser
```

### Run the tool

```bash
python main.py
```

**Input files** — place both files in the `data/` folder:

- `actuals.csv` — recorded expenses by employee and category
- `forecast.csv` — planned budget data per charge code

**Output** — a JSON summary report containing:

- Total actual spend vs forecast
- Variance calculations per category
- Spend breakdown by employee
- Spend breakdown by expense category

### Run the unit tests

```bash
python -m unittest test_analyser.py
```
---

## 3. Project Structure
```
charge-code-analyser/
├── main.py              # Entry point - runs the analyser
├── analyser.py          # Core business logic
├── test_analyser.py     # Unit tests
├── data/
│   ├── actuals.csv      # Actual expense data (CSV input)
│   └── forecast.csv     # Forecast/budget data (CSV input)
└── output/              # Generated summary reports
```
---

## 4. Dependencies

No external libraries are required. This tool is built 
using Python 3.x standard library modules only:

- `csv` — reading and parsing CSV input files
- `json` — structured report output  
- `unittest` — unit testing framework

---

## 5. Known Issues & Future Improvements

### Known Issues

- Currently processes one charge code at a time prioritise clarity, testability and correctness over premature optimisation
- Input CSV files must follow the expected column format

### Future Improvements

- [ ] Scale to process multiple charge codes simultaneously
- [ ] Integrate directly with Accenture's internal portal via API
- [ ] Add a web-based dashboard for finance teams
- [ ] Export reports in Excel format for wider stakeholder use
- [ ] Add CI/CD pipeline via GitHub Actions for automated testing

---

## 6. Author 
Kausar Member  
BPP University — Advanced Programming
