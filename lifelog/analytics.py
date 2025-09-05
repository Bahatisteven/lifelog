import csv
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, date, timedelta
import os
from lifelog.data_handler import FILE_PATH

EXPORT_DIR = "exports"

# load csv file
def load_and_clean_data(file_path=FILE_PATH):
    df = pd.read_csv(file_path)
    df = clean_data(df)
    return df


# load and clean data
df = load_and_clean_data(FILE_PATH)

# check for missing values in columns
print("Missing values per column:")
print(df.isnull().sum())

df["activity"] = df["activity"].str.strip().str.title() # " running " -> "Running"

# save cleaned data 
df.to_csv("lifelog_cleaned.csv", index=False)

# export aggregated CSVs
def export_aggregates(df):
    avg_duration = df.groupby("activity")["duration"].mean()
    avg_duration.to_csv(os.path.join(EXPORT_DIR, "avg_duration_per_activity.csv"))
    print("Average duration per activity exported")

    hours_per_weekday = df.groupby(df["date"].dt.day_name())["duration"].sum()
    ordered_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    hours_per_weekday = hours_per_weekday.reindex(ordered_days)
    hours_per_weekday.to_csv(os.path.join(EXPORT_DIR, "hours_per_weekday.csv"))
    print("Total hours per weekday exported")


# export cleaned dataset
def export_cleaned_data(df):
    """export cleaned dataset to CSV"""
    path = os.path.join(EXPORT_DIR, "lifelog_cleaned.csv")
    df.to_csv(path, index=False)
    print(f"Cleaned dataset exported to {path}")


def clean_data(df):
    df["mood"] = df["mood"].fillna("Unknown") # filling missing words with "Unknown"
    df = df.drop_duplicates()   # remove duplicate rows
    df["activity"] = df["activity"].str.strip().str.title() # " running " -> "Running"
    df["date"] = pd.to_datetime(df["date"], errors="coerce") 
    df = df.dropna(subset=["date"])
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    return df
# Already loaded and cleaned above, so this is not needed:
# df = clean_data(df)
df.columns = ["date", "activity", "duration", "mood"]
df.columns = ["date", "activity", "duration", "mood"]

print("\n--- GROUP BY & AGGREGATIONS ---\n")

# average duration per activity
avg_duration = df.groupby("activity")["duration"].mean()
print("Average duration per activity:\n", avg_duration, "\n")

# count of moods per activity
mood_counts = df.groupby(["activity", "mood"]).size()
print("Mood counts per activity:\n", mood_counts, "\n")

# most common activity overall
most_common_activity = df["activity"].value_counts().head(1)
print("Most common activity:\n", most_common_activity, "\n")

# average duration per activity
avg_duration.plot(kind="bar", title="Average Duration per Activity")
plt.ylabel("Hours")
plt.show() 

# drop rows where date could be parsed 
df = df.dropna(subset=["date"])

print("\n--- DATE/TIME ANALYSIS ---\n")

# hours per week day
hours_per_weekday = df.groupby(df["date"].dt.day_name())["duration"].sum()
print("Total hours per weekday:\n", hours_per_weekday, "\n")

# sort weekends in order 
ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hours_per_weekday = hours_per_weekday.reindex(ordered_days)

# plot weekday trends
hours_per_weekday.plot(kind="bar", title="Total Hours by Weekday")
plt.ylabel("Hours")
plt.show()

# monthly activity totals
monthly_hours = df.groupby(df["date"].dt.to_period("M"))["duration"].sum()
print("Total hours per month:\n", monthly_hours, "\n")

# plot monthly trends
monthly_hours.plot(kind="line", marker="o", title="Total Hours by Month")
plt.xlabel("Month")
plt.ylabel("Hours")
plt.show()





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

    print(f"\nSummary:")
    print(f"Total hours logged: {total_hours}")
    if activities:
        activity, count = Counter(activities).most_common(1)[0]
        print(f"Most common activity: {activity} ({count} times)")
    if moods:
        mood, count = Counter(moods).most_common(1)[0]
        print(f"Most common mood: {mood} ({count} times)")

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

def weekly_summary(file_path=FILE_PATH):
    """Show logs and insights for the current week"""
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
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        print(f"Most productive day: {days[best_day]} ({weekday_hours[best_day]} hours)")

def export_insights(df):
    """export key analysis results to CSV and TXT files"""

    # export cleaned dataset
    df.to_csv("exports/lifelog_cleaned.csv", index=False)
    print("Cleaned dataset exported to exports/lifelog_cleaned.csv")

    # export average duration per activity
    avg_duration = df.groupby("activity")["duration"].mean()
    avg_duration.to_csv("exports/avg_duration_per_activity.csv")
    print("Average duration per activity exported")

    # export total hours per weekday
    hours_per_weekday = df.groupby(df["date"].dt.day_name())["duration"].sum()
    hours_per_weekday.to_csv("exports/hours_per_weekday.csv")
    print("Total hours per weekday exported")

    # export summary report (TXT)
    most_common_activity = df["activity"].value_counts().idxmax()
    most_common_mood = df["mood"].value_counts().idxmax()

    with open("exports/summary_report.txt", "w") as f:
        f.write("LifeLog Summary Report\n")
        f.write("=======================\n\n")
        f.write(f"Most common activity: {most_common_activity}\n")
        f.write(f"Most common mood: {most_common_mood}\n")
        f.write(f"Total logged hours: {df['duration'].sum()}\n")

    print("Summary report saved to exports/summary_report.txt")
