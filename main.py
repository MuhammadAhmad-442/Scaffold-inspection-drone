from ultralytics import YOLO
import cv2
import numpy as np
import pyrealsense2 as rs
import copy
import math

# Initialize the Intel RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)  # Enable RGB stream
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)   # Enable Depth Stream

pipeline.start(config)
profile = pipeline.get_active_profile()
align_to = rs.stream.color
align = rs.align(align_to)

# model
model = YOLO('yolov8n.pt')
model = YOLO("scaffold_1.pt")

# object classes
classNames = ["Guardrail", "Suspension_scaffold"]

while True:
    # Get frames from the RealSense camera
    frames = pipeline.wait_for_frames()

    #color_frame = frames.get_color_frame()
    #depth_frame = frames.get_depth_frame()
    aligned_frames = align.process(frames)

    # Retrieve aligned color and depth frames
    aligned_color_frame = aligned_frames.get_color_frame()
    aligned_depth_frame = aligned_frames.get_depth_frame()

    if not aligned_color_frame or not aligned_depth_frame:
        continue
    color_image = np.asanyarray(aligned_color_frame.get_data()) # Convert the color frame to a numpy array
    depth_image = np.asanyarray(aligned_depth_frame.get_data()) # Convert the depth frame to a numpy array

    # Detect objects in the frame
    results = model(color_image, stream=True)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    suspension_scaffold_coords = None
    guardrail_coords = None

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

            # class name
            cls = int(box.cls[0])
            class_name = classNames[cls]

            # Check if it's Suspension_scaffold
            if class_name == "Suspension_scaffold":
                suspension_scaffold_coords = (x1, y1, x2, y2)
            elif class_name == "Guardrail":
                guardrail_coords = (x1, y1, x2, y2)

            # Draw bounding box and write class name and coordinates
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.rectangle(color_image, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(color_image, class_name, org, font, fontScale, color, thickness)
            cv2.putText(color_image, f"({x1}, {y1}) ({x2}, {y2})", (x1, y1 - 10), font, 0.5, color, thickness)

            #Draw bounding boxes for depth camera
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.rectangle(depth_colormap, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(depth_colormap, class_name, org, font, fontScale, color, thickness)
            cv2.putText(depth_colormap, f"({x1}, {y1}) ({x2}, {y2})", (x1, y1 - 10), font, 0.5, color, thickness)

    # Check if Suspension_scaffold and Guardrail are both detected
    if suspension_scaffold_coords and guardrail_coords:
        # Calculate areas of the bounding boxes
        ss_area = (suspension_scaffold_coords[2] - suspension_scaffold_coords[0]) * (
                    suspension_scaffold_coords[3] - suspension_scaffold_coords[1])
        gr_area = (guardrail_coords[2] - guardrail_coords[0]) * (guardrail_coords[3] - guardrail_coords[1])

        # Compare the areas
        if ss_area > gr_area:
            print("Safe")
        else:
            print("Guardrail Misclassification")

        # Print guardrail coordinates
        print("Guardrail Coordinates:", guardrail_coords)

    # Display the RGB frame with bounding boxes, class names, and coordinates
    cv2.imshow("Webcam", color_image)
    cv2.imshow("Webcam2", depth_colormap)

    key = cv2.waitKey(1)
    if key == 27:  # Press ESC to exit
        break

# Clean up
pipeline.stop()
cv2.destroyAllWindows()
