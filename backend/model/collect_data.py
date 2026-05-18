"""
Data Collection Script for Sign Language Translator
-----------------------------------------------------
Usage:
  python collect_data.py

This script opens your webcam, detects hand landmarks using MediaPipe,
and saves keypoint sequences for each sign label.

Controls:
  Press the KEY shown on screen to start recording for that sign.
  Press 'q' to quit.
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import json
import time

# ── Config ───────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/keypoints")
SEQUENCE_LENGTH = 30          # frames per sample
SAMPLES_PER_SIGN = 200        # samples to collect per sign

SIGNS = [
    "hello", "yes", "no", "thankyou", "please",
    "sorry", "help", "good", "bad", "stop",
    "iloveyou", "goodmorning", "goodnight", "howareyou", "fine",
    "A", "B", "C", "D", "E",
    "F", "G", "H", "I", "J",
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10",
    "eat", "drink", "sleep", "come", "go"
]
# ─────────────────────────────────────────────────────────────────────────────

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

os.makedirs(DATA_DIR, exist_ok=True)

# Save sign list so training script can load it
with open(os.path.join(DATA_DIR, "../signs.json"), "w") as f:
    json.dump(SIGNS, f)


def extract_keypoints(results):
    """Return a flat numpy array of 63 values (21 landmarks × 3) for one hand."""
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
    return np.zeros(63)


def collect():
    cap = cv2.VideoCapture(0)
    current_sign_idx = 0

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    ) as hands:

        print(f"\n[INFO] Ready. Press ENTER to start collecting for: {SIGNS[current_sign_idx]}")
        print("[INFO] Press 'n' for next sign, 'p' for previous, 'q' to quit.\n")

        while cap.isOpened():
            sign = SIGNS[current_sign_idx]
            sign_dir = os.path.join(DATA_DIR, sign)
            os.makedirs(sign_dir, exist_ok=True)

            # Count existing samples
            existing = len([f for f in os.listdir(sign_dir) if f.endswith(".npy")])

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                for hl in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)

            # HUD
            cv2.rectangle(frame, (0, 0), (640, 60), (30, 30, 30), -1)
            cv2.putText(frame, f"Sign: {sign}  Samples: {existing}/{SAMPLES_PER_SIGN}",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 180), 2)
            cv2.imshow("Data Collection", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("n"):
                current_sign_idx = (current_sign_idx + 1) % len(SIGNS)
            elif key == ord("p"):
                current_sign_idx = (current_sign_idx - 1) % len(SIGNS)
            elif key == 13:  # ENTER – collect one sample
                if existing >= SAMPLES_PER_SIGN:
                    print(f"[SKIP] {sign} already has {existing} samples.")
                    continue

                sequence = []
                print(f"[REC] Recording sample {existing + 1} for '{sign}' ...")

                for frame_num in range(SEQUENCE_LENGTH):
                    ret, frame = cap.read()
                    frame = cv2.flip(frame, 1)
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(rgb)

                    keypoints = extract_keypoints(results)
                    sequence.append(keypoints)

                    if results.multi_hand_landmarks:
                        for hl in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)

                    cv2.rectangle(frame, (0, 0), (640, 60), (200, 0, 0), -1)
                    cv2.putText(frame, f"RECORDING {frame_num + 1}/{SEQUENCE_LENGTH}",
                                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.imshow("Data Collection", frame)
                    cv2.waitKey(1)

                np.save(os.path.join(sign_dir, f"{existing}.npy"), np.array(sequence))
                print(f"[SAVED] {sign}/sample_{existing}.npy")

    cap.release()
    cv2.destroyAllWindows()
    print("\n[DONE] Data collection complete.")


if __name__ == "__main__":
    collect()
