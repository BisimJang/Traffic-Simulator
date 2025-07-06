import csv
from datetime import datetime

input_csv = "traffic_data.csv"
output_csv = "summarized_traffic_data.csv"

def summarize_phases(input_file, output_file):
    with open(input_file, mode="r") as infile, open(output_file, mode="w", newline="") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        writer.writerow(
            ["Start Time", "End Time", "Phase Duration", "Traffic Light", "Phase", "North", "South", "East", "West", "Exited Vehicles"]
        )

        prev_phase = None
        start_time = None
        phase_duration = 0

        for row in reader:
            # Parse time safely
            try:
                current_time = datetime.strptime(row["UTC Time"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    current_time = datetime.strptime(row["UTC Time"], "%H:%M:%S")
                except ValueError:
                    print(f"Skipping row with invalid time format: {row['UTC Time']}")
                    continue  # Skip invalid rows

            current_phase = row["Phase"]

            if current_phase == prev_phase:
                phase_duration += 0.1  # Since each step is 0.1s
            else:
                if prev_phase and start_time:
                    writer.writerow([
                        start_time.strftime("%H:%M:%S"),
                        current_time.strftime("%H:%M:%S"),
                        round(phase_duration, 1),
                        row["Traffic Light"],
                        prev_phase,
                        row["North"],
                        row["South"],
                        row["East"],
                        row["West"],
                        row["Exited Vehicles"]
                    ])

                start_time = current_time
                phase_duration = 0.1

            prev_phase = current_phase

        # Write the last phase if it exists
        if prev_phase and start_time:
            writer.writerow([
                start_time.strftime("%H:%M:%S"),
                current_time.strftime("%H:%M:%S"),
                round(phase_duration, 1),
                row["Traffic Light"],
                prev_phase,
                row["North"],
                row["South"],
                row["East"],
                row["West"],
                row["Exited Vehicles"]
            ])

    print(f"Summarized traffic data saved to {output_file}")

# Run the summarization
summarize_phases(input_csv, output_csv)
