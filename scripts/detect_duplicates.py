import os
import pandas as pd

# Paths
CLEANED_DATA_FILE = "../data/processed/cleaned_data.csv"
DEDUPLICATED_DATA_FILE = "../data/reports/deduplicated_final_data.csv"
DUPLICATE_REPORT_FILE = "../data/reports/duplicate_report.csv"


def detect_duplicates():
    """Identify duplicate purchase orders based on Delivery Date, Product, Units, and Item Code."""
    if not CLEANED_DATA_FILE:
        print(f"Error: {CLEANED_DATA_FILE} not found!")
        return
    
    df = pd.read_csv(CLEANED_DATA_FILE)

    # Define duplicate checking criteria
    duplicate_columns = ["Delivery Date", "Product", "Units", "Item Code","Client Name"]

    #FINDING
    duplicates = df[df.duplicated(subset=duplicate_columns, keep=False)]

    # Remove duplicates (keeping the first occurrence)
    deduplicated_df = df.drop_duplicates(subset=duplicate_columns, keep="first")

    if not duplicates.empty:
        duplicates.to_csv(DUPLICATE_REPORT_FILE, index=False)
        print(f" {len(duplicates)} duplicates found and report saved to {DUPLICATE_REPORT_FILE}")
        deduplicated_df.to_csv(DEDUPLICATED_DATA_FILE, index=False)
        print(f" Deduplicated report with  {len(deduplicated_df)} entries saved to {DEDUPLICATED_DATA_FILE}")
    else:
        print(" No duplicates found.")

if __name__ == "__main__":
    detect_duplicates()