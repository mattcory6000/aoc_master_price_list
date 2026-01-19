import sys
try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("No PDF library found. Please install pypdf or PyPDF2.")
        sys.exit(1)

path = '/Users/mattcory/Desktop/aoc_master_price_list/data/samples/NOVEMBER_25_FOBNJ.pdf'
print(f"--- Analyzing {path} ---")

try:
    reader = PdfReader(path)
    print(f"Number of pages: {len(reader.pages)}")
    
    # Extract text from first 2 pages
    for i in range(min(2, len(reader.pages))):
        print(f"\n--- Page {i+1} ---")
        page = reader.pages[i]
        text = page.extract_text()
        print(text)
        print("-" * 20)
        
except Exception as e:
    print(f"Error reading PDF: {e}")
