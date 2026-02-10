# Models Directory

## Required Model File

Place your trained YOLO model here:
- **Filename**: `scaffold_1.pt`
- **Type**: YOLOv8 PyTorch model
- **Classes**: 
  - 0: Guardrail
  - 1: Suspension_scaffold

## Model Not Included

The trained model (`scaffold_1.pt`) is **not included** in this repository due to:
- Large file size (typically 5-50MB)
- Custom training on specific scaffold dataset
- GitHub file size limitations

## Getting the Model

### Option 1: Use Pre-trained (If Available)
If a pre-trained model is available:
```bash
# Download from release page or provided link
wget [MODEL_DOWNLOAD_URL] -O models/scaffold_1.pt
```

### Option 2: Train Your Own
Follow the training guide in `docs/SETUP.md` to train your own model:

```python
from ultralytics import YOLO

# Load base model
model = YOLO('yolov8n.pt')

# Train on your scaffold dataset
results = model.train(
    data='scaffold_dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='scaffold_detection'
)

# Export trained model
model.save('models/scaffold_1.pt')
```

### Option 3: Use Pre-trained YOLOv8 (For Testing)
For initial testing without custom model:
```python
# Edit main.py to use base YOLOv8
model = YOLO('yolov8n.pt')  # General object detection
```

## Model Formats

The model can be exported to various formats for optimization:

```python
from ultralytics import YOLO

model = YOLO('scaffold_1.pt')

# Export to ONNX
model.export(format='onnx')

# Export to TensorRT (for Jetson/NVIDIA)
model.export(format='engine')

# Export to CoreML (for iOS/macOS)
model.export(format='coreml')
```

## Model Storage Recommendations

For larger projects:
- Use **Git LFS** for version control of model files
- Host models on cloud storage (AWS S3, Google Drive, Hugging Face)
- Use model versioning for experiment tracking

## Training Tips

- **Dataset Size**: Minimum 500 images per class
- **Augmentation**: Use rotation, scaling, brightness variations
- **Epochs**: Start with 100, monitor for overfitting
- **Validation**: Keep 20% of data for validation
- **Class Balance**: Ensure roughly equal samples per class
