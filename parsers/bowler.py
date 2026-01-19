import pandas as pd
import re

TEMPLATE_COLUMNS = [
    'SKU', 'CATEGORY', 'Producer_Name', 'Product_Name', 'Vintage', 
    'Volume_Amount', 'Volume_Unit', 'Pack_Size', 'Sleeve_Size', 'Container', 
    'FOB', 'FOB_SS', 'FOB_CD', 'FOB_XC', 'Country', 'Region/State', 
    'Appelation', 'Grapes', 'ABV', 'Keg Coupler', 'UPC/EAN', 'COLA', 
    'Weight', 'Cases_Per_Layer', 'Cases_Per_Pallet', 'Notes', 'Status', 'Score'
]

def parse_volume_pack(uom_str):
    """
    Parses strings like "12/ 750ml" or "24/ 375ml" into (pack_size, volume_amount, volume_unit)
    """
    if not isinstance(uom_str, str):
        return None, None, None
    
    # Regex for "12/ 750ml" or "12/750ml" or "12/ 1L"
    match = re.search(r'(\d+)\s*/\s*([\d\.]+)\s*([a-zA-Z]+)', uom_str)
    if match:
        pack = match.group(1)
        vol = match.group(2)
        unit = match.group(3)
        return pack, vol, unit
    return None, None, None

def parse_bowler(filepath):
    # Read file, header is on row 0 (which is index 0 in pandas if header=0)
    # Based on analysis, the header row seems to be row 0.
    df_raw = pd.read_excel(filepath, header=0)
    
    # Filter out rows where SKU (Column 1, 'DB...') is NaN
    # The analysis showed SKU is in the second column (index 1) which is named 'Unnamed: 1' or similar if header is messy,
    # but let's look at the analysis output again.
    # Analysis:
    #    0            1                    2 ...
    # 0  NaN          NaN             Producer ...
    # 3  ORGANIC    DB6293-NV  Sonnhof Social Club ...
    
    # It seems row 0 contains "Producer", "Product Name" etc in columns 2, 3.
    # But column 1 has the SKU.
    # Let's reload with header=0 and see column names.
    # Actually, looking at the analysis:
    # Row 0: NaN, NaN, Producer, Product Name...
    # So if we read with header=0, the columns will be named "Producer", "Product Name" etc.
    # But Column 0 and 1 might be named "Unnamed: 0", "Unnamed: 1".
    
    # Let's standardize column access by index to be safe, as column names might vary or be NaN.
    # We'll read without header first to map by index, then drop the header row.
    df_raw = pd.read_excel(filepath, header=None)
    
    # The header row is row 0. Data starts from row 1?
    # Row 0 has "Producer" at index 2.
    # Let's iterate and build the list.
    
    data = []
    
    # Iterate from row 1 to skip the header row (row 0)
    for index, row in df_raw.iterrows():
        if index == 0: continue # Skip header row
        
        sku = row[1]
        if pd.isna(sku):
            continue # Skip rows without SKU (likely category headers or empty)
            
        producer = row[2]
        product_name = row[3]
        vintage = row[4]
        uom = row[5] # "12/ 750ml"
        fob = row[7] # "Cs" price
        region = row[12]
        grapes = row[15]
        upc = row[16]
        
        pack, vol, unit = parse_volume_pack(str(uom))
        
        # Map to template
        entry = {col: None for col in TEMPLATE_COLUMNS}
        entry['SKU'] = sku
        entry['Producer_Name'] = producer
        entry['Product_Name'] = product_name
        entry['Vintage'] = vintage
        entry['Pack_Size'] = pack
        entry['Volume_Amount'] = vol
        entry['Volume_Unit'] = unit
        entry['FOB'] = fob
        entry['Region/State'] = region
        entry['Grapes'] = grapes
        entry['UPC/EAN'] = upc
        # Default Country to Austria? The file had "AUSTRIA" in col 0 row 1.
        # But maybe we should leave it blank if not row-specific.
        # Analysis showed "AUSTRIA" in col 0. We could capture state.
        # For now, let's leave Country blank or infer from context if requested.
        # The prompt didn't strictly specify stateful country parsing for Bowler, but it might be good.
        # However, for now let's stick to the direct mapping.
        
        data.append(entry)
        
    return pd.DataFrame(data)
