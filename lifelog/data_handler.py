import csv
import os
from datetime import datetime
from typing import Optional  

# paths
DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "lifelog.csv")
CLEANED_FILE = os.path.join(DATA_DIR, "lifelog_cleaned.csv")

# CSV header definition 
CSV_HEADER = ["date", "activity", "duration", "mood", "tags", "notes"]


def init_file(file_path: str = FILE_PATH) -> None:
    """create CSV with header if it doesn't exist."""
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
    # check for empty activity name
    if not activity:
        print("Activity name cannot be empty.")
        return

    duration = input("Enter duration in hours: ")
    try:
        duration_float = float(duration)  # validate duration
        # check for negative duration values
        if duration_float < 0:
            print("Duration cannot be negative.")
            return
    except ValueError:
        print("Invalid duration. Please enter a number.")
        return

    mood = input("Enter your mood: ").strip().capitalize()
    tags = input("Enter tags (comma-separated, e.g. Health, Workout): ").strip()
    notes = input("Enter any notes (optional): ").strip()

    # error handling for file operations
    try:
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date_str, activity, duration, mood, tags, notes])
        print("Activity saved successfully!\n")
    except (IOError, PermissionError) as e:
        print(f"Error saving activity: {e}")

def show_logs(file_path: str = FILE_PATH) -> None: 
    """display all saved activities with formatting"""
    # error handling for file operations
    try:
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
    except (IOError, PermissionError) as e:
        print(f"Error reading file: {e}")
    except Exception as e:
        print(f"Unexpected error displaying logs: {e}")

def filter_by_tag(file_path: str = FILE_PATH) -> None:  
    """show activities filtered by a tag"""
    tag = input("Enter a tag to filter by: ").strip().lower()
    # check for empty tag input
    if not tag:
        print("Tag cannot be empty.")
        return

    # error handling for file operations
    try:
        if not os.path.exists(file_path):
            print("No logs found. Add an activity first!")
            return

        print(f"\nActivities with tag '{tag}':")
        found_any = False  # track if any entries are found
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tags = [t.strip().lower() for t in row["tags"].split(",")] if row["tags"] else []
                if tag in tags:
                    print(f"- {row['date']} | {row['activity']} ({row['duration']}hrs)")
                    found_any = True

        # inform user if no matches found
        if not found_any:
            print(f"No activities found with tag '{tag}'.")

    except (IOError, PermissionError) as e:
        print(f"Error reading file: {e}")
    except Exception as e:
        print(f"Unexpected error filtering by tag: {e}")


def search_notes(file_path: str = FILE_PATH) -> None:  
    """search notes for a keyword"""
    keyword = input("Enter keyword to search in notes: ").strip().lower()
    # check for empty keyword input
    if not keyword:
        print("Keyword cannot be empty.")
        return

    # error handling for file operations
    try:
        if not os.path.exists(file_path):
            print("No logs found. Add an activity first!")
            return

        print(f"\nActivities with notes containing '{keyword}':")
        found_any = False  # track if any entries are found
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if keyword in (row["notes"] or "").lower():
                    print(f"- {row['date']} | {row['activity']} ({row['duration']}hrs)\n {row['notes']}")
                    found_any = True

        # inform user if no matches found
        if not found_any:
            print(f"No notes found containing '{keyword}'.")

    except (IOError, PermissionError) as e:
        print(f"Error reading file: {e}")
    except Exception as e:
        print(f"Unexpected error searching notes: {e}")
