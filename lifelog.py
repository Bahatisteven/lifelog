import csv
from collections import Counter
import os
from datetime import datetime, date, timedelta
import pandas as pd

df= pd.read_csv('lifelog.csv')

print(df.head())  
print(df.info())    
print(df.describe())


FILE_PATH = "lifelog.csv"


def init_file(file_path=FILE_PATH):
    """Create CSV with header if it doesn't exist"""
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Activity", "Duration (hrs)", "Mood"])


def add_activity(file_path=FILE_PATH):
    """ask user for details and save activity into CSV"""
    date = input("Enter date (YYYY-MM-DD): ")
    activity = input("Enter activity name: ")
    duration = input("Enter duration in hours: ")
    mood = input("Enter your mood: ")
    tags = input("Enter tags (comma-separated, e.g. health,workout): ")
    notes = input("Enter any notes (optional): ")


    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        if file.tell() == 0:
         # if the file is empty, write header  
         writer.writerow(["Date", "Activity", "Duration", "Mood", "Tags", "Notes"])
        writer.writerow([date, activity, duration, mood, tags, notes])

    print("Activity saved successfully!\n")


def date_range_summary():
    """show logs and insights for a specific date range"""
    try:
        start_str = input("Enter start date (YYYY-MM-DD): ")
        end_str = input("Enter end date(YYYY-MM-DD): ")

        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    if start_date > end_date: 
        print("Start date must be before end date.")

        total_hours = 0
        activities = []
        moods = []

        with open(FILE_PATH, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None) # skip header
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
    """Show summary of activities and moods"""
    total_hours = 0
    activities = []
    moods = []

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



date_obj = datetime.strptime("2025-08-24", "%Y-%m-%d").date()

def weekly_summary(file_path=FILE_PATH):
    """show logs and insights for the current week"""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # monday
    end_of_week = start_of_week + timedelta(days=6)          # sunday

    total_hours = 0
    weekday_hours = {i: 0.0 for i in range(7)}  # 0=mon ... 6=sun

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
                continue  # skip bad rows

            # keep only this week
            if start_of_week <= log_date <= end_of_week:
                total_hours += hours
                weekday_hours[log_date.weekday()] += hours

    print("\nWeekly Summary:")
    print(f"Week of {start_of_week} → {end_of_week}")
    print(f"Total hours logged this week: {total_hours}")

    if total_hours > 0:
        # find most productive day
        best_day = max(weekday_hours, key=lambda k: weekday_hours[k])
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        print(f"Most productive day: {days[best_day]} ({weekday_hours[best_day]} hours)")


# app entry point

def main():
    init_file()

    while True:
        print("\n=== LifeLog Menu ===")
        print("1. Add new activity")
        print("2. Show all logs")
        print("3. Show summary")
        print("4. Weekly summary")
        print("5. Date range summary")
        print("6. Quit")

        choice = input("Choose an option (1-6): ")

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
            print("👋Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
