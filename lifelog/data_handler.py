import csv
import os

from LifeLog import lifelog

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
