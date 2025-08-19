import airsim
import time
import numpy as np
import traceback

def get_drone_position(client, drone):
    state = client.getMultirotorState(vehicle_name=drone)
    return np.array([state.kinematics_estimated.position.x_val,
                     state.kinematics_estimated.position.y_val,
                     state.kinematics_estimated.position.z_val])

def boid_flocking(client, drones):
    positions = [get_drone_position(client, drone) for drone in drones]
    velocities = []
    
    for i, drone in enumerate(drones):
        pos = positions[i]
        # Cohesion: Move toward average position
        avg_pos = np.mean(positions, axis=0)
        cohesion = (avg_pos - pos) * 0.1
        
        # Separation: Avoid crowding
        separation = np.zeros(3)
        for j, other_pos in enumerate(positions):
            if i != j and np.linalg.norm(pos - other_pos) < 5:
                separation -= (other_pos - pos) * 0.2
        
        # Alignment: Match average velocity (simplified as zero for now)
        alignment = np.zeros(3)
        
        # Combine rules
        velocity = cohesion + separation + alignment
        velocities.append(velocity)
    
    return velocities

def start_swarm_simulation():
    try:
        client = airsim.MultirotorClient()
        client.confirmConnection()
        print("Connected to AirSim")

        # List of drone names
        drones = ["Drone1", "Drone2", "Drone3"]

        # Enable API control and take off
        for drone in drones:
            try:
                client.enableApiControl(True, drone)
                client.armDisarm(True, drone)
                client.takeoffAsync(vehicle_name=drone).join()
                print(f"{drone} has taken off")
            except Exception as e:
                print(f"Error with {drone} takeoff: {str(e)}")
                traceback.print_exc()

        # Move to initial positions
        for i, drone in enumerate(drones):
            try:
                client.moveToPositionAsync(i * 5, 0, -10, 2, vehicle_name=drone).join()
                print(f"{drone} moved to position ({i * 5}, 0, -10)")
            except Exception as e:
                print(f"Error moving {drone}: {str(e)}")
                traceback.print_exc()

        # Apply flocking for 10 seconds
        start_time = time.time()
        while time.time() - start_time < 10:
            velocities = boid_flocking(client, drones)
            for drone, velocity in zip(drones, velocities):
                try:
                    client.moveByVelocityAsync(velocity[0], velocity[1], velocity[2], 0.5, vehicle_name=drone)
                except Exception as e:
                    print(f"Error moving {drone}: {str(e)}")
            time.sleep(0.1)  # Update every 0.1 seconds

        print("Swarm simulation with flocking completed")
    except Exception as e:
        print(f"Simulation error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    start_swarm_simulation()