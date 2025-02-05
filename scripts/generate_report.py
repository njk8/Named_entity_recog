import pandas as pd

# File paths
DUPLICATE_REPORT_FILE = "../data/processed/duplicate_report.csv"
REPORT_SUMMARY_FILE = "../data/processed/report_summary.txt"

def generate_insights():
    """Analyze duplicate report and generate insights."""
    try:
        df = pd.read_csv(DUPLICATE_REPORT_FILE)
        if df.empty:
            print("✅ No duplicates found. No report generated.")
            return

        # Total duplicate records
        total_duplicates = len(df)

        # Most frequently duplicated products
        top_duplicated_products = df["Product"].value_counts().head(5)

        # Suppliers with highest duplicate POs
        top_suppliers = df["Supplier"].value_counts().head(5)

        # Save report summary
        with open(REPORT_SUMMARY_FILE, "w") as f:
            f.write(f"📊 **Duplicate Report Summary** 📊\n")
            f.write(f"-----------------------------------\n")
            f.write(f"🔹 Total Duplicate Orders: {total_duplicates}\n\n")
            f.write(f"🔹 Top Duplicated Products:\n{top_duplicated_products.to_string()}\n\n")
            f.write(f"🔹 Suppliers with Most Duplicates:\n{top_suppliers.to_string()}\n")

        print(f"✅ Report generated: {REPORT_SUMMARY_FILE}")

    except FileNotFoundError:
        print(f"❌ Error: {DUPLICATE_REPORT_FILE} not found!")

if __name__ == "__main__":
    generate_insights()
