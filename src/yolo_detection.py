import airsim
import cv2
import numpy as np
import time
import traceback
import os

def test_camera_capture():
    try:
        # Connect to AirSim
        client = airsim.MultirotorClient()
        client.confirmConnection()
        print("Connected to AirSim")

        # Ensure Drone1 is active
        client.enableApiControl(True, "Drone1")
        client.armDisarm(True, "Drone1")
        client.takeoffAsync(vehicle_name="Drone1").join()
        print("Drone1 has taken off")

        # Move Drone1 to a position
        client.moveToPositionAsync(0, 0, -10, 2, vehicle_name="Drone1").join()
        print("Drone1 moved to position (0, 0, -10)")

        # Capture image from Drone1's camera
        time.sleep(2)  # Wait for stability
        responses = client.simGetImages(
            [airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)],
            vehicle_name="Drone1"
        )

        print(f"Image responses: {len(responses)}")

        if responses and responses[0].image_data_uint8:
            response = responses[0]
            print(f"Image data length: {len(response.image_data_uint8)}")

            # Convert raw bytes to numpy array
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)

            # Reshape to 3D array (H x W x 3)
            img_rgb = img1d.reshape(response.height, response.width, 3)

            # Convert RGB → BGR for OpenCV
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

            # Ensure output folder exists
            os.makedirs("data", exist_ok=True)

            # Save decoded image
            cv2.imwrite("data/raw_image.jpg", img_bgr)
            print("Saved decoded image to data/raw_image.jpg")

        else:
            print("No image data received from Drone1. Check AirSim camera settings.")

    except Exception as e:
        print(f"Camera capture error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_camera_capture()
