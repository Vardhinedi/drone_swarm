import airsim
import cv2
import numpy as np
from ultralytics import YOLO
import time
import os
import traceback

def detect_threats():
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

        # Load YOLOv8 model
        model = YOLO("yolov8n.pt")  # Pre-trained model
        print("YOLOv8 model loaded")

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
            img_rgb = img1d.reshape(response.height, response.width, 3)
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

            # Run YOLOv8 detection
            results = model(img_bgr)
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy()
                for box, conf, cls in zip(boxes, confidences, classes):
                    if conf > 0.5:  # Confidence threshold
                        print(f"Detected: Class {result.names[int(cls)]}, Confidence {conf:.2f}, Box {box}")

            # Save image with detections
            os.makedirs("data", exist_ok=True)
            annotated_img = results[0].plot()
            cv2.imwrite("data/detected_image.jpg", annotated_img)
            print("Saved detection image to data/detected_image.jpg")
        else:
            print("No image data received from Drone1. Check AirSim camera settings.")

    except Exception as e:
        print(f"Detection error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    detect_threats()