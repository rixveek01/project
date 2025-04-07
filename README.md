Drowsiness Detection System

This is a real-time drowsiness detection system that uses a webcam to monitor signs of sleepiness. It detects eye closure and yawning and provides voice alerts to help users stay alert, especially while studying or driving.

Features 

1. Real-time detection using webcam feed

2. Eye closure detection using Eye Aspect Ratio (EAR)

3. Yawn detection using lip distance

4. Voice alerts using espeak

5. Uses MediaPipe FaceMesh (no external model files required)

6. Suppresses unnecessary warnings for a cleaner output

 ## Model Used
The project uses the FaceMesh model from the MediaPipe library. It detects 468 facial landmarks, including eyes and lips, directly from the video stream. It does not require any external files like .xml or .dat.

## Requirements
Python 3

OpenCV

NumPy

MediaPipe

espeak (for voice alerts)


How It Works
Captures live video from the webcam.

Uses MediaPipe FaceMesh to identify key facial landmarks.

Calculates EAR (Eye Aspect Ratio) from eye landmarks to detect if eyes are closed.

Calculates lip distance to detect if the mouth is wide open (yawning).

If drowsiness or yawning is detected for more than one second, it gives a voice alert.



Output
The system displays the EAR and Yawn values on the video feed. Alerts such as "You are sleepy" or "You are yawning" will appear on screen and be spoken aloud when thresholds are crossed.

License
This project is open-source and free to use or modify.
