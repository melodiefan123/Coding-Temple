# Student Grade Tracker — Starter

## What You're Building

A Python script that reads student grade data from a CSV, calculates averages, assigns letter grades, and writes a formatted summary report.

## Setup

No external packages needed — this uses only Python's built-in `csv` module.

```bash
# Make sure you're in the project folder
cd project/starter/

# Run the script
python3 grade_tracker.py
```

## Files

```
starter/
├── data/
│   └── students.csv      ← input data (15 students, some missing grades)
├── grade_tracker.py      ← your work goes here (implement the 5 functions)
├── requirements.txt      ← empty (no external packages)
└── README.md
```

## Your Task

Open `grade_tracker.py` and implement the 5 stub functions:

| Function | What it does |
|----------|-------------|
| `load_students(filepath)` | Reads CSV, returns list of dicts |
| `calculate_average(grades)` | Averages grade values, skips missing |
| `get_letter_grade(average)` | Converts number → A/B/C/D/F |
| `generate_report(students)` | Builds class summary dict |
| `write_report(report, filepath)` | Writes formatted report to file |

Do NOT modify `main()` — it orchestrates your functions and shows you what the expected output looks like.

## Expected Output

When all functions are implemented, running `python3 grade_tracker.py` should print something like:

```
Loading student data...
Loaded 15 students.
Generating report...

--- Summary ---
Total students:   15
Class average:    80.1
Highest average:  95.0
Lowest average:   55.0

Grade Distribution:
  A: 3
  B: 5
  C: 4
  D: 2
  F: 1

Top 5 students:
  Eve Williams         95.0  (A)
  ...

Report written to grade_report.txt
```
