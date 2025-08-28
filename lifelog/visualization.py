import os
import pandas as pd
import matplotlib.pyplot as plt
from lifelog.data_handler import FILE_PATH

def pandas_analysis(file_path=FILE_PATH):
    """run pandas & matplotlib analysis if data exists"""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print("No data available for analysis.")
        return

    df = pd.read_csv(file_path)
    if df.empty:
        print("No records to analyze.")
        return

    print("\nData Overview:")
    print(df.head())
    print(df.info())
    print(df.describe())

    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    print(f"\nTotal hours logged: {df['duration'].sum()}")
    print(f"Most common activity: {df['activity'].mode()[0]}")
    print(f"Most common mood: {df['mood'].mode()[0]}")
    print("\nAverage duration per activity:")
    print(df.groupby("activity")["duration"].mean())

    weekly_df = df.groupby(df["date"].dt.day_name())["duration"].sum()
    weekly_df.plot(kind="bar", title="Weekly Activity Duration")
    plt.ylabel("Hours")
    plt.show()
