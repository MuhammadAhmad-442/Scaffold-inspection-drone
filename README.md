# Scaffold Inspection Drone (Test Files)
- Test Files include Software in the Loop check
- Depth Camera check
- Detection with depth check

## 🎯 Project Overview

This project combines a Jetson Nano, Intel RealSense depth cameras, and YOLOv8 object detection to automate scaffold safety inspections. The system can:

- Detect suspension scaffolds and guardrails in real-time
- Verify guardrail by checking midrail presence
- Provide depth information for the guardrail

https://github.com/user-attachments/assets/ff68ee72-9c8f-45f5-b728-6ec91cd5a969

## 🔧 Hardware

- **Drone**: Compatible with MAVLink protocol (tested with PX4)
- **Camera**: Intel RealSense Depth Camera (D435)
- **Computing**: Onboard computer (Jetson Nano)
- **Optional**: Ground control station for monitoring

## 📋 Software Requirements

- Python 3.8+ (3.6 for Jetson Nano)
- CUDA-capable GPU (recommended for faster inference)
- See `requirements.txt` for full dependency list

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/scaffold-inspection-drone.git
cd scaffold-inspection-drone
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download or Train YOLO Model
Place your trained `scaffold_1.pt` model in the `models/` directory.

**Model Classes:**
- Class 0: Guardrail
- Class 1: Suspension_scaffold

## 📁 Project Structure

```
scaffold-inspection-drone/
├── main.py                    # Main detection script (RealSense + YOLO)
├── scripts/
│   ├── drone.py              # Drone flight control simulation
│   ├── Guardrail.py          # Webcam-based detection
│   └── Depth_Detections.py   # RealSense detection (color only)
├── models/
│   └── scaffold_1.pt         # Trained YOLO model (not included)
├── docs/
│   └── SETUP.md             # Detailed setup guide
├── requirements.txt
├── .gitignore
└── README.md
```

## 🎮 Usage

### Real-Time Detection with Depth Camera
```bash
python main.py
```
This runs the full system with:
- RGB and depth stream visualization
- Real-time object detection
- Safety classification logic
- Press `ESC` to exit

### Webcam Testing (No Depth)
```bash
python scripts/Guardrail.py
```
Use this for testing without RealSense hardware.

### Drone Simulation
```bash
python scripts/drone.py
```
Simulates basic drone movements (requires SITL setup).

## 🧠 Detection Logic

The system uses area-based comparison to verify guardrail authenticity:

```
if suspension_scaffold_area > guardrail_area:
    → "Safe" (Guardrail is properly visible)
else:
    → "Guardrail Misclassification" (Potential fake/hidden guardrail)
```

**Reasoning**: A legitimate guardrail should appear smaller than the scaffold it's protecting when viewed from the drone's perspective.

## 🔑 Key Features

- **Real-time Detection**: YOLOv8-based object detection at 30 FPS
- **Depth Integration**: Uses aligned RGB-D frames from Intel RealSense
- **Safety Validation**: Automated guardrail authenticity checking
- **Dual Visualization**: Side-by-side RGB and depth colormap views
- **Autonomous Flight**: DroneKit integration for waypoint navigation

## 📊 Performance

- Detection Speed: ~30 FPS (on GPU)
- Detection Range: Up to 10 meters (depth camera dependent)
- Accuracy: Depends on trained model quality

## 🛠️ Configuration

### Camera Settings
Edit in `main.py`:
```python
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
```

### Model Selection
Switch YOLO models:
```python
model = YOLO("yolov8n.pt")  # Pre-trained
model = YOLO("scaffold_1.pt")  # Custom trained
```

## 🐛 Troubleshooting

**Camera not detected:**
```bash
rs-enumerate-devices
```

**CUDA errors:**
Install CUDA-compatible PyTorch version:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**Drone connection issues:**
Check connection string in `drone.py`:
```python
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ultralytics YOLOv8** for object detection framework
- **Intel RealSense** for depth sensing technology
- **DroneKit** for drone control capabilities

## 📧 Contact

For questions or collaboration opportunities, please open an issue on GitHub.

---

**⚠️ Safety Notice**: This system is for research and development purposes. Always follow local regulations and safety protocols when operating drones.
