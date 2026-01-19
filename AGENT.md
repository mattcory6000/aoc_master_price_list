# AGENT.md

## Project Goal
We are building a Python parsing engine for "BeverageData.ai".
The goal is to transform messy "FOB Pricing Sheets" (Excel/CSV) from alcohol suppliers into a single, standardized CSV format for a distributor. We'll encounter other formats, like the one PDF currently in the `data` folder, but we'll focus first on the .xlsx files.

## The Standard Output Schema
All parsers must output a DataFrame that strictly adheres to the headers defined in `data/template.csv`.
- **Crucial Rule:** If a source file misses a column (e.g., "Vintage"), the parser must create that column and fill it with `NaN` or an empty string to match the template.
- **Minimum Viable Data:** We must have `Producer Name` and `Product Name`.

## Parsing Rules & Heuristics
1. **Header Hunting:** Source files often have metadata (logos, addresses) in the first few rows. You must programmatically find the real header row by looking for keywords like "Item", "Description", "Vintage", or "Pack".
2. **Producer/Product Split:**
   - Ideally, extract `Producer` and `Product` into separate columns.
   - If they are combined in one cell (e.g., "Caymus Cabernet 2020"), try to split them.
   - If splitting is ambiguous, put the whole string in `Product Name` and leave `Producer` empty.
3. **Cost Normalization:**
   - We need **Case Cost**.
   - If the sheet lists **Bottle Cost**, you must identify the "Pack Size" (e.g., 12, 6) and calculate: `Case Cost = Bottle Cost * Pack Size`.
4. **Data Types:**
   - `Case Cost` must be a float (strip '$' and ',' symbols).
   - `Vintage` should be a string (to handle "NV" or "Multi").

## Tech Stack
- Python 3.12+
- Pandas
- OpenPyXL (for .xlsx)