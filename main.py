from ics import Calendar, Event
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def parse_exam_schedule(file_path):
    events = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Skip header lines until we find the data table
    start_processing = False
    for line in lines:
        if line.startswith("Học kỳ\tMôn học"):  # Header row
            start_processing = True
            continue
        if start_processing and line.strip() and not line.startswith("Trình bày từ dòng"):
            # Split tab-separated values
            cols = line.strip().split('\t')
            if len(cols) < 11:
                continue  # Skip incomplete rows
            
            try:
                # Extract fields
                subject_code, subject_name = cols[1].split(' - ', 1)
                group = cols[2]
                exam_date = cols[3]
                exam_type = cols[4]
                location = f"{cols[5]} {cols[6]}"
                start_time_raw = cols[8]
                duration = int(cols[9])

                # Clean start time
                start_time = start_time_raw.replace('g', ':')
                local_tz = ZoneInfo("Asia/Ho_Chi_Minh") 
                
                start_dt = datetime.strptime(f"{exam_date} {start_time}", "%Y-%m-%d %H:%M").replace(tzinfo=local_tz)
                end_dt = start_dt + timedelta(minutes=duration)

                # Create event
                event = Event()
                event.name = f"{exam_type}: {subject_name} ({group})"
                event.begin = start_dt
                event.end = end_dt
                event.location = location
                event.description = (
                    f"Subject: {subject_name} ({subject_code})\n"
                    f"Type: {exam_type}\n"
                    f"Group: {group}\n"
                    f"Location: {location}\n"
                    f"Duration: {duration} minutes"
                )
                events.append(event)
            except Exception as e:
                print(f"Skipping row due to error: {e}\nRow: {cols}")
    
    return events

def create_ics_file(events, output_file="exam_schedule.ics"):
    cal = Calendar()
    for event in events:  # ✅ Correct usage
        cal.events.add(event)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cal.serialize_iter())

    print(f"✅ ICS file created: {output_file}")

def main():
    file_path = "exam_schedule.txt"  # Make sure this file contains the tab-separated rows
    events = parse_exam_schedule(file_path)
    if events:
        create_ics_file(events)
    else:
        print("⚠️ No valid exam events found.")

if __name__ == "__main__":
    main()
