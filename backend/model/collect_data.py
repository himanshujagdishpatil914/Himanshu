"""
Data Collection Script for Sign Language Translator
-----------------------------------------------------
Usage:
  python collect_data.py

Supports BOTH HANDS — left hand + right hand keypoints are captured
together giving 126 values per frame (21 landmarks × 3 × 2 hands).

If only one hand is visible, the missing hand is filled with zeros.
This means signs that only need one hand still work perfectly.

Controls:
  ENTER  — record one 30-frame sample for the current sign
  N      — next sign
  P      — previous sign
  Q      — quit
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import json

# ── Config ────────────────────────────────────────────────────────────────────
DATA_DIR        = os.path.join(os.path.dirname(__file__), "../data/keypoints")
SEQUENCE_LENGTH = 30    # frames per sample
SAMPLES_PER_SIGN = 200  # target samples per sign

SIGNS = [
    # Common Phrases
    "hello", "yes", "no", "thankyou", "please",
    "sorry", "help", "good", "bad", "stop",
    # Expressions
    "iloveyou", "goodmorning", "goodnight", "howareyou", "fine",
    # Alphabet A–J
    "A", "B", "C", "D", "E",
    "F", "G", "H", "I", "J",
    # Numbers 1–10
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10",
    # Actions
    "eat", "drink", "sleep", "come", "go",
]
# ─────────────────────────────────────────────────────────────────────────────

# Each hand = 21 landmarks × 3 (x,y,z) = 63 values
# Both hands = 63 × 2 = 126 values per frame
KEYPOINTS_PER_HAND = 63
TOTAL_KEYPOINTS    = KEYPOINTS_PER_HAND * 2   # 126

mp_hands    = mp.solutions.hands
mp_drawing  = mp.solutions.drawing_utils
mp_draw_styles = mp.solutions.drawing_styles

os.makedirs(DATA_DIR, exist_ok=True)

# Save sign list so training / inference scripts can load it
with open(os.path.join(DATA_DIR, "../signs.json"), "w") as f:
    json.dump(SIGNS, f, indent=2)


# ── Keypoint extraction ───────────────────────────────────────────────────────
def extract_keypoints(results):
    """
    Returns a flat numpy array of 126 values:
      [left_hand_63_values, right_hand_63_values]

    If a hand is not detected its 63 values are all zeros.
    MediaPipe labels each detected hand as 'Left' or 'Right'
    (mirrored label — 'Right' means the user's right hand).
    """
    left  = np.zeros(KEYPOINTS_PER_HAND)
    right = np.zeros(KEYPOINTS_PER_HAND)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):
            label = handedness.classification[0].label  # 'Left' or 'Right'
            kp    = np.array(
                [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
            ).flatten()   # 63 values

            if label == "Left":
                left = kp
            else:
                right = kp

    return np.concatenate([left, right])   # shape: (126,)


# ── HUD helpers ───────────────────────────────────────────────────────────────
def draw_hud(frame, sign, existing, recording=False, frame_num=0):
    h, w = frame.shape[:2]

    # Top bar
    bar_color = (180, 0, 0) if recording else (30, 30, 30)
    cv2.rectangle(frame, (0, 0), (w, 68), bar_color, -1)

    if recording:
        cv2.putText(
            frame,
            f"  RECORDING  {frame_num + 1}/{SEQUENCE_LENGTH}",
            (10, 44), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2,
        )
    else:
        cv2.putText(
            frame,
            f"  Sign: {sign}    Samples: {existing}/{SAMPLES_PER_SIGN}",
            (10, 44), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 180), 2,
        )

    # Bottom hint bar
    cv2.rectangle(frame, (0, h - 36), (w, h), (20, 20, 20), -1)
    cv2.putText(
        frame,
        "  ENTER=Record   N=Next   P=Prev   Q=Quit",
        (8, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160, 160, 160), 1,
    )


# ── Main ──────────────────────────────────────────────────────────────────────
def collect():
    cap = cv2.VideoCapture(0)
    current_sign_idx = 0

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,                 # ← detect BOTH hands
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    ) as hands:

        print("\n" + "═" * 58)
        print("  SignAI — Data Collection  (BOTH HANDS SUPPORTED)")
        print("═" * 58)
        print(f"  Total signs   : {len(SIGNS)}")
        print(f"  Frames/sample : {SEQUENCE_LENGTH}")
        print(f"  Target samples: {SAMPLES_PER_SIGN} per sign")
        print(f"  Keypoints     : {TOTAL_KEYPOINTS} per frame (both hands)")
        print("─" * 58)
        print("  Controls:")
        print("    ENTER  → record one sample")
        print("    N      → next sign")
        print("    P      → previous sign")
        print("    Q      → quit")
        print("═" * 58 + "\n")

        while cap.isOpened():
            sign     = SIGNS[current_sign_idx]
            sign_dir = os.path.join(DATA_DIR, sign)
            os.makedirs(sign_dir, exist_ok=True)

            existing = len([f for f in os.listdir(sign_dir) if f.endswith(".npy")])

            ret, frame = cap.read()
            if not ret:
                break

            frame   = cv2.flip(frame, 1)
            rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            # Draw hand skeletons for BOTH hands
            if results.multi_hand_landmarks:
                for hl in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hl, mp_hands.HAND_CONNECTIONS,
                        mp_draw_styles.get_default_hand_landmarks_style(),
                        mp_draw_styles.get_default_hand_connections_style(),
                    )

            # Show which hands are detected
            hands_visible = []
            if results.multi_handedness:
                for hd in results.multi_handedness:
                    hands_visible.append(hd.classification[0].label)
            hand_str = " + ".join(hands_visible) if hands_visible else "No hand"
            cv2.putText(
                frame, f"  Detected: {hand_str}",
                (10, 96), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 220, 255) if hands_visible else (80, 80, 80), 2,
            )

            draw_hud(frame, sign, existing)
            cv2.imshow("SignAI — Data Collection (Both Hands)", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            elif key == ord("n"):
                current_sign_idx = (current_sign_idx + 1) % len(SIGNS)
                print(f"[SIGN] ▶  {SIGNS[current_sign_idx]}")

            elif key == ord("p"):
                current_sign_idx = (current_sign_idx - 1) % len(SIGNS)
                print(f"[SIGN] ◀  {SIGNS[current_sign_idx]}")

            elif key == 13:  # ENTER
                if existing >= SAMPLES_PER_SIGN:
                    print(f"[SKIP] '{sign}' already has {existing}/{SAMPLES_PER_SIGN} samples.")
                    continue

                sequence = []
                print(f"[REC]  Recording sample {existing + 1}/{SAMPLES_PER_SIGN} for '{sign}' …")

                for frame_num in range(SEQUENCE_LENGTH):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame   = cv2.flip(frame, 1)
                    rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(rgb)

                    keypoints = extract_keypoints(results)   # (126,)
                    sequence.append(keypoints)

                    # Draw skeletons during recording
                    if results.multi_hand_landmarks:
                        for hl in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                frame, hl, mp_hands.HAND_CONNECTIONS,
                                mp_draw_styles.get_default_hand_landmarks_style(),
                                mp_draw_styles.get_default_hand_connections_style(),
                            )

                    draw_hud(frame, sign, existing,
                             recording=True, frame_num=frame_num)
                    cv2.imshow("SignAI — Data Collection (Both Hands)", frame)
                    cv2.waitKey(1)

                # Save as (30, 126) array
                np.save(
                    os.path.join(sign_dir, f"{existing}.npy"),
                    np.array(sequence),   # shape: (SEQUENCE_LENGTH, 126)
                )
                print(f"[SAVED] {sign}/{existing}.npy  shape={np.array(sequence).shape}")

    cap.release()
    cv2.destroyAllWindows()
    print("\n[DONE] Data collection complete.")


if __name__ == "__main__":
    collect()
