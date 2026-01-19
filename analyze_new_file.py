import pandas as pd
import os

path = '/Users/mattcory/Desktop/aoc_master_price_list/data/samples/November Distributor PDF.xlsx'
print(f"--- Analyzing {path} ---")
try:
    # Read first 20 rows
    df = pd.read_excel(path, header=None, nrows=20)
    print(df.to_string())
except Exception as e:
    print(f"Error reading file: {e}")
