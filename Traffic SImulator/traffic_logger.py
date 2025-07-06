import csv
from config import CSV_FILENAME, SUMMARY_CSV_FILENAME

# Initialize CSV file
with open(CSV_FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Step", "UTC Time", "Traffic Light", "Phase", "North", "South", "East", "West", "Exited Vehicles"])


def log_traffic_data(step, utc_time, phase, lane_counts, exited_vehicles):
    """Logs traffic data to CSV with UTC timestamps."""
    north_count = lane_counts.get("-E1_0", 0)
    south_count = lane_counts.get("-E2_0", 0)
    east_count = lane_counts.get("E0.48_0", 0)
    west_count = lane_counts.get("E0_0", 0)

    with open(CSV_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"{step:.1f}", utc_time, "CJ_TL", phase, north_count, south_count, east_count, west_count, exited_vehicles])


def summarize_phases():
    """Summarizes phase duration data from CSV."""
    with open(CSV_FILENAME, mode="r") as infile, open(SUMMARY_CSV_FILENAME, mode="w", newline="") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        # Writing header
        writer.writerow(["Start Time", "End Time", "Phase Duration", "Traffic Light", "Phase", "North", "South", "East", "West", "Exited Vehicles"])

        prev_phase = None
        start_time = None
        phase_duration = 0

        for row in reader:
            current_time = row["UTC Time"]
            current_phase = row["Phase"]

            if current_phase == prev_phase:
                phase_duration += 0.1  # Since each step is 0.1s
            else:
                if prev_phase is not None:
                    writer.writerow([
                        start_time,
                        current_time,
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
                phase_duration = 0.1  # Start counting new phase duration

            prev_phase = current_phase

        # Write the last recorded phase
        if prev_phase is not None:
            writer.writerow([
                start_time,
                current_time,
                round(phase_duration, 1),
                row["Traffic Light"],
                prev_phase,
                row["North"],
                row["South"],
                row["East"],
                row["West"],
                row["Exited Vehicles"]
            ])

    print(f"Summarized traffic data saved to {SUMMARY_CSV_FILENAME}")
