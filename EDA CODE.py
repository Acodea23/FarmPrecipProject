import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('/mnt/data/combined_farm_precip (1).csv')

# -----------------------------
# 1. BASIC DATA OVERVIEW
# -----------------------------
print("\n---- HEAD ----")
print(df.head())

print("\n---- SUMMARY STATISTICS ----")
print(df.describe())

print("\n---- MISSING VALUES ----")
print(df.isna().sum())


# -----------------------------
# 2. TEMPORAL TRENDS
# -----------------------------
# Average precipitation per year (national mean across states)
mean_precip_by_year = df.groupby("year")["yearly_avg"].mean()

plt.figure(figsize=(12,6))
plt.plot(mean_precip_by_year)
plt.xlabel("Year")
plt.ylabel("Mean Normalized Precipitation")
plt.title("Average Precipitation Across the U.S. Over Time")
plt.tight_layout()
plt.show()


# -----------------------------
# 3. INCOME TRENDS OVER TIME
# -----------------------------
mean_income_by_year = df.groupby("year")["Crop cash receipts"].mean()

plt.figure(figsize=(12,6))
plt.plot(mean_income_by_year)
plt.xlabel("Year")
plt.ylabel("Mean Crop Cash Receipts")
plt.title("Crop Income Trends Over Time")
plt.tight_layout()
plt.show()


# -----------------------------
# 4. SCATTER: PRECIPITATION VS INCOME
# -----------------------------
plt.figure(figsize=(12,6))
plt.scatter(df["yearly_avg"], df["Crop cash receipts"], s=10)
plt.xlabel("Normalized Precipitation")
plt.ylabel("Crop Cash Receipts")
plt.title("Relationship Between Precipitation and Crop Income")
plt.tight_layout()
plt.show()


# -----------------------------
# 5. STATE-LEVEL COMPARISONS
# -----------------------------
# mean precipitation & income per state
state_summary = df.groupby("state")[["yearly_avg", "Crop cash receipts"]].mean()

plt.figure(figsize=(12,6))
plt.scatter(state_summary["yearly_avg"], state_summary["Crop cash receipts"])
plt.xlabel("Mean Normalized Precipitation")
plt.ylabel("Mean Crop Cash Receipts")
plt.title("State-Level Comparison: Income vs. Precipitation")
plt.tight_layout()
plt.show()


# -----------------------------
# 6. CORRELATION CHECKS 
# (helps identify multicollinearity risk)
# -----------------------------
corr = df[["yearly_avg", "Crop cash receipts"]].corr()
print("\n---- CORRELATION MATRIX ----")
print(corr)
