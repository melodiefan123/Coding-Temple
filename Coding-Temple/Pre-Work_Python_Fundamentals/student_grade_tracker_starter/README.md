# Student Grade Tracker

A command-line Python application that processes student grade data from a CSV file, calculates individual averages and letter grades, and outputs a formatted summary report.

## Project Overview

This project reads student records from `data/students.csv`, handles missing or non-numeric grade values gracefully, computes overall class metrics, and outputs final analytics both to the terminal and to `grade_report.txt`.

## Prerequisites & Installation

- Python 3.10+
- Built entirely with Python's standard library (`csv`). No external dependencies or virtual environments required.

## Project Structure

```
starter/
├── data/
│   └── students.csv      # Input CSV file containing student names and grades
├── grade_tracker.py      # Core application logic and CLI entry point
├── grade_report.txt      # Formatted report output generated upon execution
├── requirements.txt      # Dependency specification (built-in modules only)
└── README.md             # Project documentation
```

## How to Run

1. Open your terminal and navigate to the project root directory:
   ```bash
   cd path/to/starter
   ```

2. Run the application:
   ```bash
   python3 grade_tracker.py
   ```

## Expected Terminal Output

```
Loading student data...
Loaded 15 students.
Generating report...

--- Summary ---
Total students:   15
Class average:    79.4
Highest average:  95.2
Lowest average:   58.2

Grade Distribution:
  A: 3
  B: 4
  C: 5
  D: 2
  F: 1
  N/A: 0

Top 5 students:
  Eve Williams         95.2  (A)
  Noah Garcia          93.0  (A)
  Alice Johnson        91.5  (A)
  Jack Taylor          89.0  (B)
  Grace Lee            86.8  (B)

Report written to grade_report.txt
```

## Error & Missing Data Handling

- **Missing Files:** If `data/students.csv` is not found, the program displays a helpful error message asking the user to verify their current working directory and safely returns an empty student list without crashing.
- **Missing / Invalid Grades:** Blank cells, whitespace, and non-numeric inputs are safely skipped. Averages are computed using only valid numeric entries.
- **No Available Grades:** If all subject grades for a student are missing, their numeric average is evaluated as `None` and assigned a letter grade of `"N/A"`.