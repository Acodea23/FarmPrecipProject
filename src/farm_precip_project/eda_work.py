import pandas as pd
import matplotlib.pyplot as plt

def basic_summary(df):
    print(df.head())
    print(df.describe())
    print(df.isna().sum())

