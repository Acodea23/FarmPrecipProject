import streamlit as st
import pandas as pd
import farm_precip_project as fpp
import matplotlib.pyplot as plt
import seaborn as sns
from farm_precip_project import (
    merge_csvs,
    make_scatter_w_cat,
    precip_trend_figure,
    crop_income_fig,
    remove_outliers,
    corr_and_plot,
    center_column
)


# # https://farmprecipproject-overview.streamlit.app/

st.title("State Farm Precipitation and Income Data Analysis")
st.subheader("Highlights of an analysis performed using the farm_precip_project package")


st.write("After scraping, cleaning, and merging the data, we have the following table:")

csvs = ["FarmIncome_full.csv", "rain_clean.csv"]
group_on = ["state", "year"]
new_csv_name = "combined_farm_precip.csv"

merge_csvs(new_csv_name, csvs, group_on)

st.markdown(pd.read_csv(new_csv_name).head(5).to_markdown())

st.write("After removing outliers from the data, we can visualize the correlation between yearly average precipitation and farm income:")

st.header("EDA")

df = pd.read_csv("combined_farm_precip.csv")

group_by = "year"
titles = ["Year", "Mean Normalized Precipitation", "Average Precipitation Across the U.S. Over Time"]
plot = precip_trend_figure(df, group_by,titles)
st.pyplot(plot)

st.write("We see that PDSI is stable over time, the only error is the data provided in 2014, which we will remove before analysis.")


group_by2 = "year"
titles2 = ["Year", "Mean Crop Cash Receipts", "Crop Income Trends Over Time"]
plot2 = crop_income_fig(df, group_by2, titles2)
st.pyplot(plot2)

st.write("Crop income has been steadily increasing over time, which we will have to be aware of during our analysis.")

st.header("Analysis of PDSI vs. Income")

df = pd.read_csv('combined_farm_precip.csv')
col_name = "yearly_avg"
threshold = -50

df = remove_outliers(df, col_name, threshold, lower = True)

colx = "yearly_avg"
coly = "Value of crop production"
plot_file = f"plot_{colx}_vs_{coly}.png"
n_digits = 4

plot3 = corr_and_plot(df, colx, coly, plot_file,n_digits)
st.pyplot(plot3)

st.write("We see little to no correlation between PDSI and crop income when the income is not normalized by state. " \
"This demonstrates that PDSI by itself does not accurately predict crop income. " \
"Some states have a larger base income than others. We instead want to focus on how each state's income's variance is related to PDSI.")

col_name = "yearly_avg"
col_group = "state"
col_stand_name = "income_centered"

df = center_column(df, col_name, col_group, col_stand_name)

# colx = "yearly_avg"
# coly = "income_centered"
# plot_file = f"plot_{colx}_vs_{coly}.png"
# n_digits = 4

# corr_and_plot(df, colx, coly, plot_file,n_digits)

st.write("After centering the income by state, we create a plot that colors by state to see if the state's data are each linear with a different intercept.")

colx = "yearly_avg"
coly = "income_centered"
colcat = "state"
plot_file = f"plot_{colx}_vs_{coly}_by_{colcat}.png"


plot5 = make_scatter_w_cat(df, colx, coly, colcat, plot_file)
st.pyplot(plot5)

st.write("We can see that each state's data is roughly linear with a different intercept, which is why centering the income by state was important. " \
"This further confirms that there is a relationship between PDSI and crop income when accounting for state")
