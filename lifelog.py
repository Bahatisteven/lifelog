import csv
from collections import Counter
import os
from datetime import datetime, date, timedelta
import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = "lifelog.csv"

# CSV initialization & logging

def init_file(file_path=FILE_PATH):
    """create CSV with header if it doesn't exist"""
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "activity", "duration", "mood", "tags", "notes"])


def add_activity(file_path=FILE_PATH):
    """user details and save activity into CSV"""
    date_str = input("Enter date (YYYY-MM-DD): ")
    activity = input("Enter activity name: ")
    duration = input("Enter duration in hours: ")
    mood = input("Enter your mood: ")
    tags = input("Enter tags (comma-separated, e.g. health,workout): ")
    notes = input("Enter any notes (optional): ")

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date_str, activity, duration, mood, tags, notes])

    print("Activity saved successfully!\n")


# summaries

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
        next(reader, None)  # skip header
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


def show_logs(file_path=FILE_PATH):
    """Display all saved activities"""
    print("\nYour LifeLog Entries:")
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def summarize(file_path=FILE_PATH):
    """Show overall summary of activities and moods"""
    total_hours, activities, moods = 0, [], []

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


def weekly_summary(file_path=FILE_PATH):
    """Show logs and insights for the current week"""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # monday
    end_of_week = start_of_week + timedelta(days=6)          # sunday

    total_hours, weekday_hours = 0, {i: 0.0 for i in range(7)}

    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
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


# pandas and plot analysis

def pandas_analysis(file_path=FILE_PATH):
    """Run pandas & matplotlib analysis if data exists"""
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

    # clean up columns
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # summaries
    print(f"\nTotal hours logged: {df['duration'].sum()}")
    print(f"Most common activity: {df['activity'].mode()[0]}")
    print(f"Most common mood: {df['mood'].mode()[0]}")
    print("\nAverage duration per activity:")
    print(df.groupby("activity")["duration"].mean())

    # weekly chart
    weekly_df = df.groupby(df["date"].dt.day_name())["duration"].sum()
    weekly_df.plot(kind="bar", title="Weekly Activity Duration")
    plt.ylabel("Hours")
    plt.show()


# entry point

def main():
    init_file()
    while True:
        print("\n=== LifeLog Menu ===")
        print("1. Add new activity")
        print("2. Show all logs")
        print("3. Show summary")
        print("4. Weekly summary")
        print("5. Date range summary")
        print("6. Advanced analysis (pandas + charts)")
        print("7. Quit")

        choice = input("Choose an option (1-7): ")

        if choice == "1":
            add_activity()
        elif choice == "2":
            show_logs()
        elif choice == "3":
            summarize()
        elif choice == "4":
            weekly_summary()
        elif choice == "5":
            date_range_summary()
        elif choice == "6":
            pandas_analysis()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
