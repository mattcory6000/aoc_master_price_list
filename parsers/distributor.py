import pandas as pd
import re

TEMPLATE_COLUMNS = [
    'SKU', 'CATEGORY', 'Producer_Name', 'Product_Name', 'Vintage', 
    'Volume_Amount', 'Volume_Unit', 'Pack_Size', 'Sleeve_Size', 'Container', 
    'FOB', 'FOB_SS', 'FOB_CD', 'FOB_XC', 'Country', 'Region/State', 
    'Appelation', 'Grapes', 'ABV', 'Keg Coupler', 'UPC/EAN', 'COLA', 
    'Weight', 'Cases_Per_Layer', 'Cases_Per_Pallet', 'Notes', 'Status', 'Score'
]

def parse_volume_unit(vol_str):
    if not isinstance(vol_str, str):
        return None, None
    match = re.search(r'([\d\.]+)\s*([a-zA-Z]+)', vol_str)
    if match:
        return match.group(1), match.group(2)
    return None, None

def parse_distributor(filepath):
    # No header row
    df_raw = pd.read_excel(filepath, header=None)
    
    data = []
    
    for index, row in df_raw.iterrows():
        # Check if row is valid (has SKU)
        if pd.isna(row[0]):
            continue
            
        sku = row[0]
        country = row[1]
        region = row[2]
        vintage = row[3]
        producer = row[4]
        product = row[5]
        vol_str = row[6]
        pack = row[7]
        fob = row[8] # Case Price
        
        vol, unit = parse_volume_unit(str(vol_str))
        
        entry = {col: None for col in TEMPLATE_COLUMNS}
        entry['SKU'] = sku
        entry['Country'] = country
        entry['Region/State'] = region
        entry['Vintage'] = vintage
        entry['Producer_Name'] = producer
        entry['Product_Name'] = product
        entry['Volume_Amount'] = vol
        entry['Volume_Unit'] = unit
        entry['Pack_Size'] = pack
        entry['FOB'] = fob
        
        data.append(entry)
        
    return pd.DataFrame(data)
