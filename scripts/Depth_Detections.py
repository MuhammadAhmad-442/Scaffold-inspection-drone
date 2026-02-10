import cv2
import numpy as np
from ultralytics import YOLO
import pyrealsense2 as rs
import math

# Initialize the YOLO model
model = YOLO("scaffold_1.pt")

# Configure the pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
profile = pipeline.start(config)
classNames = ["Guardrail","Suspension_scaffold"]
try:
    while True:
        # Wait for a frame
        frames = pipeline.wait_for_frames()

        # Get the color frame
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Convert the frame to a numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Perform object detection
        results = model.predict(color_image)

        # Draw bounding boxes and labels
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                # put box in cam
                cv2.rectangle(color_image, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)

                # class name
                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (0, 0, 0)
                thickness = 1

                cv2.putText(color_image, classNames[cls], org, font, fontScale, color, thickness)

        # Display the frame
        cv2.imshow("Object Detection", color_image)

        # Exit if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the pipeline
    pipeline.stop()

# Release the camera and destroy all windows
cv2.destroyAllWindows()