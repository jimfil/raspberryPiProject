import paho.mqtt.client as mqtt




BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/test"


def on_connect(client, userdata, flags, rc):
    #Callback που εκτελείται όταν ο client συνδέεται στον broker.
    # rc == 0 σημαίνει επιτυχής σύνδεση
    if rc == 0:
        print("Συνδέθηκα επιτυχώς στον broker!")
        # Κάνουμε subscribe στο επιλεγμένο topic
        client.subscribe(TOPIC)
        print(f"Έγινε subscribe στο topic: {TOPIC}")
    else:
        print(f"Αποτυχία σύνδεσης. Κωδικός: {rc}")

def on_message(client, userdata, msg):
    #Callback που εκτελείται όταν λαμβάνεται μήνυμα από κάποιο topic.
    #- msg.topic: το topic από το οποίο ήρθε το μήνυμα
    #- msg.payload: το περιεχόμενο του μηνύματος (bytes)
    print(f"Λήφθηκε μήνυμα στο topic '{msg.topic}': {msg.payload.decode('utf-8')}")



def main():
    # Δημιουργία ενός MQTT client
    client = mqtt.Client()
    # Σύνδεση των callback functions ώστε ο client να ξέρει
    # τι να κάνει όταν συνδέεται ή όταν λαμβάνει μήνυμα.
    client.on_connect = on_connect
    client.on_message = on_message
    # Σύνδεση στον MQTT broker.
    # Το keepalive=60 σημαίνει ότι ο client θα ενημερώνει τον broker ότι είναι ενεργός κάθε 60
    # δευτερόλεπτα.
    client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=60)
    print("👂 Περιμένω μηνύματα... Πατήστε Ctrl+C για έξοδο.")
    # Το loop_forever κρατά τον client σε λειτουργία,
    # ακούγοντας συνεχώς για γεγονότα (π.χ. εισερχόμενα μηνύματα).
    client.loop_forever()
    
if __name__ == "__main__":
    main()

