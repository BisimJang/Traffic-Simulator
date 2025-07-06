import traci
import random
import logging
import csv
from datetime import datetime
import pytz
from config import SUMO_CONFIG, ROUTES
from traffic_light_manager import manage_traffic_lights
from traffic_logger import log_traffic_data
import subprocess


print("Running SUMO simulation...")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Global Variables
vehicle_count = 0
stuck_vehicles = {}


def start_sumo():
    """Starts the SUMO simulation."""
    traci.start(SUMO_CONFIG)


def flow_sensor():
    """Tracks the number of vehicles entering each lane."""
    return {lane: traci.lane.getLastStepVehicleNumber(lane) for lane in traci.lane.getIDList()}


def spawn_vehicles():
    """Spawn vehicles based on detected flow per lane."""
    global vehicle_count
    lane_flow = flow_sensor()

    for from_edge, to_edge in ROUTES:
        num_vehicles = lane_flow.get(from_edge, random.randint(5, 20))

        for _ in range(num_vehicles):
            vehicle_id = f"veh{vehicle_count}"
            route_id = f"route_{vehicle_count}"
            depart_time = random.uniform(0, 100)

            if from_edge in traci.edge.getIDList() and to_edge in traci.edge.getIDList():
                traci.route.add(routeID=route_id, edges=[from_edge, to_edge])
                traci.vehicle.add(vehID=vehicle_id, routeID=route_id, typeID="car", depart=depart_time)
                stuck_vehicles[vehicle_id] = 0
                vehicle_count += 1
            else:
                logging.warning(f"Invalid route: {from_edge} -> {to_edge}")


def monitor_vehicles():
    """Monitors vehicle movement and logs data with UTC timestamp."""
    real_time = traci.simulation.getTime()
    step = round(real_time, 1)

    # Get UTC timestamp
    utc_now = datetime.now(pytz.utc).strftime("%H:%M:%S")

    phase = traci.trafficlight.getPhase("CJ_TL")
    lane_counts = flow_sensor()
    exited_vehicles = traci.simulation.getArrivedNumber()

    log_traffic_data(step, utc_now, phase, lane_counts, exited_vehicles)


def run_simulation():
    """Runs the SUMO simulation."""
    spawn_vehicles()

    while traci.simulation.getMinExpectedNumber() > 0:
        print(flow_sensor())
        traci.simulationStep()

        for tl_id in traci.trafficlight.getIDList():
            manage_traffic_lights(tl_id)

        monitor_vehicles()

    traci.close()


if __name__ == "__main__":
    start_sumo()
    run_simulation()

print("Simulation complete. Running summarize traffic.py...")
subprocess.run(["python", "summarize traffic.py"])
print("Summarization complete. Dash app should update.")
