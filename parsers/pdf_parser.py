import pandas as pd
import re
from pypdf import PdfReader

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

def parse_volume_pack(uom_str):
    # "12/750ml" -> 12, 750, ml
    if not isinstance(uom_str, str):
        return None, None, None
    match = re.search(r'(\d+)\s*/\s*([\d\.]+)\s*([a-zA-Z]+)', uom_str)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None, None, None

def parse_pdf(filepath):
    reader = PdfReader(filepath)
    data = []
    
    current_country = None
    current_producer = None
    current_region = None
    
    # Regex for product line:
    # LD2910020 La Mision Vino Tinto Chileno Pisador 2020 12/750ml (2020) (12/750ml) (2020) (12/750ml) $186/cs 58.25
    # SKU: Starts with LD, followed by digits.
    # Price: $XXX/cs
    
    line_regex = re.compile(r'^(LD\d+)\s+(.+?)\s+(\d+/\s*[\d\.]+[a-zA-Z]+).*\$([\d\.]+)/cs')
    
    for page in reader.pages:
        text = page.extract_text()
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Check for Country Header
            if line in KNOWN_COUNTRIES:
                current_country = line
                current_producer = None
                current_region = None
                continue
                
            # Check for Producer/Region Header
            # Heuristic: Contains comma, no SKU, no Price
            # e.g. "Clemens Busch, Mosel"
            if ',' in line and '$' not in line and not line.startswith('LD'):
                parts = line.split(',', 1)
                current_producer = parts[0].strip()
                if len(parts) > 1:
                    current_region = parts[1].strip()
                continue
            
            # Check for Product Line
            match = line_regex.search(line)
            if match:
                sku = match.group(1)
                raw_name = match.group(2)
                pack_str = match.group(3) # 12/750ml
                fob = match.group(4)
                
                # Extract Vintage from name or raw text if possible
                # The line often has vintage in name "Pisador 2020"
                # Or in parens "(2020)"
                vintage = None
                vintage_match = re.search(r'\b(19|20)\d{2}\b', raw_name)
                if vintage_match:
                    vintage = vintage_match.group(0)
                
                # Clean name: remove vintage if at end
                product_name = raw_name
                
                pack, vol, unit = parse_volume_pack(pack_str)
                
                entry = {col: None for col in TEMPLATE_COLUMNS}
                entry['SKU'] = sku
                entry['Country'] = current_country
                entry['Producer_Name'] = current_producer
                entry['Region/State'] = current_region
                entry['Product_Name'] = product_name
                entry['Vintage'] = vintage
                entry['Pack_Size'] = pack
                entry['Volume_Amount'] = vol
                entry['Volume_Unit'] = unit
                entry['FOB'] = fob
                
                data.append(entry)
                
    return pd.DataFrame(data)
