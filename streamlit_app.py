# import streamlit as st
# import pandas as pd
# import farm_precip_project as fpp

# # https://farmprecipproject-overview.streamlit.app/

# st.title("State Farm Precipitation and Income Data Analysis")
# st.subheader("Highlights of an analysis performed using the farm_precip_project package")


import os
import io
import pandas as pd
import streamlit as st

# Visualization libraries for display and backup plots
import matplotlib.pyplot as plt
import seaborn as sns

# Your package functions
from farm_precip_project import (
    read_url_txt,
    normalized_data,
    merge_csvs,
    remove_outliers,
    corr_and_plot,
    center_column,
    make_scatter_w_cat
)

# --------------------------
# App config
# --------------------------
st.set_page_config(
    page_title="Farm Income vs PDSI – Analysis App",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Farm Income vs PDSI – Streamlit App")
st.markdown("""
This app reproduces the workflow from your Quarto doc using your `farm_precip_project` package:
- Scrape PDSI from NCEI
- Normalize monthly values to yearly averages
- Merge with Farm Income data
- Clean based on EDA findings (e.g., outliers, optional drop of 2014)
- Correlation analysis and scatterplots (including color by state)

Use the **sidebar** to adjust parameters and re-run analysis.
""")

# --------------------------
# Sidebar controls
# --------------------------
st.sidebar.header("Controls")

# File naming
txt_name = st.sidebar.text_input("PDSI raw text filename", value="rain.txt")
csv_name_dirty = st.sidebar.text_input("PDSI raw CSV filename", value="rain_dirty.csv")
csv_name_clean = st.sidebar.text_input("PDSI yearly-avg CSV filename", value="rain_clean.csv")
combined_csv_name = st.sidebar.text_input("Merged CSV filename", value="combined_farm_precip.csv")

# Outlier removal settings
st.sidebar.subheader("Outlier Removal (PDSI)")
outlier_column = st.sidebar.text_input("Column for outlier check", value="yearly_avg")
threshold = st.sidebar.number_input("Threshold", value=-50.0, step=1.0, format="%.1f")
lower = st.sidebar.checkbox("Treat threshold as lower bound (remove values < threshold)", value=True)

# Optional filter to drop problematic year noted in EDA
drop_2014 = st.sidebar.checkbox("Drop year 2014 (known collection issues)", value=True)

# Columns for analysis
st.sidebar.subheader("Analysis Columns")
colx = st.sidebar.text_input("X column (PDSI)", value="yearly_avg")
coly_raw_income = "Value of crop production"
coly_centered = st.sidebar.text_input("Centered income column name", value="income_centered")
group_on = ["state", "year"]

n_digits = st.sidebar.number_input("Correlation: number of digits", value=4, min_value=0)

# Plot filenames
plot_raw_name = st.sidebar.text_input("Plot filename (raw income vs PDSI)", value=f"plot_{colx}_vs_{coly_raw_income}.png")
plot_centered_name = st.sidebar.text_input("Plot filename (centered income vs PDSI)", value=f"plot_{colx}_vs_{coly_centered}.png")
plot_by_state_name = st.sidebar.text_input("Plot filename (centered income by state)", value=f"plot_{colx}_vs_{coly_centered}_by_state.png")

# --------------------------
# Constants for NCEI PDSI file
# --------------------------
url = "https://www.ncei.noaa.gov/pub/data/cirs/drd/drd964x.pdsi.txt"

# Fixed-width specs from your qmd
colspecs = [
    (0, 2), (2, 4), (4, 6), (6, 10),
    (10, 17), (17, 24), (24, 31), (31, 38),
    (38, 45), (45, 52), (52, 59), (59, 66),
    (66, 73), (73, 80), (80, 87), (87, 94)
]

cols = [
    "state", "division", "element", "year",
    "jan","feb","mar","apr","may","jun","jul","aug",
    "sep","oct","nov","dec"
]

months = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

# --------------------------
# Helper: show df head safely
# --------------------------
def show_df_head(df: pd.DataFrame, caption: str, n=5):
    st.caption(caption)
    st.dataframe(df.head(n), use_container_width=True)

# --------------------------
# Workflow sections
# --------------------------
st.header("1) Fetch & parse PDSI data")
col_fetch1, col_fetch2 = st.columns(2)

with col_fetch1:
    if st.button("Download and parse PDSI"):
        read_url_txt(url, txt_name, csv_name_dirty, colspecs, cols)
        st.success(f"PDSI parsed and saved as `{csv_name_dirty}` (and raw text `{txt_name}`).")
        if os.path.exists(csv_name_dirty):
            df_pdsi_dirty = pd.read_csv(csv_name_dirty)
            show_df_head(df_pdsi_dirty, "Head of PDSI monthly data (dirty CSV)")

with col_fetch2:
    st.info("This step uses `read_url_txt`, which internally calls `txt_to_csv` for fixed-width parsing.")

st.header("2) Compute yearly averages per state")
if st.button("Normalize monthly → yearly averages"):
    normalized_data(csv_name_dirty, "yearly_avg", csv_name_clean, months, groups=["state", "year"])
    st.success(f"Yearly averages computed and saved to `{csv_name_clean}`.")
    if os.path.exists(csv_name_clean):
        df_pdsi_clean = pd.read_csv(csv_name_clean)
        show_df_head(df_pdsi_clean, "Head of PDSI yearly averages")

st.header("3) Upload Farm Income Data")
uploaded_farm = st.file_uploader("Upload `FarmIncome_full.csv` (or similarly structured)", type=["csv"])
df_farm = None
if uploaded_farm is not None:
    df_farm = pd.read_csv(uploaded_farm)
    show_df_head(df_farm, "Head of Farm Income data")

st.header("4) Merge PDSI with Farm Income")
if st.button("Merge on ['state','year']"):
    if not os.path.exists(csv_name_clean):
        st.error("Missing PDSI yearly file. Please run step 2 first.")
    elif df_farm is None:
        st.error("Please upload Farm Income CSV in step 3.")
    else:
        # Save uploaded farm income to a temp file to pass into merge_csvs
        tmp_farm_name = "FarmIncome_full_uploaded.csv"
        df_farm.to_csv(tmp_farm_name, index=False)

        merge_csvs(combined_csv_name, [tmp_farm_name, csv_name_clean], group_on)
        st.success(f"Merged dataset saved as `{combined_csv_name}`.")
        if os.path.exists(combined_csv_name):
            df_combined = pd.read_csv(combined_csv_name)
            show_df_head(df_combined, "Head of merged data")
            st.download_button(
                label="Download merged CSV",
                data=df_combined.to_csv(index=False).encode("utf-8"),
                file_name=combined_csv_name,
                mime="text/csv"
            )

st.header("5) Cleaning (outliers and optional year filter)")
df_clean = None
if os.path.exists(combined_csv_name):
    df_combined = pd.read_csv(combined_csv_name)

    # Remove outliers on PDSI yearly averages
    df_clean = remove_outliers(df_combined, outlier_column, threshold, lower=lower)

    # Optional: drop year 2014 based on EDA findings
    if drop_2014 and "year" in df_clean.columns:
        df_clean = df_clean[df_clean["year"] != 2014]

    st.success("Cleaning applied.")
    show_df_head(df_clean, "Head of cleaned data")

    st.download_button(
        label="Download cleaned CSV",
        data=df_clean.to_csv(index=False).encode("utf-8"),
        file_name="combined_farm_precip_cleaned.csv",
        mime="text/csv"
    )
else:
    st.warning("Merged CSV not found. Complete steps 1–4 first.")

st.header("6) Analysis: Correlation & Scatterplots")

if df_clean is not None:
    # --- Raw income vs PDSI ---
    st.subheader("6a) Raw income vs PDSI")
    if colx in df_clean.columns and coly_raw_income in df_clean.columns:
        # Save temp cleaned file to let package plotting function read from it if needed
        tmp_clean_name = "combined_farm_precip_cleaned_current.csv"
        df_clean.to_csv(tmp_clean_name, index=False)

        # Use your package function to produce and save a plot
        corr_and_plot(df_clean, colx, coly_raw_income, plot_raw_name, n_digits)

        # Also compute correlation manually for display
        corr_raw = df_clean[colx].corr(df_clean[coly_raw_income])
        st.metric("Correlation (raw income vs PDSI)", f"{corr_raw:.{n_digits}f}")

        if os.path.exists(plot_raw_name):
            st.image(plot_raw_name, caption=f"Scatter: {colx} vs {coly_raw_income}", use_column_width=True)
            with open(plot_raw_name, "rb") as f:
                st.download_button("Download plot (raw)", f.read(), file_name=plot_raw_name, mime="image/png")
    else:
        st.error(f"Columns `{colx}` and/or `{coly_raw_income}` not found in cleaned data.")

    # --- Center income by state, then analyze vs PDSI ---
    st.subheader("6b) Centered income vs PDSI")
    if coly_raw_income in df_clean.columns and "state" in df_clean.columns:
        df_centered = center_column(df_clean, coly_raw_income, "state", coly_centered)
        show_df_head(df_centered[[ "state", "year", colx, coly_raw_income, coly_centered ]], "Head of centered income data")

        corr_and_plot(df_centered, colx, coly_centered, plot_centered_name, n_digits)
        corr_centered = df_centered[colx].corr(df_centered[coly_centered])
        st.metric("Correlation (centered income vs PDSI)", f"{corr_centered:.{n_digits}f}")

        if os.path.exists(plot_centered_name):
            st.image(plot_centered_name, caption=f"Scatter: {colx} vs {coly_centered}", use_column_width=True)
            with open(plot_centered_name, "rb") as f:
                st.download_button("Download plot (centered)", f.read(), file_name=plot_centered_name, mime="image/png")

        # --- Color-by-state scatter ---
        st.subheader("6c) Color-by-state scatter (centered income)")
        make_scatter_w_cat(df_centered, colx, coly_centered, "state", plot_by_state_name)
        if os.path.exists(plot_by_state_name):
            st.image(plot_by_state_name, caption=f"Scatter by state: {colx} vs {coly_centered}", use_column_width=True)
            with open(plot_by_state_name, "rb") as f:
                st.download_button("Download plot (by-state)", f.read(), file_name=plot_by_state_name, mime="image/png")
    else:
        st.error("Cannot center: missing `Value of crop production` or `state` column.")

st.markdown("---")
st.caption("Notes:")
