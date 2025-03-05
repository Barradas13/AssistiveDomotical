# AssistiveDomotical

### Key Features

1. **Real-Time Eye Blink Detection**
   - Uses facial landmarks (68-point model) with `dlib` library
   - Calculates Eye Aspect Ratio (EAR) to detect blinks
   - Customizable detection threshold with auto-calibration

2. **Observer Pattern Implementation** 
   - Observable (`observadorMainClass`) notifies observers (like GUI) about blink events

3. **Calibration System** 
   - 10-second calibration process to determine user-specific eye ratios
   - Calculates min/max EAR values and sets optimal threshold

---

### Core Components

1. **Main Execution (`main.py`)**:
```python
# Initializes system with video source and GUI
sistema = observadorMainClass("video.mp4")  # Can use 0 for webcam
menu = Menu()
sistema.attach(menu)  # Connect GUI as observer

# Start processing in separate thread
threading.Thread(target=menu.run).start()  
sistema.executar()
```

2. **Eye Detection Engine (`observadorMainClass.py`)**:
   - **Landmark Detection**:
     ```python
     detector = dlib.get_frontal_face_detector()
     predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
     ```
   - **EAR Calculation**:
     ```python
     # Right eye: points 36-41
     # Left eye: points 42-47
     EAR = (vertical_dist1 + vertical_dist2) / (2 * horizontal_dist)
     ```

3. **Observer Pattern (`observerClasses.py`)**:
   ```python
   class DataEvent:
       piscou = True  # Blink detected
       tempo = 0      # Timestamp

   class Observable(ABC):
       def attach/detach/notify...

   class Observer(ABC):
       def update...
   ```

4. **Geometric Calculations (`equacoes.py`)**:
   ```python
   def razaoDistOlhos(p2, p6, p3, p5, p1, p4):
       # Calculates vertical and horizontal distances
       return (vertical1 + vertical2) / (2 * horizontal)
   ```

---

### Technical Implementation

**Blink Detection Workflow**:
1. Frame capture → CLAHE preprocessing
2. Face detection → Landmark identification
3. EAR calculation for both eyes
4. Threshold comparison using calibrated values
5. Observer notification on blink detection

**Calibration Process**:
```python
def calibrar_razao_olhos(self):
    # Collects 10 seconds of EAR data
    self.limiar = (max + min) / 2  # Auto-set threshold
```

**Visual Feedback**:
- Green circle (blink detected)
- Red circle (eyes open)
- Landmark points overlay
- Real-time FPS counter

---

### Configuration Options

1. **Video Source**:
   ```python
   # Use webcam (0) or video file
   sistema = observadorMainClass(0)  # Webcam
   sistema = observadorMainClass("input.mp4")  # Video file
   ```

2. **Detection Parameters**:
   ```python
   self.limiar = 0.27  # Default threshold (0.2-0.3 typical)
   CLAHE clipLimit=2.0  # Contrast enhancement
   ```

3. **Performance Settings**:
   ```python
   video_capture.set(3, 640)  # Width
   video_capture.set(4, 480)  # Height
   ```

---

### Dependencies

```toml
[Tool.poetry.dependencies]
python = "^3.10"
opencv-python = "^4.7.0"
dlib = "^19.24.0"
numpy = "^1.24.3"
```

---

### Testing & Usage

1. **Calibration**:
   ```python
   sistema.calibrar_razao_olhos()  # Uncomment in main
   ```

2. **Threshold Adjustment**:
   ```python
   sistema.limiar = 0.25  # Lower = more sensitive
   ```

3. **Event Handling**:
   ```python
   # Observer receives events with blink duration
   def update(self, subject, dataEvent):
       if dataEvent.piscou:
           print(f"Blink detected! Duration: {dataEvent.tempo:.2f}s")
   ```

---

This system provides a robust foundation for eye-controlled interfaces, with potential applications in:
- Accessibility tools
- Driver drowsiness detection
- Hands-free device control
- Behavioral research
