import paho.mqtt.client as mqtt
import time

BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/test"

def main():
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=60)
    # Μικρή παύση ώστε να ολοκληρωθεί σωστά η σύνδεση πριν γίνει publish
    time.sleep(1)
    message = "Hello world from Python via MQTT!"
    # Αποστολή του μηνύματος (publish) στο συγκεκριμένο topic
    # Το αποτέλεσμα είναι tuple (status, mid)
    result = client.publish(TOPIC, payload=message, qos=0)
    # result[0] == 0 σημαίνει επιτυχής αποστολή
    if result[0] == 0:
        print(f"Μήνυμα στάλθηκε στο topic '{TOPIC}': {message}")
    else:
        print(f"Αποτυχία αποστολής.")
    client.disconnect()

if __name__ == "__main__":
    main()