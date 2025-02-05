import os
import re
import json
import pandas as pd

# Paths to the extracted files
EXTRACTED_DATA_FILE = "../data/processed/extracted_data.json"
CLEANED_DATA_FILE = "../data/processed/cleaned_data.csv"

# Define regex patterns for extracting PO fields
PO_NUMBER_PATTERN = r"(PO-PO-\d+)"  # Pattern to extract PO number from content
DELIVERY_DATE_PATTERN = r"(?i)Delivery by\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})"  # Patern to capture delivery date
PRODUCT_PATTERN = r"(\d+\s*\d+\s*units\s*of\s*([^\(]+)\s*\()"  # Pattern to capture product and units
ITEM_CODE_PATTERN = r"\(Item Code:\s*([^)]+)\)"  # Pattern to capture Item Codee

# Keywords to capture in the Notes column
NOTES_KEYWORDS = ["urgent", "ASAP", "confirm availability"]

def clean_text(text):
    """Clean extracted text: remove extra spaces, special characters, and normalize text."""
    text = text.replace("\n", " ").strip()
    text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces
    return text

def extract_notes(text):
    """Extract notes based on specific keywords which iss mentioned above."""
    notes = []
    for keyword in NOTES_KEYWORDS:
        if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):  # Case-insensitive search
            notes.append(keyword)
    return ", ".join(notes) if notes else None  # Join keywords into a single string

def extract_fields(text):
    """Extract key fields from text using regex."""
    po_number = re.search(PO_NUMBER_PATTERN, text)
    delivery_date = re.search(DELIVERY_DATE_PATTERN, text)

    # Extract product, units, and item codes (finadall as there can be mutiple)
    product_matches = re.findall(PRODUCT_PATTERN, text)  # Extract product and units together as per the pattern, also using findall
    item_codes = re.findall(ITEM_CODE_PATTERN, text)  # Extract item codes

    # Combine product, units, and item codes into a list of dictionaries
    items = []
    for i, (unit_product, product) in enumerate(product_matches):
        if i < len(item_codes):  # Ensure there's a corresponding item code
            unit = re.search(r"\d+", unit_product).group()  # Extract units from the match
            items.append({
                "Product": product.strip(),
                "Units": unit,
                "Item Code": item_codes[i]
            })

    # Extract notes
    notes = extract_notes(text)

    return {
        "PO Number": po_number.group(1) if po_number else None, 
        "Delivery Date": delivery_date.group(1) if delivery_date else None,
        "Items": items,  # List of dictionaries containing product, units, and item code
        "Notes": notes  # Add extracted notes
    }


def clean_and_structure_data():
    """Load extracted data, clean and structure it, and save to CSV."""
    if not os.path.exists(EXTRACTED_DATA_FILE):
        print(f"Error: {EXTRACTED_DATA_FILE} not found!")
        return

    with open(EXTRACTED_DATA_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    structured_data = []
    for entry in raw_data:
        filename = entry["filename"]
        content = clean_text(entry["content"])
        extracted_fields = extract_fields(content)

        # Extract PO number from filename 
        po_from_filename = re.search(r"PO_\d+", filename)
        po_number = po_from_filename.group(0) if po_from_filename else None

        # Extract client name from filename
        client_name = re.sub(r"\.txt$", "", filename)  # Remove .txt extension
        client_name = re.sub(r"_PO_\d+$", "", client_name)  # Remove PO number prefix

        # Add extracted fields to the result
        extracted_fields["PO Number"] = po_number  # Override PO number from filename
        extracted_fields["Client Name"] = client_name
        structured_data.append(extracted_fields)

    # Convert structured data to a DataFrame for CSV output
    df = pd.DataFrame(structured_data)

    # Normalize item details for better CSV formatting
    df_items = df.explode("Items")  # Explode the list of items into separate rows
    df_items = pd.concat([df_items.drop(columns=["Items"]), df_items["Items"].apply(pd.Series)], axis=1)

    # Save the cleaned data to a CSV file
    df_items.to_csv(CLEANED_DATA_FILE, index=False)

clean_and_structure_data()