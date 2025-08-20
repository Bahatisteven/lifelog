import csv 

# activity details 
activity = input("Enter activity name: ")
duration = input("Enter duration in hours: ")
mood = input("Enter your mood: ")
date = input("Enter date (YYYY-MM-DD): ")

with open('lifelog.csv', mode='a', newline='') as file:
  writer = csv.writer(file)
  writer.writerow([ date, activity, duration, mood ])

  print('Activity saved successfully!')

# read and display all entries
print("\nYour LifeLog Entries:")
with open('lifelog.csv', mode='r') as file:
  reader = csv.reader(file)
  for row in reader:
    print(row)
    

# summaries
total_hours = 0
with open('lifelog.csv', mode='r') as file:
  reader = csv.reader(file)
  for row in reader:
    try:
      hours = float(row[2])
      total_hours += hours

    except:
      pass   # ignore if it's not a number (header or bad row)

print(f"\n Total hours logged: {total_hours}")