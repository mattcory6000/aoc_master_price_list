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
    print(f"=== Analyzing {f} ===")
    try:
        # Read first 20 rows without header to see layout
        df = pd.read_excel(path, header=None, nrows=20)
        print("First 10 rows (raw):")
        print(df.head(10).to_string())
        print("-" * 20)
    except Exception as e:
        print(f"Error reading {f}: {e}")
    print("\n")
