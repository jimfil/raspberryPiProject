import paho.mqtt.client as mqtt
import json
import time
import click
import joblib
import numpy as np
from datetime import datetime

def load_model(path):
    return joblib.load(path)

def predict_next_hour(model):
    now = datetime.now()
    next_hour = (now.hour + 1) % 24

    dayOfWeek = now.weekday()

    if dayOfWeek == 5 or dayOfWeek == 6: # saturday or sunday 
        isWeekend = 1
    else:
        isWeekend = 0

    features = np.array([[next_hour, dayOfWeek, isWeekend]])

    prediction = model.predict(features)
    probabilities = model.predict_proba(features)
    print(probabilities)
    confidence = np.max(probabilities[0])
    return prediction, confidence, next_hour, features[0]


@click.command()
@click.option("--model-path", default="models/busy_predictor.joblib", help="Path to the trained ML model")
@click.option("--broker", default="localhost", help="MQTT Broker address")
@click.option("--port", type=int, default=1883, help="MQTT Broker port")
@click.option("--publish-topic", default="smartbin/bin-01/usage", help="MQTT topic to publish to")
@click.option("--interval", type=int, default=30, help="Time between predictions in seconds")
@click.option("--bin-id", default="bin-01", help="Identifier for the smart bin")

def main(model_path, broker, port, publish_topic, interval, bin_id):
    model = load_model(model_path)
    client = mqtt.Client()
    client.connect(broker, port)
    client.loop_start()
    print(f"[Virtual Sensor ML] Monitoring {publish_topic} for usage prediction")
    try:
        while True:
            prediction, confidence, next_hour, features = predict_next_hour(model)

            timestamp = time.time()

            if features[1] == 0:
                dayName = "Monday"
            elif features[1] == 1:
                dayName = "Tuesday"
            elif features[1] == 2:
                dayName = "Wednesday"
            elif features[1] == 3:
                dayName = "Thursday"
            elif features[1] == 4:
                dayName = "Friday"
            elif features[1] == 5:
                dayName = "Saturday"
            elif features[1] == 6:
                dayName = "Sunday"
            confidence_value = round(float(confidence), 3)
            is_weekend = features[2]
            payload = {
                "prediction": prediction,
                "confidence": confidence_value,
                "predicted_hour": next_hour,
                "utc_prediction_timestamp": timestamp,
                "model_name": "busy_predictor.joblib",
                "features_used": {
                    "day_of_week": dayName,
                    "hour": next_hour,
                    "is_weekend": is_weekend
                }
            }
            client.publish(publish_topic, json.dumps(payload), qos=1, retain=True)
            print(f"[Virtual Sensor ML] Predicted hour: {next_hour} Prediction: {prediction} Confidence Percentage: {confidence}")
            time.sleep(interval)
    except KeyboardInterrupt:
        client.disconnect()
        print("[Virtual Sensor ML] Disconnected from broker.")
        

if __name__ == "__main__":
    main()