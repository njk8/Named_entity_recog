import os
import json
from tika import parser

# Paths to the datas

PROCESSED_DATA_DIR = "../data/processed/"

def extract_text_from_file(file_path):
    """Extract text from a given file using Apache Tika."""
    try:
        parsed = parser.from_file(file_path)
        return parsed["content"].strip() if parsed["content"] else ""
    except Exception as e:
        print(f"Error extracting {file_path}: {str(e)}")
        return None

def process_all_files():
    """Extract text from all files in the raw data directory."""
    extracted_data = []

    for filename in os.listdir(RAW_DATA_DIR):
        file_path = os.path.join(RAW_DATA_DIR, filename)

        if os.path.isfile(file_path):
            print(f"Processing: {filename}")
            extracted_text = extract_text_from_file(file_path)

            if extracted_text:
                extracted_data.append({
                    "filename": filename,
                    "content": extracted_text
                })

    # save extractedd data as JSON format
    output_file = os.path.join(PROCESSED_DATA_DIR, "extracted_data.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)

    print(f"Extraction completed. Data saved in {output_file}")

if __name__ == "__main__":
    process_all_files()
