# Detailed Setup Guide

This guide will walk you through setting up the Scaffold Inspection Drone project from scratch.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Hardware Setup](#hardware-setup)
3. [Software Installation](#software-installation)
4. [Model Training](#model-training)
5. [Testing](#testing)
6. [Deployment](#deployment)

## System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+ / Windows 10+ / macOS 11+
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space

### Recommended for Real-Time Performance
- **GPU**: NVIDIA GPU with CUDA support (GTX 1060 or better)
- **RAM**: 16GB+
- **CPU**: Quad-core processor

## Hardware Setup

### 1. Intel RealSense Camera Setup

#### Ubuntu/Linux
```bash
# Install RealSense SDK
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main"
sudo apt-get update
sudo apt-get install librealsense2-dkms librealsense2-utils librealsense2-dev

# Verify installation
realsense-viewer
```

#### Windows
1. Download [Intel RealSense SDK](https://www.intelrealsense.com/sdk-2/)
2. Install the executable
3. Run `Intel RealSense Viewer` to test camera

### 2. Drone Hardware Setup

For physical drone deployment:
1. Install ArduPilot or PX4 firmware on flight controller
2. Connect companion computer to flight controller via UART/USB
3. Configure MAVLink connection (typically `/dev/ttyUSB0` or `/dev/ttyACM0`)

For simulation:
```bash
# Install SITL (Software In The Loop)
pip install dronekit-sitl

# Test SITL
dronekit-sitl copter --home=-35.363261,149.165230,584,353
```

## Software Installation

### 1. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install CUDA (For GPU Acceleration)

If you have an NVIDIA GPU:

**Ubuntu:**
```bash
# Install CUDA Toolkit 11.8
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2004-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
```

**Install PyTorch with CUDA:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Model Training

### 1. Prepare Dataset

Collect images of:
- Suspension scaffolds
- Guardrails (both legitimate and fake)

Organize in YOLO format:
```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

### 2. Create Dataset YAML

Create `scaffold_dataset.yaml`:
```yaml
path: ./dataset
train: images/train
val: images/val
test: images/test

nc: 2  # number of classes
names: ['Guardrail', 'Suspension_scaffold']
```

### 3. Train the Model

```python
from ultralytics import YOLO

# Load a pretrained model
model = YOLO('yolov8n.pt')

# Train the model
results = model.train(
    data='scaffold_dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='scaffold_detection'
)

# Save the model
model.save('scaffold_1.pt')
```

### 4. Validate Model
```python
metrics = model.val()
print(f"mAP50: {metrics.box.map50}")
print(f"mAP50-95: {metrics.box.map}")
```

## Testing

### 1. Test Camera Connection
```python
import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)
print("Camera connected successfully!")
pipeline.stop()
```

### 2. Test YOLO Model
```bash
# Use webcam script for quick testing
python scripts/Guardrail.py
```

### 3. Test Full System
```bash
# Requires RealSense camera
python main.py
```

### 4. Test Drone Simulation
```bash
# In terminal 1: Start SITL
dronekit-sitl copter --home=-35.363261,149.165230,584,353

# In terminal 2: Run drone script
python scripts/drone.py
```

## Deployment

### On Companion Computer (Raspberry Pi / Jetson Nano)

1. **Copy project to drone:**
```bash
scp -r scaffold-inspection-drone/ pi@drone-ip:/home/pi/
```

2. **Install on drone:**
```bash
ssh pi@drone-ip
cd /home/pi/scaffold-inspection-drone
pip install -r requirements.txt
```

3. **Update connection string:**
Edit `main.py` to connect to actual flight controller:
```python
vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=57600)
```

4. **Run on startup:**
Create systemd service:
```bash
sudo nano /etc/systemd/system/scaffold-drone.service
```

Add:
```ini
[Unit]
Description=Scaffold Inspection Drone
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/scaffold-inspection-drone
ExecStart=/home/pi/scaffold-inspection-drone/venv/bin/python main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable scaffold-drone.service
sudo systemctl start scaffold-drone.service
```

## Troubleshooting

### Camera Issues
```bash
# Check if camera is detected
lsusb | grep Intel

# Check permissions
sudo usermod -a -G video $USER
sudo usermod -a -G dialout $USER

# Restart required after adding to groups
```

### CUDA Issues
```bash
# Check CUDA installation
nvcc --version
nvidia-smi

# Verify PyTorch sees GPU
python -c "import torch; print(torch.cuda.is_available())"
```

### Drone Connection Issues
```bash
# List available serial ports
ls /dev/tty*

# Check permissions
sudo chmod 666 /dev/ttyACM0  # or your port
```

## Performance Optimization

### For Jetson Nano / Edge Devices
```bash
# Use TensorRT for faster inference
model.export(format='engine')
model = YOLO('scaffold_1.engine')
```

### Reduce Resolution for Speed
```python
config.enable_stream(rs.stream.color, 320, 240, rs.format.rgb8, 30)
```

## Next Steps

- Fine-tune model on your specific scaffold types
- Implement autonomous waypoint navigation
- Add telemetry logging
- Create web dashboard for monitoring
- Implement emergency landing protocols

## Support

For issues or questions:
- Open an issue on GitHub
- Check Intel RealSense documentation: https://dev.intelrealsense.com/
- Check Ultralytics YOLO documentation: https://docs.ultralytics.com/
