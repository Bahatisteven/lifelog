import csv
import os
from collections import Counter
from datetime import datetime, date, timedelta

import pandas as pd
import matplotlib.pyplot as plt

from lifelog.data_handler import FILE_PATH

EXPORT_DIR = "exports"


# cleaning and loading
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """clean and standardize the dataframe"""
    df["mood"] = df["mood"].fillna("Unknown")
    df = df.drop_duplicates()
    df["activity"] = df["activity"].str.strip().str.title()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    return df


def load_and_clean_data(file_path=FILE_PATH) -> pd.DataFrame:
    """load CSV and return cleaned DataFrame."""
    df = pd.read_csv(file_path)
    return clean_data(df)


# summaries
def summarize(file_path=FILE_PATH):
    """show overall summary of activities and moods"""
    total_hours, activities, moods = 0, [], []
    if not os.path.exists(file_path):
        print("No data yet.")
        return

    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) < 4:
                continue
            activities.append(row[1])
            moods.append(row[3])
            try:
                total_hours += float(row[2])
            except ValueError:
                pass

    print("\nSummary:")
    print(f"Total hours logged: {total_hours}")
    if activities:
        activity, count = Counter(activities).most_common(1)[0]
        print(f"Most common activity: {activity} ({count} times)")
    if moods:
        mood, count = Counter(moods).most_common(1)[0]
        print(f"Most common mood: {mood} ({count} times)")


def weekly_summary(file_path=FILE_PATH):
    """show logs and insights for the current week"""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    total_hours, weekday_hours = 0, {i: 0.0 for i in range(7)}

    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) < 4:
                continue
            try:
                log_date = datetime.strptime(row[0], "%Y-%m-%d").date()
                hours = float(row[2])
            except Exception:
                continue
            if start_of_week <= log_date <= end_of_week:
                total_hours += hours
                weekday_hours[log_date.weekday()] += hours

    print("\nWeekly Summary:")
    print(f"Week of {start_of_week} → {end_of_week}")
    print(f"Total hours logged this week: {total_hours}")
    if total_hours > 0:
        best_day = max(weekday_hours, key=lambda k: weekday_hours[k])
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print(f"Most productive day: {days[best_day]} ({weekday_hours[best_day]} hours)")


def date_range_summary(file_path=FILE_PATH):
    """show logs and insights for a specific date range"""
    try:
        start_str = input("Enter start date (YYYY-MM-DD): ")
        end_str = input("Enter end date (YYYY-MM-DD): ")
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    if start_date > end_date:
        print("Start date must be before end date.")
        return

    total_hours, activities, moods = 0, [], []
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) < 4:
                continue
            try:
                log_date = datetime.strptime(row[0], "%Y-%m-%d").date()
                hours = float(row[2])
            except Exception:
                continue
            if start_date <= log_date <= end_date:
                total_hours += hours
                activities.append(row[1])
                moods.append(row[3])

    print(f"\nSummary for {start_date} → {end_date}:")
    print(f"Total hours: {total_hours}")
    if activities:
        activity, count = Counter(activities).most_common(1)[0]
        print(f"Most common activity: {activity} ({count} times)")
    if moods:
        mood, count = Counter(moods).most_common(1)[0]
        print(f"Most common mood: {mood} ({count} times)")


# export functions
def export_cleaned_data(df):
    path = os.path.join(EXPORT_DIR, "lifelog_cleaned.csv")
    df.to_csv(path, index=False)
    print(f"Cleaned dataset exported to {path}")


def export_aggregates(df):
    avg_duration = df.groupby("activity")["duration"].mean()
    avg_duration.to_csv(os.path.join(EXPORT_DIR, "avg_duration_per_activity.csv"))
    print("Average duration per activity exported")

    hours_per_weekday = df.groupby(df["date"].dt.day_name())["duration"].sum()
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours_per_weekday = hours_per_weekday.reindex(ordered_days)
    hours_per_weekday.to_csv(os.path.join(EXPORT_DIR, "hours_per_weekday.csv"))
    print("Total hours per weekday exported")


def export_summary_report(df):
    most_common_activity = df["activity"].value_counts().idxmax()
    most_common_mood = df["mood"].value_counts().idxmax()
    total_hours = df["duration"].sum()

    path = os.path.join(EXPORT_DIR, "summary_report.txt")
    with open(path, "w") as f:
        f.write("LifeLog Summary Report\n")
        f.write("=======================\n\n")
        f.write(f"Most common activity: {most_common_activity}\n")
        f.write(f"Most common mood: {most_common_mood}\n")
        f.write(f"Total logged hours: {total_hours}\n")

    print(f"Summary report saved to {path}")


def export_charts(df):
    avg_duration = df.groupby("activity")["duration"].mean()
    ax = avg_duration.plot(kind="bar", title="Average Duration per Activity")
    ax.set_ylabel("Hours")
    fig = ax.get_figure()
    fig.savefig(os.path.join(EXPORT_DIR, "avg_duration_per_activity.png"))
    plt.close(fig)

    hours_per_weekday = df.groupby(df["date"].dt.day_name())["duration"].sum()
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours_per_weekday = hours_per_weekday.reindex(ordered_days)
    ax = hours_per_weekday.plot(kind="bar", title="Total Hours by Weekday")
    ax.set_ylabel("Hours")
    fig = ax.get_figure()
    fig.savefig(os.path.join(EXPORT_DIR, "hours_per_weekday.png"))
    plt.close(fig)

    print("Charts exported as PNG files")


def export_all(df):
    """run all export functions at once"""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    export_cleaned_data(df)
    export_aggregates(df)
    export_summary_report(df)
    export_charts(df)
    print("\nAll exports completed!")
