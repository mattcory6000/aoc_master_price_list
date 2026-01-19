import pandas as pd

TEMPLATE_COLUMNS = [
    'SKU', 'CATEGORY', 'Producer_Name', 'Product_Name', 'Vintage', 
    'Volume_Amount', 'Volume_Unit', 'Pack_Size', 'Sleeve_Size', 'Container', 
    'FOB', 'FOB_SS', 'FOB_CD', 'FOB_XC', 'Country', 'Region/State', 
    'Appelation', 'Grapes', 'ABV', 'Keg Coupler', 'UPC/EAN', 'COLA', 
    'Weight', 'Cases_Per_Layer', 'Cases_Per_Pallet', 'Notes', 'Status', 'Score'
]

def parse_skurnik(filepath):
    # Read without header to access by index
    df_raw = pd.read_excel(filepath, header=None)
    
    data = []
    current_country = None
    
    # Iterate rows
    # Row 0 is header "SKU", "ORDER", "Producer"...
    for index, row in df_raw.iterrows():
        if index == 0: continue # Skip header
        
        col0 = row[0] # SKU or Country
        col2 = row[2] # Producer
        
        if pd.isna(col0):
            continue
            
        # Check if it's a country header
        # If Producer is NaN and SKU/Col0 has text, it's likely a header like "Argentina"
        if pd.isna(col2) and isinstance(col0, str):
            current_country = col0
            continue
            
        # Otherwise it's a data row
        sku = col0
        producer = col2
        product_name = row[3]
        vintage = row[4]
        vol = row[5]
        pack = row[6]
        fob = row[9] # FOBNJ 1 cs Price
        upc = row[16]
        
        entry = {col: None for col in TEMPLATE_COLUMNS}
        entry['SKU'] = sku
        entry['Producer_Name'] = producer
        entry['Product_Name'] = product_name
        entry['Vintage'] = vintage
        entry['Volume_Amount'] = vol
        # Volume Unit is likely 'ml' if vol is 750, but let's check if it's in the value
        # The analysis showed "750", so unit is implicit or separate?
        # Analysis: "750" in col 5. Let's assume 'ml' for now or leave blank.
        entry['Volume_Unit'] = 'ml' # Reasonable default for wine lists
        entry['Pack_Size'] = pack
        entry['FOB'] = fob
        entry['UPC/EAN'] = upc
        entry['Country'] = current_country
        
        data.append(entry)
        
    return pd.DataFrame(data)
