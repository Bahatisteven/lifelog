from lifelog.data_handler import init_file, add_activity, show_logs, search_notes, filter_by_tag
from lifelog.analytics import summarize, weekly_summary, date_range_summary 
from lifelog.analytics import export_summary_report, load_and_clean_data
from lifelog.visualization import pandas_analysis

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
        print("7. Export insights")
        print("8. Filter by tag")
        print("9. Search in notes")
        print("10. Quit")

        choice = input("Choose an option (1-8): ").strip()

        menu_options = {
            "1": add_activity,
            "2": show_logs,
            "3": summarize,
            "4": weekly_summary,
            "5": date_range_summary,
            "6": pandas_analysis,
            "7": export_summary_report,
            "8": filter_by_tag,
            "9": search_notes, 
            "10": lambda: export_summary_report(load_and_clean_data())

        }

        if choice in menu_options:
            menu_options[choice]()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
