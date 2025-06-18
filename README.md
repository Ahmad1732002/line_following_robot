# Class Project: Line Following Robot

## 📌 Project Summary
This project is an autonomous robot built to follow a black line on a modular field. The field contains various challenges like intersections, ramps, obstacles, gaps, and a reflective silver end marker. The robot must detect and respond to these features in real time without prior knowledge of the field layout.

## 🚗 What the Robot Can Do
- Follows a black line using computer vision
- Detects and responds to green intersection markers
- Handles left, right, and U-turn decisions
- Avoids or reacts to obstacles and changes in the path
- Stops at the silver reflective strip that marks the end of the course

## 🔧 Hardware & Tools Used
- NVIDIA Jetson Nano + JetBot platform
- JetBot Camera
- Differential drive motor system
- Jupyter Notebook interface
- OpenCV for image processing
- ipywidgets for real-time image feedback

## 🧠 Key Features in the Code
- `find_black_object_center`: Locates the center of the black line
- `find_green_square`: Detects green markers that indicate turns
- Autonomous decision making:
  - Turns left/right based on marker position
  - Performs U-turns at dead ends
  - Follows the line forward if no markers are found
- Smooth motor control with gradual deceleration
- Live camera feed and processed feedback using Jupyter widgets

## ▶️ How to Run
1. Power up the JetBot and connect via Jupyter Notebook.
2. Open and run the notebook containing the robot control code.
3. Place the robot at the starting tile of the course.
4. Let the robot run autonomously. It will:
   - Follow the black line
   - React to green markers
   - Stop at the silver tape
5. Observe behavior to confirm detection and control logic.

## 🧪 Calibration Guidelines
- Use the center 150x150 cropped camera view for better focus.
- Tune threshold values for black and green detection as needed.
- Make sure lighting conditions are stable for consistent detection.
- No code changes or sensor calibration are allowed once a scoring run starts.

## 🏁 Field & Gameplay Rules (Summary)
- Field is built from unknown tile arrangements (min 8 tiles).
- Black lines may have 0–20 cm gaps.
- Obstacles, debris, speed bumps, and ramps may be present.
- Green 25x25 mm squares indicate turns:
  - One green square = direction marker (left/right)
  - Two green squares = dead end (U-turn)
- Robot must stay on the field and operate fully autonomously.






