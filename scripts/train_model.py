import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

DATA_PATH = Path(__file__).parent / "diabetes.csv"
MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "model_exp5.h5"
SCALER_PATH = MODEL_DIR / "scaler.joblib"

FEATURE_ORDER = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker",
    "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits",
    "Veggies", "HvyAlcoholConsump", "AnyHealthcare",
    "NoDocbcCost", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk",
    "Sex", "Age", "Education", "Income"
]

TARGET_COL = "Diabetes_012"

def load_data(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")
    df = pd.read_csv(path)
    # Ensure all feature columns exist
    missing = [c for c in FEATURE_ORDER + [TARGET_COL] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")
    # Fill NAs
    df = df.copy()
    df[FEATURE_ORDER] = df[FEATURE_ORDER].fillna(0)
    df[TARGET_COL] = df[TARGET_COL].fillna(0)
    return df

def build_model(input_dim: int):
    model = Sequential([
        Dense(64, activation="relu", input_shape=(input_dim,)),
        Dense(32, activation="relu"),
        Dense(16, activation="relu"),
        Dense(1, activation="linear")  # regression output 0/1/2
    ])
    model.compile(optimizer=Adam(1e-3), loss="mse", metrics=["mae"])
    return model

def main():
    print("\n=== Training model ===\n")
    df = load_data(DATA_PATH)
    X = df[FEATURE_ORDER].astype(float).values
    y = df[TARGET_COL].astype(float).values

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=None)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)

    print("✓ Data loaded and scaled")

    model = build_model(X_train_scaled.shape[1])
    history = model.fit(
        X_train_scaled, y_train,
        validation_data=(X_val_scaled, y_val),
        epochs=30,
        batch_size=32,
        verbose=2
    )

    # Evaluate
    loss, mae = model.evaluate(X_val_scaled, y_val, verbose=0)
    print(f"\nValidation MAE: {mae:.4f}, MSE: {loss:.4f}")

    # Save model and scaler
    model.save(MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"\n Model saved to {MODEL_PATH}")
    print(f"Scaler saved to {SCALER_PATH}")

if __name__ == "__main__":
    main()