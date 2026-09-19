"""
pipeline.py — Module 2 Project Implementation
A data processing pipeline for employee survey data.
"""

import pandas as pd
import re, os
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")  # Ensure headless environment compatibility


class DataPipeline:
    """
    A data processing pipeline for employee survey data.

    Usage:
        pipeline = DataPipeline("data/messy_employee_survey.csv")
        results = pipeline.run()
    """

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
        """Load the CSV at `filepath` into self.df (a pandas DataFrame)."""
        self.filepath = filepath
        self.df = None

        try:
            self.df = pd.read_csv(filepath)
            print(f"Loaded {self.df.shape[0]} rows and {self.df.shape[1]} columns.")
        except FileNotFoundError:
            print(f"Error: Raw data file not found at {filepath}.")
            self.df = pd.DataFrame()
        except Exception as e:
            print(f"Unexpected error loading file: {e}")
            self.df = pd.DataFrame()

    def _parse_salary(self, val):
        if pd.isna(val):
            return None

        pattern = re.sub(r"[$,]", "", str(val)).strip()

        try:
            sal_float = float(pattern)
            return sal_float if sal_float >= 0 else None
        except ValueError:
            return None

    def _parse_date(self, val):
        if pd.isna(val):
            return None

        formats = ["%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y"]
        for fmt in formats:
            try:
                return pd.to_datetime(val, format=fmt)
            except Exception:
                pass
        try:
            return pd.to_datetime(val)
        except Exception:
            return None

    def clean(self):
        """Clean the DataFrame stored in self.df and print a summary."""
        if self.df is None or self.df.empty:
            print("Cleaning skipped: DataFrame is empty.")
            return self

        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=["employee_id"], keep="first").copy()
        dup_count = initial_rows - len(self.df)

        # 2. Standardize 'name' cleanly without index misalignment
        if "name" in self.df.columns:
            self.df["name"] = self.df["name"].astype(str).str.strip().str.title()
            self.df["name"] = self.df["name"].replace({"Nan": None, "None": None, "": None})

        # 3. Normalize department: map known aliases, title-case unmapped values
        if "department" in self.df.columns:
            dept_lower = self.df["department"].astype(str).str.strip().str.lower()
            # Replace known aliases
            dept_mapped = dept_lower.replace(self.DEPT_MAP)
            # Title-case any valid departments that weren't in DEPT_MAP keys
            unmapped_mask = ~dept_lower.isin(self.DEPT_MAP.keys())
            dept_mapped[unmapped_mask] = dept_mapped[unmapped_mask].str.title()
            
            self.df["department"] = dept_mapped.replace({"Nan": None, "None": None, "": None})

        # 4. Normalize office location similarly
        if "office_location" in self.df.columns:
            loc_lower = self.df["office_location"].astype(str).str.strip().str.lower()
            loc_mapped = loc_lower.replace(self.LOC_MAP)
            unmapped_loc = ~loc_lower.isin(self.LOC_MAP.keys())
            loc_mapped[unmapped_loc] = loc_mapped[unmapped_loc].str.title()

            self.df["office_location"] = loc_mapped.replace({"Nan": None, "None": None, "": None})

        # 5. Salary parsing
        sal_nulls_before = self.df["salary"].isna().sum()
        self.df["salary"] = self.df["salary"].apply(self._parse_salary)
        invalid_salaries = self.df["salary"].isna().sum() - sal_nulls_before

        # 6. Experience validation
        self.df["years_experience"] = pd.to_numeric(self.df["years_experience"], errors="coerce")
        invalid_exp = ((self.df["years_experience"] < 0) | (self.df["years_experience"] > 50)).sum()
        self.df["years_experience"] = self.df["years_experience"].where(
            (self.df["years_experience"] >= 0) & (self.df["years_experience"] <= 50), other=None
        )

        # 7. Satisfaction score validation
        self.df["satisfaction_score"] = pd.to_numeric(self.df["satisfaction_score"], errors="coerce")
        invalid_sat = ((self.df["satisfaction_score"] < 1) | (self.df["satisfaction_score"] > 10)).sum()
        self.df["satisfaction_score"] = self.df["satisfaction_score"].where(
            (self.df["satisfaction_score"] >= 1) & (self.df["satisfaction_score"] <= 10), other=None
        )

        # 8. Date parsing
        self.df["survey_date"] = self.df["survey_date"].apply(self._parse_date)

        print("\n" + "=" * 40)
        print("CLEANING SUMMARY")
        print("=" * 40)
        print(f"• Removed {dup_count} duplicate rows.")
        print(f"• Reset {invalid_salaries} invalid/negative salary entries.")
        print(f"• Reset {invalid_exp} experience values exceeding 50 years.")
        print(f"• Reset {invalid_sat} satisfaction scores outside 1–10.")
        print(f"• Total remaining null values across dataset: {self.df.isnull().sum().sum()}\n")

        return self

    def analyze(self):
        """Compute summary statistics from the cleaned self.df."""
        if self.df is None or self.df.empty:
            print("Analysis skipped: DataFrame is empty.")
            return {}

        avg_salary_by_dept = self.df.groupby("department")["salary"].mean().round(0)
        avg_satisfaction_by_dept = self.df.groupby("department")["satisfaction_score"].mean().round(1)
        headcount_by_location = self.df["office_location"].value_counts()
        avg_satisfaction_by_location = self.df.groupby("office_location")["satisfaction_score"].mean().round(1)

        clean_df = self.df[["years_experience", "salary"]].dropna()
        experience_salary_correlation = round(clean_df["years_experience"].corr(clean_df["salary"]), 3)

        print("=" * 40)
        print("ANALYSIS RESULTS")
        print("=" * 40)
        print("\n1. Average Salary by Department:")
        print(avg_salary_by_dept.to_string())
        print("\n2. Average Satisfaction by Department:")
        print(avg_satisfaction_by_dept.to_string())
        print("\n3. Headcount by Office Location:")
        print(headcount_by_location.to_string())
        print(f"\n4. Pearson Correlation (Experience vs Salary): {experience_salary_correlation}")
        print("\n5. Average Satisfaction by Office Location:")
        print(avg_satisfaction_by_location.to_string())
        print("=" * 40 + "\n")

        return {
            "avg_salary_by_dept": avg_salary_by_dept,
            "avg_satisfaction_by_dept": avg_satisfaction_by_dept,
            "headcount_by_location": headcount_by_location,
            "experience_salary_correlation": experience_salary_correlation,
            "avg_satisfaction_by_location": avg_satisfaction_by_location,
        }

    def visualize(self, output_path="output/charts.png"):
        """Create and save visualizations to `output_path`."""
        if self.df is None or self.df.empty:
            print("Visualization skipped: DataFrame is empty.")
            return

        try:
            dir_name = os.path.dirname(output_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

            avg_salary = self.df.groupby("department")["salary"].mean()
            satisfaction_score = self.df["satisfaction_score"]

            # Bar Chart
            ax1.bar(avg_salary.index, avg_salary.values, color="skyblue", edgecolor="black")
            ax1.set_title("Average Salary by Department")
            ax1.set_xlabel("Department")
            ax1.set_ylabel("Average Salary ($)")

            # Histogram
            ax2.hist(satisfaction_score.dropna(), bins=[i - 0.5 for i in range(1, 12)], rwidth=0.8, color="teal", edgecolor="black")
            ax2.set_title("Satisfaction Score Distribution")
            ax2.set_xlabel("Satisfaction Score")
            ax2.set_ylabel("Frequency")

            plt.tight_layout()
            plt.savefig(output_path, dpi=120, bbox_inches="tight")
            plt.close()
            print(f"Visualizations saved to {output_path}")
        except Exception as e:
            print(f"Error generating visualizations: {e}")

    def export(self, output_path="output/clean_data.csv"):
        """Save the cleaned self.df to a CSV at `output_path`."""
        if self.df is None or self.df.empty:
            print("Export skipped: DataFrame is empty.")
            return

        try:
            dir_name = os.path.dirname(output_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            self.df.to_csv(output_path, index=False)
            print(f"Cleaned data exported to {output_path}")
        except Exception as e:
            print(f"Error exporting data: {e}")

    def run(self):
        """Execute the full pipeline: clean → analyze → visualize → export."""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            base_dir = os.getcwd()

        chart_path = os.path.join(base_dir, "output", "charts.png")
        csv_path = os.path.join(base_dir, "output", "clean_data.csv")

        try:
            self.clean()
            results = self.analyze()
            self.visualize(chart_path)
            self.export(csv_path)
            return results
        except Exception as e:
            print(f"Pipeline execution failed: {e}")
            return None