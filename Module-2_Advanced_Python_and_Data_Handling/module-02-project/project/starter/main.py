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
    # pipeline = DataPipeline(DATA_PATH)
    # results = pipeline.run()

    # TODO: print a short summary using the results dict, e.g.:
    # print(f"  Top location by headcount: {results['headcount_by_location'].idxmax()}")

    print("Pipeline not yet implemented — fill in pipeline.py to continue.")


if __name__ == "__main__":
    main()
