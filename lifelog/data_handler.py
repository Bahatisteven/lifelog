import csv
import os

FILE_PATH = os.path.join("data", "lifelog.csv")

def init_file(file_path=FILE_PATH):
    """Create CSV with header if it doesn't exist"""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "activity", "duration", "mood", "tags", "notes"])

def add_activity(file_path=FILE_PATH):
    """ask user details and save activity into CSV"""
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

def show_logs(file_path=FILE_PATH):
    """display all saved activities"""
    print("\nYour LifeLog Entries:")
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)





