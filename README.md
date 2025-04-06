# project
#  Drowsiness & Yawn Detection System

A real-time Python-based system that detects drowsiness and yawning using computer vision techniques. Designed to help **students stay alert while studying** and **drivers avoid accidents caused by sleepiness**.

---

##  Features

- Detects **eye closure** using Eye Aspect Ratio (EAR)
- Identifies **yawning** using lip distance measurement
- Provides **audio alerts** using `espeak` to wake users up
- Works with any standard **webcam**
- Lightweight and real-time performance

---

##  How It Works

1. Captures live video feed using OpenCV
2. Detects face and facial landmarks with Dlib
3. Calculates EAR to detect eye closure (drowsiness)
4. Measures lip distance to detect yawns
5. Plays alert audio when thresholds are crossed

---

##  Tech Stack

- Python 3
- OpenCV
- Dlib
- imutils
- NumPy
- Haar Cascades (for face detection)
- `espeak` (for voice alerts)
