import airsim
import time
import traceback

def start_swarm_simulation():
    try:
        client = airsim.MultirotorClient()
        client.confirmConnection()
        print("Connected to AirSim")

        # List of drone names (3 drones)
        drones = ["Drone1", "Drone2", "Drone3"]

        # Enable API control and take off for each drone
        for drone in drones:
            try:
                client.enableApiControl(True, drone)
                client.armDisarm(True, drone)
                client.takeoffAsync(vehicle_name=drone).join()
                print(f"{drone} has taken off")
            except Exception as e:
                print(f"Error with {drone} takeoff: {str(e)}")
                traceback.print_exc()

        # Move drones to initial positions
        for i, drone in enumerate(drones):
            try:
                client.moveToPositionAsync(i * 5, 0, -10, 2, vehicle_name=drone).join()
                print(f"{drone} moved to position ({i * 5}, 0, -10)")
            except Exception as e:
                print(f"Error moving {drone}: {str(e)}")
                traceback.print_exc()

        time.sleep(2)  # Wait to observe
        print("Swarm simulation running")
    except Exception as e:
        print(f"Simulation error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    start_swarm_simulation()