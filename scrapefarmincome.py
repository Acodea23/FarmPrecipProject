import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1. File paths (same folder as your current Excel files)
# ---------------------------------------------------------
farm_path = "FarmIncome.xlsx"
va_path   = "VA_State_US (1).xlsx"

# Read FarmIncome ONLY to grab the years and the column order you like
farm_df = pd.read_excel(farm_path, sheet_name="Sheet1")
years = sorted(farm_df["year"].unique())
cols  = list(farm_df.columns)

# ---------------------------------------------------------
# 2. State numbering: 1–48 in alphabetical order
# ---------------------------------------------------------
contiguous_states = [
    "Alabama",        # 1
    "Arizona",        # 2
    "Arkansas",       # 3
    "California",     # 4
    "Colorado",       # 5
    "Connecticut",    # 6
    "Delaware",       # 7
    "Florida",        # 8
    "Georgia",        # 9
    "Idaho",          # 10
    "Illinois",       # 11
    "Indiana",        # 12
    "Iowa",           # 13
    "Kansas",         # 14
    "Kentucky",       # 15
    "Louisiana",      # 16
    "Maine",          # 17
    "Maryland",       # 18
    "Massachusetts",  # 19
    "Michigan",       # 20
    "Minnesota",      # 21
    "Mississippi",    # 22
    "Missouri",       # 23
    "Montana",        # 24
    "Nebraska",       # 25
    "Nevada",         # 26
    "New Hampshire",  # 27
    "New Jersey",     # 28
    "New Mexico",     # 29
    "New York",       # 30
    "North Carolina", # 31
    "North Dakota",   # 32
    "Ohio",           # 33
    "Oklahoma",       # 34
    "Oregon",         # 35
    "Pennsylvania",   # 36
    "Rhode Island",   # 37
    "South Carolina", # 38
    "South Dakota",   # 39
    "Tennessee",      # 40
    "Texas",          # 41
    "Utah",           # 42
    "Vermont",        # 43
    "Virginia",       # 44
    "Washington",     # 45
    "West Virginia",  # 46
    "Wisconsin",      # 47
    "Wyoming",        # 48
]

# ---------------------------------------------------------
# 3. Helper: extract crop block for one state from VA workbook
# ---------------------------------------------------------
def extract_state_rows(sheet_name, state_id, years_needed):
    """
    Pulls crop-related data for one state from the VA workbook and
    returns a DataFrame with the same columns as FarmIncome.
    """
    df = pd.read_excel(va_path, sheet_name=sheet_name)

    # Row 1 (index 1) has the year labels as strings: '1924', '1925', ...
    year_row = df.iloc[1]
    # Map year (int) -> column name (e.g., 'Unnamed: 27')
    year_to_col = {
        int(v): col_name
        for col_name, v in year_row.items()
        if isinstance(v, str) and v.isdigit()
    }

    # First column holds row labels like 'Value of crop production', etc.
    labels = df.iloc[:, 0]

    def row_by_label(label):
        idx = labels[labels == label].index
        if len(idx) == 0:
            return None
        return df.loc[idx[0]]

    # Crop-block rows we want to match FarmIncome
    row_value  = row_by_label("Value of crop production")
    row_cash   = row_by_label("Crop cash receipts")
    row_cotton = row_by_label("Cotton")
    row_feed   = row_by_label("Feed crops")
    row_food   = row_by_label("Food grains")
    row_fruit  = row_by_label("Fruits and nuts")
    row_oil    = row_by_label("Oil crops")
    row_veg    = row_by_label("Vegetables and melons")
    row_other  = row_by_label("All other crops")
    row_home   = row_by_label("Home consumption")

    # There are multiple "Inventory adjustment" rows;
    # first one (right after the crop block) = crop inventory adjustment
    inv_indices = labels[labels == "Inventory adjustment"].index
    row_inv = df.loc[inv_indices[0]] if len(inv_indices) > 0 else None

    records = []
    for y in years_needed:
        col_name = year_to_col.get(int(y))
        if col_name is None:
            # If the sheet doesn't have that year, skip
            continue

        rec = {
            "state": state_id,
            "year": int(y),
            "Value of crop production":   row_value[col_name] if row_value is not None else np.nan,
            "Crop cash receipts":         row_cash[col_name] if row_cash is not None else np.nan,
            "Cotton":                     row_cotton[col_name] if row_cotton is not None else np.nan,
            "Feed crops":                 row_feed[col_name] if row_feed is not None else np.nan,
            "Food grains":                row_food[col_name] if row_food is not None else np.nan,
            "Fruits and nuts":            row_fruit[col_name] if row_fruit is not None else np.nan,
            "Oil crops":                  row_oil[col_name] if row_oil is not None else np.nan,
            "Vegetables and melons":      row_veg[col_name] if row_veg is not None else np.nan,
            "All other crops":            row_other[col_name] if row_other is not None else np.nan,
            "Home consumption":           row_home[col_name] if row_home is not None else np.nan,
            "Inventory adjustment":       row_inv[col_name] if row_inv is not None else np.nan,
        }
        records.append(rec)

    return pd.DataFrame.from_records(records)

# ---------------------------------------------------------
# 4. Build ALL 48 states from VA_State_US (1).xlsx
# ---------------------------------------------------------
all_states = []

for state_id, state_name in enumerate(contiguous_states, start=1):
    print(f"Processing state {state_id}: {state_name}")
    df_state = extract_state_rows(state_name, state_id, years)
    all_states.append(df_state)

all_states_df = pd.concat(all_states, ignore_index=True)

# Make sure column order matches original FarmIncome
all_states_df = all_states_df[cols]

# Sort by state, then year
all_states_df = all_states_df.sort_values(["state", "year"]).reset_index(drop=True)

# ---------------------------------------------------------
# 5. Save in the same location with a new name
# ---------------------------------------------------------
output_path = "FarmIncome_full.xlsx"
all_states_df.to_excel(output_path, sheet_name="Sheet1", index=False)

print(f"Done. Wrote {all_states_df.shape[0]} rows to {output_path}.")
