import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs
sys.stderr = open(os.devnull, 'w')        # Hide MediaPipe warnings

import cv2
import numpy as np
import mediapipe as mp
import subprocess
import time

print("[INFO] Initializing Drowsiness Detection System...")
for i in range(3):
    print("." * (i + 1))
    time.sleep(0.3)
print("[INFO] Starting video stream.\n")

# Thresholds
EAR_THRESHOLD = 0.24
YAWN_THRESHOLD = 27
EAR_CONSEC_FRAMES = 30

# Alert control
sleep_start_time = None
yawn_start_time = None
sleep_alerted = False
yawn_alerted = False

# MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
TOP_LIP = [13]
BOTTOM_LIP = [14]

def calculate_EAR(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def lip_distance(top, bottom):
    return abs(top[0][1] - bottom[0][1])

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            left_eye = np.array([(landmarks[i].x * w, landmarks[i].y * h) for i in LEFT_EYE], dtype=np.int32)
            right_eye = np.array([(landmarks[i].x * w, landmarks[i].y * h) for i in RIGHT_EYE], dtype=np.int32)
            left_ear = calculate_EAR(left_eye)
            right_ear = calculate_EAR(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            top_lip = [(landmarks[i].x * w, landmarks[i].y * h) for i in TOP_LIP]
            bottom_lip = [(landmarks[i].x * w, landmarks[i].y * h) for i in BOTTOM_LIP]
            mouth_open = lip_distance(top_lip, bottom_lip)

            # Draw eyes
            cv2.polylines(frame, [left_eye], isClosed=True, color=(0, 255, 0), thickness=1)
            cv2.polylines(frame, [right_eye], isClosed=True, color=(0, 255, 0), thickness=1)

            # Draw mouth
            for point in top_lip + bottom_lip:
                cv2.circle(frame, (int(point[0]), int(point[1])), 2, (0, 255, 0), -1)

            # EAR and Yawn display
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            cv2.putText(frame, f"YAWN: {mouth_open:.2f}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

            now = time.time()

            # Sleep detection
            if avg_ear < EAR_THRESHOLD:
                if sleep_start_time is None:
                    sleep_start_time = now
                elif now - sleep_start_time > 1 and not sleep_alerted:
                    subprocess.call(["espeak", "You are sleepy"])
                    sleep_alerted = True
                    cv2.putText(frame, "SLEEPY ALERT!", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            else:
                sleep_start_time = None
                sleep_alerted = False

            # Yawn detection
            if mouth_open > YAWN_THRESHOLD:
                if yawn_start_time is None:
                    yawn_start_time = now
                elif now - yawn_start_time > 1 and not yawn_alerted:
                    subprocess.call(["espeak", "You are yawning"])
                    yawn_alerted = True
                    cv2.putText(frame, "YAWNING!", (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            else:
                yawn_start_time = None
                yawn_alerted = False

    cv2.imshow("Drowsiness Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

