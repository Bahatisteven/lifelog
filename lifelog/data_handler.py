import csv
import os
from datetime import datetime

# paths
DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "lifelog.csv")
CLEANED_FILE = os.path.join(DATA_DIR, "lifelog_cleaned.csv")

# CSV header definition 
CSV_HEADER = ["date", "activity", "duration", "mood", "tags", "notes"]


def init_file(file_path: str = FILE_PATH) -> None:
    """Create CSV with header if it doesn't exist."""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)
        print(f"Created new lifelog file at: {file_path}")


def add_activity(file_path: str = FILE_PATH) -> None:
    """ask user details and save activity into CSV."""
    # input with validation
    date_str = input("Enter date (YYYY-MM-DD): ")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")  # validate date
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    activity = input("Enter activity name: ").strip().title()
    duration = input("Enter duration in hours: ")
    try:
        float(duration)  # validate duration
    except ValueError:
        print("Invalid duration. Please enter a number.")
        return

    mood = input("Enter your mood: ").strip().capitalize()
    tags = input("Enter tags (comma-separated, e.g. Health, Workout): ").strip()
    notes = input("Enter any notes (optional): ").strip()

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date_str, activity, duration, mood, tags, notes])

    print("Activity saved successfully!\n")

def show_logs(file_path=FILE_PATH):
    """display all saved activities with formatting"""

    if not os.path.exists(file_path):
        print("No logs found. Add an activity first!")
        return
    print("\nYour LifeLog Entries:")
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(
                f"- {row['date']} | {row['activity']} "
                f"({row['duration']}hrs, Mood: {row['mood']})\n"
                f"Tags: {row['tags']} | Notes: {row['notes']}\n"
            )

def filter_by_tag(file_path=FILE_PATH):
    """show activities filtered by a tag"""
    tag = input("Enter a tag to filter by: ").strip().lower()
    print(f"\nActivities with tag '{tag}':")
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tags = [t.strip().lower() for t in row["tags"].split(",")] if row["tags"] else []
            if tag in tags:
                print(f"- {row['date']} | {row['activity']} ({row['duration']}hrs)")


def search_notes(file_path=FILE_PATH):
    """search notes for a keyword"""
    keyword = input("Enter keyword to search in notes: ").strip().lower()
    print(f"\nActivities with notes containing '{keyword}':")
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if keyword in (row["notes"] or "").lower():
                print(f"- {row['date']} | {row['activity']} ({row['duration']}hrs)\n {row['notes']}")
