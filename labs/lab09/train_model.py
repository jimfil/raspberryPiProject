import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def generate_training_data(days=30, seed=42):
    rng = np.random.default_rng(seed)
    rows = []

    for day in range(days):
        day_of_week = day % 7  # 0 = Monday, 6 = Sunday
        is_weekend = 1 if day_of_week >= 5 else 0

        for hour in range(24):
            # Determine base_rate based on day and hour
            if is_weekend:
                base_rate = 2
            elif 8 <= hour <= 10:
                base_rate = 15
            elif 11 <= hour <= 14:
                base_rate = 25
            elif 15 <= hour <= 17:
                base_rate = 12
            elif 18 <= hour <= 20:
                base_rate = 8
            else:
                base_rate = 1

            # Generate event_count using normal distribution
            event_count = int(rng.normal(loc=base_rate, scale=base_rate * 0.3))
            
            # Clamp event_count to minimum 0
            if event_count < 0:
                event_count = 0

            # Determine label
            label = "busy" if event_count > 10 else "quiet"

            rows.append({
                "day_of_week": day_of_week,
                "hour": hour,
                "is_weekend": is_weekend,
                "event_count": event_count,
                "label": label
            })

    return pd.DataFrame(rows)

def train_and_save(output_dir="models"):
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate data
    df = generate_training_data()

    # Define Features and Target
    X = df[['day_of_week', 'hour', 'is_weekend']]
    y = df['label']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train Random Forest
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Predict and Evaluate
    y_pred = model.predict(X_test)
    
    print("--- Model Evaluation ---")
    print(classification_report(y_test, y_pred))

    # Save model
    model_path = os.path.join(output_dir, "busy_predictor.joblib")
    joblib.dump(model, model_path)

    print(f"Model successfully saved to: {model_path}")
    return model

if __name__ == "__main__":
    train_and_save()