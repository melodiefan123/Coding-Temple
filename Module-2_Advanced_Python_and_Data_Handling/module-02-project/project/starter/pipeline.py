"""
pipeline.py — Module 2 Project Starter
Your job: implement each method in the DataPipeline class below.
The docstrings describe exactly what each method should do.
"""

import pandas as pd
import re, os
import matplotlib.pyplot as plt


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
        try:
            self.df = pd.read_csv(filepath)
            print(f"Loaded {self.df.shape[0]} rows and {self.df.shape[1]} columns.")
        except FileNotFoundError:
            print("File not found.")


    def _parse_salary(self, val): 
        pattern = re.sub(r"[$,]", "", str(val))
        try:
            if not float(pattern) or float(pattern) < 0: 
                return None
            else: 
                return float(pattern)
        except ValueError: 
            return None
        
    def _parse_date(self, val):
        formats = ["%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y"]
        for format in formats: 
            try: 
                return pd.to_datetime(val, format = format)
            except:
                pass
        return None

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
        self.df = self.df.drop_duplicates(subset=["employee_id"], keep="first")
        self.df["name"] = self.df["name"].str.strip().str.title()
        self.df["department"] = self.df["department"].str.strip().str.lower().map(self.DEPT_MAP)
        self.df["office_location"] = self.df["office_location"].str.strip().str.lower().map(self.LOC_MAP)
        self.df["salary"] = self.df["salary"].apply(self._parse_salary)
        self.df["years_experience"] = pd.to_numeric(self.df["years_experience"], errors="coerce")
        self.df["years_experience"] = self.df["years_experience"].where(self.df["years_experience"] <= 50, other=None)
        self.df["satisfaction_score"] = pd.to_numeric(self.df["satisfaction_score"], errors="coerce")
        self.df["satisfaction_score"] = self.df["satisfaction_score"].where((self.df["satisfaction_score"] >= 1) & (self.df["satisfaction_score"] <= 10), other=None)
        self.df["survey_date"] = self.df["survey_date"].apply(self._parse_date)
        print(f"Cleaning complete. Total missing values: {sum(self.df.isnull().sum())}")
        return self




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
        avg_salary_by_dept = self.df.groupby("department")["salary"].mean().round(0)
        avg_satisfaction_by_dept = self.df.groupby("department")["satisfaction_score"].mean().round(0)
        headcount_by_location = self.df["office_location"].value_counts()
        avg_satisfaction_by_location = self.df.groupby("office_location")["satisfaction_score"].mean().round(0)
        clean_df = self.df[["years_experience", "salary"]].dropna()
        experience_salary_correlation = clean_df["years_experience"].corr(clean_df["salary"])
        return {
            "avg_salary_by_dept": avg_salary_by_dept,
            "avg_satisfaction_by_dept": avg_satisfaction_by_dept,
            "headcount_by_location": headcount_by_location, 
            "experience_salary_correlation": experience_salary_correlation,
            "avg_satisfaction_by_location": avg_satisfaction_by_location}
        

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
        try: 
            fig, (ax1, ax2) = plt.subplots(1,2, figsize = (15,5))

            avg_salary = self.df.groupby("department")["salary"].mean()
            satisfaction_score = self.df["satisfaction_score"]
            #bar
            ax1.bar(avg_salary.index, avg_salary.values)
            ax1.set_title("Average Salary by Department")
            ax1.set_xlabel("Average Salary")
            ax1.set_ylabel("Departments")

            #Histogram 
            ax2.hist(satisfaction_score, bins = 10 )
            ax2.set_title("Satisfaction Score Distribution")
            ax2.set_xlabel("Satisfaction Score")
            ax2.set_ylabel("Distribution(1-10)")

            plt.tight_layout()
            plt.savefig(output_path, dpi=150)
            plt.close()
        except FileNotFoundError:
            return None
        

    def export(self, output_path="output/clean_employees.csv"):
        """Save the cleaned self.df to a CSV at `output_path`.

        Create the output directory if it doesn't exist.
        Wrap in try/except.

        Hint: df.to_csv(output_path, index=False)

        Args:
            output_path: path for the exported CSV
        """
        # TODO: implement export()
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            self.df.to_csv(output_path, index=False)
        except FileNotFoundError:
            return None

    def run(self):
        """Execute the full pipeline: clean → analyze → visualize → export.

        Build output paths using os.path.join(os.path.dirname(__file__), "output", ...).
        Return the results dict from analyze().
        """
        # TODO: call each method in order and return results
        try: 

            self.clean()
            data_analysis = self.analyze()
            self.visualize(os.path.join(os.path.dirname(__file__), "output", "chart.png"))
            self.export(os.path.join(os.path.dirname(__file__), "output", "clean_data.csv"))
            return data_analysis
        except FileNotFoundError:
            return None
