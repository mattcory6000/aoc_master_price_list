import pandas as pd
import re

TEMPLATE_COLUMNS = [
    'SKU', 'CATEGORY', 'Producer_Name', 'Product_Name', 'Vintage', 
    'Volume_Amount', 'Volume_Unit', 'Pack_Size', 'Sleeve_Size', 'Container', 
    'FOB', 'FOB_SS', 'FOB_CD', 'FOB_XC', 'Country', 'Region/State', 
    'Appelation', 'Grapes', 'ABV', 'Keg Coupler', 'UPC/EAN', 'COLA', 
    'Weight', 'Cases_Per_Layer', 'Cases_Per_Pallet', 'Notes', 'Status', 'Score'
]

KNOWN_COUNTRIES = {
    'FRANCE', 'ITALY', 'SPAIN', 'AUSTRIA', 'GERMANY', 'USA', 'UNITED STATES', 
    'ARGENTINA', 'CHILE', 'PORTUGAL', 'SOUTH AFRICA', 'NEW ZEALAND', 'AUSTRALIA',
    'GREECE', 'HUNGARY', 'SLOVENIA', 'CROATIA'
}

def parse_volume_unit(vol_str):
    # "200ml" -> 200, ml
    if not isinstance(vol_str, str):
        return None, None
    match = re.search(r'([\d\.]+)\s*([a-zA-Z]+)', vol_str)
    if match:
        return match.group(1), match.group(2)
    return None, None

def parse_zrs(filepath):
    df_raw = pd.read_excel(filepath, header=None)
    
    data = []
    current_country = None
    current_producer = None
    
    for index, row in df_raw.iterrows():
        col0 = row[0]
        col1 = row[1]
        
        if pd.isna(col0):
            continue
            
        # Check if header (Col 1 is NaN)
        if pd.isna(col1):
            text = str(col0).strip()
            # Heuristic: Check if it's a country
            # We'll normalize to upper for check
            if text.upper() in KNOWN_COUNTRIES:
                current_country = text
                current_producer = None
            else:
                current_producer = text
            continue
            
        # Data row
        sku = col0
        product_name = col1
        grapes = row[2]
        vintage = row[3]
        pack = row[4]
        vol_str = row[5]
        fob = row[6]
        
        vol, unit = parse_volume_unit(str(vol_str))
        
        entry = {col: None for col in TEMPLATE_COLUMNS}
        entry['SKU'] = sku
        entry['Producer_Name'] = current_producer
        entry['Product_Name'] = product_name
        entry['Vintage'] = vintage
        entry['Pack_Size'] = pack
        entry['Volume_Amount'] = vol
        entry['Volume_Unit'] = unit
        entry['FOB'] = fob
        entry['Grapes'] = grapes
        entry['Country'] = current_country
        
        data.append(entry)
        
    return pd.DataFrame(data)
