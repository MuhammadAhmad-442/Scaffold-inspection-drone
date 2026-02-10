from ultralytics import YOLO
import cv2
import math
# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# model
model = YOLO("scaffold_1.pt")

# object classes
classNames = ["Guardrail","Suspension_scaffold"]

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    suspension_scaffold_coords = None
    guardrail_coords = None

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # class name
            cls = int(box.cls[0])
            class_name = classNames[cls]

            # Check if it's Suspension_scaffold
            if class_name == "Suspension_scaffold":
                suspension_scaffold_coords = (x1, y1, x2, y2)
            elif class_name == "Guardrail":
                guardrail_coords = (x1, y1, x2, y2)

            # Draw bounding box and write class name
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(img, class_name, org, font, fontScale, color, thickness)

    # Check if Suspension_scaffold and Guardrail are both detected
    if suspension_scaffold_coords and guardrail_coords:
        # Calculate areas of the bounding boxes
        ss_area = (suspension_scaffold_coords[2] - suspension_scaffold_coords[0]) * (suspension_scaffold_coords[3] - suspension_scaffold_coords[1])
        gr_area = (guardrail_coords[2] - guardrail_coords[0]) * (guardrail_coords[3] - guardrail_coords[1])

        # Compare the areas
        if ss_area > gr_area:
            print("Safe")
        else:
            print("Guardrail is Fake")

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()