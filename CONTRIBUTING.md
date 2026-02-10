# Contributing to Scaffold Inspection Drone

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, hardware)
   - Screenshots if applicable

### Suggesting Enhancements
1. Check existing issues and discussions
2. Create an issue describing:
   - The enhancement
   - Why it would be useful
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Add comments for complex logic

4. **Test your changes**
   ```bash
   # Run existing tests
   python -m pytest tests/
   
   # Test manually with camera/simulation
   python main.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```
   
   Commit message format:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Describe what you changed and why
   - Reference any related issues

## Code Style

### Python Style Guide
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and modular

Example:
```python
def detect_scaffolds(image, model):
    """
    Detect scaffolds and guardrails in image.
    
    Args:
        image (numpy.ndarray): Input RGB image
        model (YOLO): Trained YOLO model
        
    Returns:
        tuple: (detections, safety_status)
    """
    results = model(image)
    # Process results...
    return detections, safety_status
```

### Documentation
- Update README.md if adding features
- Add comments for complex algorithms
- Update SETUP.md for new dependencies

## Areas for Contribution

### High Priority
- [ ] Autonomous waypoint navigation
- [ ] Battery level monitoring integration
- [ ] Real-time telemetry dashboard
- [ ] Model optimization (TensorRT export)
- [ ] Unit tests for core functions

### Medium Priority
- [ ] Multi-drone coordination
- [ ] Wind resistance detection
- [ ] Video recording functionality
- [ ] GPS logging
- [ ] Emergency landing protocols

### Documentation
- [ ] Video tutorials
- [ ] More training examples
- [ ] Deployment guides for different platforms
- [ ] API documentation

### Testing
- [ ] Unit tests for detection logic
- [ ] Integration tests for drone control
- [ ] Benchmark performance metrics

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/scaffold-inspection-drone.git
cd scaffold-inspection-drone

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks (optional)
pre-commit install
```

## Testing Guidelines

Before submitting:
- Test with real camera (if available)
- Test with webcam fallback
- Check for memory leaks in long runs
- Verify FPS performance
- Test edge cases (no detections, multiple detections)

## Code Review Process

1. Maintainer reviews code
2. Automated tests run (if configured)
3. Discussion and revisions if needed
4. Approval and merge

## Questions?

- Open a discussion on GitHub
- Check existing issues
- Review documentation in `docs/`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
