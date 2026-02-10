# Configuration file for Scaffold Inspection Drone
# Copy this to config.py and modify for your setup

# Camera Configuration
CAMERA_CONFIG = {
    'width': 640,
    'height': 480,
    'fps': 30,
    'color_format': 'rgb8',  # or 'bgr8'
    'depth_format': 'z16'
}

# YOLO Model Configuration
MODEL_CONFIG = {
    'model_path': 'models/scaffold_1.pt',
    'confidence_threshold': 0.5,
    'iou_threshold': 0.45,
    'device': 'cuda',  # 'cuda', 'cpu', or 'mps' (for Mac)
    'half_precision': False,  # FP16 for faster inference on supported GPUs
}

# Detection Classes
CLASS_NAMES = [
    "Guardrail",
    "Suspension_scaffold"
]

# Safety Logic Configuration
SAFETY_CONFIG = {
    'area_ratio_threshold': 1.0,  # scaffold_area / guardrail_area
    'min_detection_confidence': 0.6,
    'enable_depth_check': True,
    'max_detection_distance': 10.0,  # meters
}

# Drone Connection Configuration
DRONE_CONFIG = {
    'connection_string': 'tcp:127.0.0.1:5760',  # SITL simulation
    # 'connection_string': '/dev/ttyACM0',  # Physical drone (Linux)
    # 'connection_string': 'COM3',  # Physical drone (Windows)
    'baud_rate': 57600,
    'timeout': 30,
    'flight_altitude': 2.0,  # meters
    'movement_speed': 0.5,  # m/s
}

# Flight Parameters
FLIGHT_CONFIG = {
    'takeoff_altitude': 2.0,  # meters
    'inspection_altitude': 3.0,  # meters
    'horizontal_speed': 0.5,  # m/s
    'vertical_speed': 0.3,  # m/s
    'waypoint_radius': 1.0,  # meters
}

# Visualization Configuration
VISUALIZATION_CONFIG = {
    'show_rgb': True,
    'show_depth': True,
    'show_bounding_boxes': True,
    'show_class_names': True,
    'show_confidence': True,
    'show_coordinates': True,
    'box_color': (255, 0, 255),  # BGR format
    'text_color': (255, 0, 0),  # BGR format
    'box_thickness': 3,
    'text_thickness': 2,
    'font_scale': 1.0,
}

# Logging Configuration
LOGGING_CONFIG = {
    'enable_logging': True,
    'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'log_file': 'logs/drone_inspection.log',
    'log_detections': True,
    'save_images': False,
    'image_save_path': 'logs/images/',
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'use_tensorrt': False,  # Requires TensorRT installation
    'max_batch_size': 1,
    'num_threads': 4,
    'prefetch_frames': 2,
}

# Alert Configuration
ALERT_CONFIG = {
    'enable_audio_alerts': False,
    'enable_visual_alerts': True,
    'alert_on_fake_guardrail': True,
    'alert_on_no_detection': False,
}
