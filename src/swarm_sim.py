import airsim
import time

# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()

# Enable API control and take off
client.enableApiControl(True, "SimpleFlight")
client.armDisarm(True, "SimpleFlight")
client.takeoffAsync("SimpleFlight").join()

print("Drone1 has taken off")
time.sleep(5)  # Wait to observe