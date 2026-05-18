"""
Model Training Script — Sign Language Translator
-------------------------------------------------
Architecture : Stacked LSTM → Dense → Softmax
Input        : (30 frames × 63 keypoints) per sample
Output       : 40-class softmax (one per sign)

Usage:
  python train.py

Outputs:
  ../data/sign_model.h5        — saved Keras model
  ../data/label_encoder.npy    — class label array
  ../data/training_history.json
"""

import os, json, time
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    LSTM, Dense, Dropout, BatchNormalization
)
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
)
from tensorflow.keras.utils import to_categorical

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "../data/keypoints")
MODEL_OUT = os.path.join(BASE, "../data/sign_model.h5")
LABELS_OUT = os.path.join(BASE, "../data/label_encoder.npy")
HIST_OUT   = os.path.join(BASE, "../data/training_history.json")
SIGNS_FILE = os.path.join(BASE, "../data/signs.json")

SEQUENCE_LENGTH = 30
# ─────────────────────────────────────────────────────────────────────────────


def load_signs():
    if os.path.exists(SIGNS_FILE):
        with open(SIGNS_FILE) as f:
            return json.load(f)
    return sorted(os.listdir(DATA_DIR))


def load_dataset(signs):
    X, y = [], []
    for idx, sign in enumerate(signs):
        sign_dir = os.path.join(DATA_DIR, sign)
        if not os.path.isdir(sign_dir):
            print(f"[WARN] No data directory for '{sign}', skipping.")
            continue
        files = [f for f in os.listdir(sign_dir) if f.endswith(".npy")]
        print(f"  {sign:20s} → {len(files)} samples")
        for fname in files:
            seq = np.load(os.path.join(sign_dir, fname))
            if seq.shape == (SEQUENCE_LENGTH, 63):
                X.append(seq)
                y.append(idx)
    return np.array(X), np.array(y)


def build_model(n_classes: int) -> tf.keras.Model:
    model = Sequential([
        # ── Encoder ──────────────────────────────────────────────────
        LSTM(128, return_sequences=True, input_shape=(SEQUENCE_LENGTH, 63)),
        BatchNormalization(),
        Dropout(0.3),

        LSTM(256, return_sequences=True),
        BatchNormalization(),
        Dropout(0.3),

        LSTM(128, return_sequences=False),
        BatchNormalization(),
        Dropout(0.3),

        # ── Classifier ───────────────────────────────────────────────
        Dense(256, activation="relu"),
        Dropout(0.4),
        Dense(128, activation="relu"),
        Dropout(0.3),
        Dense(n_classes, activation="softmax"),
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train():
    os.makedirs(os.path.join(BASE, "../data"), exist_ok=True)

    signs = load_signs()
    print(f"\n[INFO] Loading data for {len(signs)} signs …")
    X, y = load_dataset(signs)

    if len(X) == 0:
        print("[ERROR] No training data found. Run collect_data.py first.")
        return

    print(f"\n[INFO] Dataset: {X.shape[0]} samples, shape {X.shape}")

    # One-hot encode labels
    y_cat = to_categorical(y, num_classes=len(signs))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_cat, test_size=0.15, random_state=42, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.15, random_state=42
    )

    print(f"[INFO] Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

    model = build_model(len(signs))
    model.summary()

    callbacks = [
        EarlyStopping(monitor="val_accuracy", patience=20, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=8, min_lr=1e-6),
        ModelCheckpoint(MODEL_OUT, save_best_only=True, monitor="val_accuracy"),
    ]

    print("\n[INFO] Training …")
    t0 = time.time()
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=200,
        batch_size=32,
        callbacks=callbacks,
    )
    elapsed = time.time() - t0
    print(f"[INFO] Training finished in {elapsed:.1f}s")

    # ── Evaluate ─────────────────────────────────────────────────────────────
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"\n[RESULT] Test Accuracy: {acc * 100:.2f}%  |  Loss: {loss:.4f}")

    y_pred = np.argmax(model.predict(X_test), axis=1)
    y_true = np.argmax(y_test, axis=1)
    print("\n[REPORT]\n", classification_report(y_true, y_pred, target_names=signs))

    # ── Save artefacts ───────────────────────────────────────────────────────
    np.save(LABELS_OUT, np.array(signs))

    hist_serialisable = {k: [float(v) for v in vals]
                         for k, vals in history.history.items()}
    with open(HIST_OUT, "w") as f:
        json.dump(hist_serialisable, f, indent=2)

    print(f"\n[SAVED] Model   → {MODEL_OUT}")
    print(f"[SAVED] Labels  → {LABELS_OUT}")
    print(f"[SAVED] History → {HIST_OUT}")


if __name__ == "__main__":
    train()
