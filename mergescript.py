import pandas as pd

# -----------------------------
# 1. Load datasets
# -----------------------------
farm_path = "FarmIncome_full.xlsx"
rain_path = "rain_clean.csv"

farm = pd.read_excel(farm_path, sheet_name="Sheet1")
rain = pd.read_csv(rain_path)

# -----------------------------
# 2. Standardize column names
# -----------------------------
# Convert to lowercase for safety
farm.columns = farm.columns.str.lower()
rain.columns = rain.columns.str.lower()

# If rain_clean uses different names, fix them here:
# Example: rename "state_number" -> "state"
# rain = rain.rename(columns={"state_number": "state", "yr": "year"})

# -----------------------------
# 3. Ensure merge keys are numeric
# -----------------------------
farm["state"] = farm["state"].astype(int)
farm["year"] = farm["year"].astype(int)

rain["state"] = rain["state"].astype(int)
rain["year"] = rain["year"].astype(int)

# -----------------------------
# 4. Merge
# -----------------------------
merged = pd.merge(
    farm,
    rain,
    on=["state", "year"],    # merge keys
    how="inner"              # or "left" if you want all farm rows
)

# -----------------------------
# 5. Save output
# -----------------------------
output_path = "farm_precip_merged.xlsx"
merged.to_excel(output_path, index=False)

print("Merge complete. Rows in merged file:", len(merged))
print("Output saved as:", output_path)
