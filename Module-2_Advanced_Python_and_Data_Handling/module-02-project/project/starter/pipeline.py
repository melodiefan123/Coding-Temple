"""
pipeline.py — Module 2 Project Starter
Your job: implement each method in the DataPipeline class below.
The docstrings describe exactly what each method should do.
"""

import pandas as pd


class DataPipeline:
    """
    A data processing pipeline for employee survey data.

    Usage (once implemented):
        pipeline = DataPipeline("data/messy_employee_survey.csv")
        results = pipeline.run()
    """

    # Canonical spellings for normalization — use these dicts in your clean() method.
    DEPT_MAP = {
        "engineering": "Engineering",
        "eng":         "Engineering",
        "marketing":   "Marketing",
        "mktg":        "Marketing",
        "sales":       "Sales",
        "hr":          "HR",
        "human resources": "HR",
        "h.r.":        "HR",
        "finance":     "Finance",
        "fin":         "Finance",
    }

    LOC_MAP = {
        "new york":        "New York",
        "nyc":             "New York",
        "chicago":         "Chicago",
        "chi":             "Chicago",
        "austin":          "Austin",
        "austin, tx":      "Austin",
        "atx":             "Austin",
        "seattle":         "Seattle",
        "sea":             "Seattle",
        "remote":          "Remote",
        "work from home":  "Remote",
    }

    def __init__(self, filepath):
        """Load the CSV at `filepath` into self.df (a pandas DataFrame).
        Print how many rows and columns were loaded.

        Hint: use pd.read_csv()
        Wrap the load in try/except to catch FileNotFoundError.

        Args:
            filepath: path to the messy CSV file
        """
        # TODO: implement __init__
        pass

    def clean(self):
        """Clean the DataFrame stored in self.df and print a summary.

        Steps to implement (in order):
        1. Remove rows with duplicate employee_id (keep first occurrence).
           Hint: df.drop_duplicates(subset=["employee_id"], keep="first")

        2. Standardize 'name' — strip whitespace, title case.
           Hint: df["name"].str.strip().str.title()

        3. Normalize 'department' — map messy variants to canonical names.
           Hint: df["department"].str.strip().str.lower().map(self.DEPT_MAP)

        4. Normalize 'office_location' — same pattern as department.
           Hint: use self.LOC_MAP

        5. Convert 'salary' to float — strip "$" and "," first, set negatives to None.
           Hint: write a helper function and use df["salary"].apply(helper)
                 import re; re.sub(r"[$,]", "", str(val)) strips the symbols

        6. Convert 'years_experience' to numeric; set values > 50 to None (outliers).
           Hint: pd.to_numeric(..., errors="coerce")

        7. Convert 'satisfaction_score' to numeric; set values outside 1–10 to None.

        8. Parse 'survey_date' — multiple formats exist (MM/DD/YYYY, YYYY-MM-DD, DD-MM-YYYY).
           Hint: write a helper that tries pd.to_datetime(val, format=fmt) for each format.
                 Formats to try: "%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y"

        After all steps, reassign self.df = df and print a missing-values summary.

        Returns self so calls can be chained: pipeline.clean().analyze()
        """
        # TODO: implement clean()
        pass

    def analyze(self):
        """Compute summary statistics from the cleaned self.df.

        Compute and print:
        1. Average salary by department
           Hint: df.groupby("department")["salary"].mean().round(0)

        2. Average satisfaction score by department

        3. Headcount by office location
           Hint: df["office_location"].value_counts()

        4. Pearson correlation between years_experience and salary
           Hint: drop rows where either is NaN, then Series.corr()

        5. One additional insight of your choice (e.g., satisfaction by location)

        Return a dict with all results so main.py can use them.
        Keys to use: "avg_salary_by_dept", "avg_satisfaction_by_dept",
                     "headcount_by_location", "experience_salary_correlation",
                     "avg_satisfaction_by_location"
        """
        # TODO: implement analyze()
        pass

    def visualize(self, output_path="output/charts.png"):
        """Create and save visualizations to `output_path`.

        Required charts:
        - Bar chart: average salary by department
        - Histogram: satisfaction score distribution (bins 1–10)
        Bonus:
        - Horizontal bar: headcount by office location

        Use matplotlib with plt.subplots() for a multi-chart layout.
        Save with plt.savefig(output_path, dpi=120, bbox_inches="tight").
        Call plt.close() after saving.

        Hint: import matplotlib; matplotlib.use("Agg") at top of file
              prevents errors when no display is available.

        Args:
            output_path: where to save the PNG file
        """
        # TODO: implement visualize()
        pass

    def export(self, output_path="output/clean_employees.csv"):
        """Save the cleaned self.df to a CSV at `output_path`.

        Create the output directory if it doesn't exist.
        Wrap in try/except.

        Hint: df.to_csv(output_path, index=False)

        Args:
            output_path: path for the exported CSV
        """
        # TODO: implement export()
        pass

    def run(self):
        """Execute the full pipeline: clean → analyze → visualize → export.

        Build output paths using os.path.join(os.path.dirname(__file__), "output", ...).
        Return the results dict from analyze().
        """
        # TODO: call each method in order and return results
        pass
