import os
import sys

# Ensure SUMO_HOME is set
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# Define SUMO configuration
SUMO_CONFIG = [
    'sumo-gui',  # Use 'sumo' for non-GUI mode
    '-c', 'sumo_config/simple_intersection.sumocfg',
    '--step-length', '0.1',
    '--lateral-resolution', '0.1'
]

# Simulation parameters
MIN_GREEN_TIME = 10  # Minimum time before switching phases
THRESHOLD = 5  # Vehicle threshold for extending phase

# CSV Filenames
CSV_FILENAME = "traffic_data.csv"
SUMMARY_CSV_FILENAME = "summarized_traffic_data.csv"

# Define routes
ROUTES = [
    ("-E1", "E2"),
    ("-E2", "E1"),
    ("E0.48", "-E0"),
    ("E0", "-E0.48"),
    ("E0.48", "E1"),
    ("E0", "E2"),
    ("-E1", "-E0.48"),
    ("-E2", "-E0"),
]
