import csv
from collections import Counter


def add_activity(file_path="lifelog.csv"):
    """ask user for details and save activity into CSV"""
    activity = input("Enter activity name: ")
    duration = input("Enter duration in hours: ")
    mood = input("Enter your mood: ")
    date = input("Enter date (YYYY-MM-DD): ")

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, activity, duration, mood])

    print("Activity saved successfully!")


def show_logs(file_path="lifelog.csv"):
    """display all saved activities"""
    print("\nYour LifeLog Entries:")
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def summarize(file_path="lifelog.csv"):
    """show summary of activities and moods"""
    total_hours = 0
    activities = []
    moods = []

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 4:  # skip bad rows
                continue

            # collect
            activities.append(row[1])
            moods.append(row[3])

            # try counting hours
            try:
                total_hours += float(row[2])
            except ValueError:
                pass  # ignore non-numeric

    print(f"\nTotal hours logged: {total_hours}")

    if activities:
        most_common_activity = Counter(activities).most_common(1)[0]
        print(f"Most common activity: {most_common_activity[0]} ({most_common_activity[1]} times)")

    if moods:
        most_common_mood = Counter(moods).most_common(1)[0]
        print(f"Most common mood: {most_common_mood[0]} ({most_common_mood[1]} times)")


# --- main program ---
add_activity()
show_logs()
summarize()
