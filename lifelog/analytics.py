import csv
from collections import Counter
from datetime import datetime, date, timedelta
import os
from lifelog.data_handler import FILE_PATH

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
