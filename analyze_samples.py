import pandas as pd
import os

base_path = '/Users/mattcory/Desktop/aoc_master_price_list/data/samples'
files = [
    ' Bowler National Grid -  November 21, 2025 .xlsx',
    'AWS Skurnik Wines National Inventory - 11.01.25.xlsx',
    'ZRS National Pricebooks-12.xlsx'
]

for f in files:
    path = os.path.join(base_path, f)
    print(f"--- Analyzing {f} ---")
    try:
        # Read first few rows to find header
        # Some files might have metadata in first few rows, so we might need to skip rows.
        # Let's read raw first
        df = pd.read_excel(path, nrows=5, header=None)
        print("Raw first 5 rows:")
        print(df.to_string())
        print("\n")
    except Exception as e:
        print(f"Error reading {f}: {e}\n")
