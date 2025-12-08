import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------
df = pd.read_csv('combined_farm_precip.csv')

# --------------------------------------------------------
# 1. BASIC SUMMARY CHECKS
# --------------------------------------------------------
print(df.head())
print(df.describe())
print(df.isna().sum())

def basic_summary(df):
    print(df.head())
    print(df.describe())
    print(df.isna().sum())

basic_summary(df)

# --------------------------------------------------------
# 2. TEMPORAL PRECIPITATION TREND
# --------------------------------------------------------
mean_precip_by_year = df.groupby("year")["yearly_avg"].mean()

plt.figure(figsize=(12,6))
plt.plot(mean_precip_by_year)
plt.xlabel("Year")
plt.ylabel("Mean Normalized Precipitation")
plt.title("Average Precipitation Across the U.S. Over Time")
plt.tight_layout()
plt.savefig("precip_over_time.png", dpi=300)
plt.close()

group_by = "year"
titles = ["1", "2", "3"]
def precip_trend_figure(df, group_by,titles):
    mean_precip_by_year = df.groupby(group_by)["yearly_avg"].mean()
    plt.figure(figsize=(12,6))
    plt.plot(mean_precip_by_year)
    plt.xlabel(titles[0])
    plt.ylabel("Mean Normalized Precipitation")
    plt.title("Average Precipitation Across the U.S. Over Time")
    plt.tight_layout()
    plt.savefig("precip_over_time.png", dpi=300)
    plt.close()


# --------------------------------------------------------
# 3. TEMPORAL CROP INCOME TREND
# --------------------------------------------------------
mean_income_by_year = df.groupby("year")["Crop cash receipts"].mean()

plt.figure(figsize=(12,6))
plt.plot(mean_income_by_year)
plt.xlabel("Year")
plt.ylabel("Mean Crop Cash Receipts")
plt.title("Crop Income Trends Over Time")
plt.tight_layout()
plt.savefig("crop_income_over_time.png", dpi=300)
plt.close()


# --------------------------------------------------------
# 4. SCATTER: PRECIPITATION VS INCOME
# --------------------------------------------------------
plt.figure(figsize=(12,6))
plt.scatter(df["yearly_avg"], df["Crop cash receipts"], s=10)
plt.xlabel("Normalized Precipitation")
plt.ylabel("Crop Cash Receipts")
plt.title("Relationship Between Precipitation and Crop Income")
plt.tight_layout()
plt.savefig("precip_vs_income_scatter.png", dpi=300)
plt.close()


# --------------------------------------------------------
# 5. STATE-LEVEL COMPARISON SCATTER
# --------------------------------------------------------
state_summary = df.groupby("state")[["yearly_avg", "Crop cash receipts"]].mean()

plt.figure(figsize=(12,6))
plt.scatter(state_summary["yearly_avg"], state_summary["Crop cash receipts"])
plt.xlabel("Mean Normalized Precipitation")
plt.ylabel("Mean Crop Cash Receipts")
plt.title("State-Level Comparison: Income vs Precipitation")
plt.tight_layout()
plt.savefig("state_level_precip_vs_income.png", dpi=300)
plt.close()


# --------------------------------------------------------
# 6. CORRELATION + HEATMAP SAVE
# --------------------------------------------------------
corr = df[["yearly_avg", "Crop cash receipts"]].corr()
print("\nCorrelation Matrix:\n", corr)

plt.figure(figsize=(6,5))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Correlation")
plt.xticks([0,1], ["Precip", "Income"])
plt.yticks([0,1], ["Precip", "Income"])
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=300)
plt.close()

print("All PNG files saved in the current directory.")
