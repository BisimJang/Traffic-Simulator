import traci
import logging
from config import MIN_GREEN_TIME, THRESHOLD

# Setup logging
logging.basicConfig(level=logging.INFO)

time_since_last_switch = {}


def manage_traffic_lights(traffic_light_id):
    """Traffic light management with improved phase control."""
    if traffic_light_id not in time_since_last_switch:
        time_since_last_switch[traffic_light_id] = 0

    current_phase = traci.trafficlight.getPhase(traffic_light_id)
    lanes = traci.trafficlight.getControlledLanes(traffic_light_id)
    waiting_vehicles = {lane: traci.lane.getLastStepVehicleNumber(lane) for lane in lanes}
    max_waiting = max(waiting_vehicles.values(), default=0)

    if time_since_last_switch[traffic_light_id] < MIN_GREEN_TIME:
        time_since_last_switch[traffic_light_id] += 1
        return

    if max_waiting > THRESHOLD:
        new_duration = MIN_GREEN_TIME + (max_waiting // 2)
        traci.trafficlight.setPhaseDuration(traffic_light_id, new_duration)
        logging.info(f"Extended green time at {traffic_light_id} (max waiting: {max_waiting})")

    total_phases = len(traci.trafficlight.getAllProgramLogics(traffic_light_id)[0].phases)
    next_phase = (current_phase + 1) % total_phases
    traci.trafficlight.setPhase(traffic_light_id, next_phase)
    logging.info(f"Traffic light {traffic_light_id} changed to phase {next_phase}")

    time_since_last_switch[traffic_light_id] = 0
