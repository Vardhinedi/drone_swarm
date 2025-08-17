import airsim
import time

def start_swarm_simulation():
    client = airsim.MultirotorClient()
    client.confirmConnection()
    
    # List of drone names
    drones = ["Drone1", "Drone2", "Drone3", "Drone4", "Drone5"]
    
    # Enable API control and take off for each drone
    for drone in drones:
        client.enableApiControl(True, drone)
        client.armDisarm(True, drone)
        client.takeoffAsync(vehicle_name=drone).join()
        print(f"{drone} has taken off")
    
    # Move drones to initial positions
    for i, drone in enumerate(drones):
        client.moveToPositionAsync(i * 5, 0, -10, 5, vehicle_name=drone).join()
        print(f"{drone} moved to position ({i * 5}, 0, -10)")
    
    time.sleep(2)  # Wait to observe
    print("Swarm simulation running")

if __name__ == "__main__":
    start_swarm_simulation()