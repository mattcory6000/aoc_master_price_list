import os
import pandas as pd
from parsers.bowler import parse_bowler
from parsers.skurnik import parse_skurnik
from parsers.zrs import parse_zrs

from parsers.distributor import parse_distributor
from parsers.pdf_parser import parse_pdf

DATA_DIR = '/Users/mattcory/Desktop/aoc_master_price_list/data/samples'
OUTPUT_FILE = '/Users/mattcory/Desktop/aoc_master_price_list/master_aggregate.csv'

def main():
    all_data = []
    
    files = os.listdir(DATA_DIR)
    for f in files:
        if f.startswith('.'): continue # Skip hidden files
        
        filepath = os.path.join(DATA_DIR, f)
        print(f"Processing {f}...")
        
        df = None
        try:
            if 'Bowler' in f:
                df = parse_bowler(filepath)
            elif 'Skurnik' in f:
                df = parse_skurnik(filepath)
            elif 'ZRS' in f:
                df = parse_zrs(filepath)
            elif 'Distributor PDF' in f:
                df = parse_distributor(filepath)
            elif f.endswith('.pdf'):
                df = parse_pdf(filepath)
            else:
                print(f"Skipping {f}: No matching parser found.")
                continue
                
            if df is not None and not df.empty:
                print(f"  -> Parsed {len(df)} rows.")
                all_data.append(df)
            else:
                print(f"  -> Warning: No data parsed from {f}")
                
        except Exception as e:
            print(f"  -> Error parsing {f}: {e}")
            import traceback
            traceback.print_exc()

    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        master_df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nSuccess! Master aggregate saved to {OUTPUT_FILE}")
        print(f"Total rows: {len(master_df)}")
        print("Columns:", list(master_df.columns))
    else:
        print("\nNo data collected.")

if __name__ == "__main__":
    main()
