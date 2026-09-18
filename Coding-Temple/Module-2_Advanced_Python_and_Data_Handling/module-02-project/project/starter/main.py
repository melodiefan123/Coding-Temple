"""
main.py — Module 2 Project entry point
Run this file to execute your pipeline.

Once you've implemented DataPipeline in pipeline.py, running:
    python main.py
should load, clean, analyze, visualize, and export the data — all without errors.
"""

import os
from pipeline import DataPipeline

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "messy_employee_survey.csv")


def main():
    print("=" * 60)
    print("Employee Survey Data Pipeline")
    print("=" * 60)

    # TODO: uncomment these lines once pipeline.py is implemented
    pipeline = DataPipeline(DATA_PATH)
    results = pipeline.run()

    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS SUMMARY")
    print("=" * 60)

    if results: 
        for key, value in results.items():
            formatted_key = key.replace("_"," ").title()
            print(f"\n--- {formatted_key} ---")

            if hasattr(value, "to_string"):
                print(value.to_string())
            else: 
                print(value)

    # TODO: print a short summary using the results dict, e.g.:
    
        print("\n" + "-" * 40)
        print("KEY HIGHLIGHTS")
        print("-" * 40)

        if "headcount_by_location" in results and not results["headcount_by_location"].empty:
                top_loc = results["headcount_by_location"].idxmax()
                count = results["headcount_by_location"].max()
                print(f"• Top Location by Headcount: {top_loc} ({count} employees)")
                
        if "experience_salary_correlation" in results:
            corr = results["experience_salary_correlation"]
            print(f"• Experience-Salary Correlation: {corr:.3f}")

        print("\nPipeline execution complete! Check the 'output/' folder for charts and cleaned CSV.")

    else: 
        print("Pipeline failed - no results to display.")


    # print("Pipeline not yet implemented — fill in pipeline.py to continue.")


if __name__ == "__main__":
    main()
