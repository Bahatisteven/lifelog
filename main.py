from lifelog.data_handler import init_file, add_activity, show_logs
from lifelog.analytics import summarize, weekly_summary, date_range_summary 
from lifelog.analytics import export_insights, load_and_clean_data
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
        print("8. Quit")

        choice = input("Choose an option (1-8): ")

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
            df = load_and_clean_data()
            export_insights(df)
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()
