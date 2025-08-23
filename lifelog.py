import csv
from collections import Counter
import os


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

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, activity, duration, mood])

    print("Activity saved successfully!\n")


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


def main():
    init_file()

    while True:
        print("\n=== LifeLog Menu ===")
        print("1. Add new activity")
        print("2. Show all logs")
        print("3. Show summary")
        print("4. Quit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            add_activity()
        elif choice == "2":
            show_logs()
        elif choice == "3":
            summarize()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
