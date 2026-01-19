# AOC Master Price List

A Python parsing engine that transforms messy FOB pricing sheets (Excel, CSV, PDF) from alcohol suppliers into a single, standardized CSV format for distributors.

## Overview

This project is part of **BeverageData.ai**. Wine & spirits suppliers each use their own pricing sheet formats—inconsistent layouts, merged cells, metadata in random rows, and varying column names. This engine normalizes them all into a unified schema.

## Features

- **Multi-format support**: Parses `.xlsx`, `.csv`, and `.pdf` pricing sheets
- **Intelligent header detection**: Finds the real data row by scanning for keywords like "Item", "Description", "Vintage", or "Pack"
- **Cost normalization**: Automatically calculates case cost from bottle cost when needed
- **Producer/Product splitting**: Attempts to separate combined product strings
- **Aggregated output**: Combines all parsed files into a single master CSV

## Supported Suppliers

| Parser | File Pattern | Format |
|--------|-------------|--------|
| Bowler | `*Bowler*` | Excel |
| Skurnik | `*Skurnik*` | Excel |
| ZRS | `*ZRS*` | Excel |
| Distributor PDF | `*Distributor PDF*` | Excel |
| Generic PDF | `*.pdf` | PDF |

## Output Schema

All parsers output a DataFrame matching `data/template.csv`:

```
SKU, CATEGORY, Producer_Name, Product_Name, Vintage, Volume_Amount, 
Volume_Unit, Pack_Size, Sleeve_Size, Container, FOB, FOB_SS, FOB_CD, 
FOB_XC, Country, Region/State, Appelation, Grapes, ABV, Keg Coupler, 
UPC/EAN, COLA, Weight, Cases_Per_Layer, Cases_Per_Pallet, Notes, 
Status, Score
```

**Minimum required fields**: `Producer_Name` and `Product_Name`

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install pandas openpyxl pdfplumber
```

## Usage

1. Place source pricing sheets in `data/samples/`
2. Run the main script:

```bash
python main.py
```

3. Find the aggregated output in `master_aggregate.csv`

## Project Structure

```
├── data/
│   ├── samples/          # Source pricing sheets
│   └── template.csv      # Output schema definition
├── parsers/
│   ├── bowler.py         # Bowler Wines parser
│   ├── skurnik.py        # Skurnik Wines parser
│   ├── zrs.py            # ZRS Imports parser
│   ├── distributor.py    # Distributor PDF (xlsx) parser
│   └── pdf_parser.py     # Generic PDF parser
├── main.py               # Orchestrates parsing & aggregation
└── AGENT.md              # AI agent instructions
```

## Adding a New Parser

1. Create a new parser in `parsers/`
2. Define a `parse_<supplier>(filepath)` function that returns a DataFrame
3. Add file pattern matching in `main.py`
4. Ensure output matches `data/template.csv` schema

## Tech Stack

- Python 3.12+
- Pandas
- OpenPyXL (Excel parsing)
- pdfplumber (PDF parsing)
