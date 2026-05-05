from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse
from apiFunc import load_events, EVENTS_FILE
import json
import paho.mqtt.client as mqtt
import threading
from datetime import datetime, timezone

topic_store = {}
topic_lock = threading.Lock()

def on_message(client, userdata, msg):
    with topic_lock:
        topic_store[msg.topic] = {
            "topic": msg.topic,
            "payload": msg.payload.decode("utf-8", errors="replace"),
            "qos": msg.qos,
            "retain": msg.retain,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }

try:
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="wastebin-api", clean_session=False)
except AttributeError:
    mqtt_client = mqtt.Client(client_id="wastebin-api", clean_session=False)

mqtt_client.on_message = on_message
try:
    mqtt_client.connect_async("localhost", 1883, keepalive=60)
except Exception as e:
    print(f"Warning: MQTT connection failed: {e}")
    
mqtt_client.subscribe("smartbin/#", qos=1)
mqtt_client.loop_start()

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Smart Wastebin API",
    description="REST API for querying Smart Wastebin sensor data and bin status",
)

ns_bins = api.namespace("bins", description="Wastebin operations")
ns_sensors = api.namespace("sensors", description="Sensor operations")
ns_mqtt = api.namespace("mqtt", description="MQTT operations")
ns_events = api.namespace("events", description="Motion events from pipeline")

bin_model = api.model("Bin", {
    "id": fields.String(required=True, description="Bin unique identifier"),
    "name": fields.String(description="Human-readable name"),
    "location": fields.String(description="Deployment location"),
    "status": fields.String(description="Current status"),
})

event_model = api.model("Event", {
    "resultTime": fields.String(description="ISO timestamp of the event"),
    "madeBySensor": fields.String(description="Sensor ID that produced this event"),
    "hasSimpleResult": fields.String(description="Motion state (detected/clear)"),
    "pipeline_latency_ms": fields.Float(description="Pipeline latency in ms"),
})

mqtt_message_model = api.model("MqttMessage", {
    "topic": fields.String(required=True, description="MQTT topic to publish to"),
    "message": fields.String(required=True, description="Message payload"),
})

sensor_model = api.model("Sensor", {
    "topic": fields.String(required=True, description="MQTT topic to publish to"),
    "payload" : fields.String(required=True, description="Message payload"),
    "qos" : fields.Integer(required=True, description="Quality of Service"),
    "retain" : fields.Boolean(required=True, description="Retain this message on the broker", default=False),
})

events_parser = reqparse.RequestParser()
events_parser.add_argument("limit", type=int, default=50, help="Max events to return")
events_parser.add_argument("start", type=str, help="Start datetime (ISO format)")
events_parser.add_argument("end", type=str, help="End datetime (ISO format)")

bin_parser = reqparse.RequestParser()
bin_parser.add_argument("bin_id", type=str, required=True, help="Bin unique identifier")

allbins_parser = reqparse.RequestParser()
allbins_parser.add_argument("limit", type=int, default=50, help="Max bins to return")
allbins_parser.add_argument("offset", type=int, default=0, help="Offset")

mqtt_parser = reqparse.RequestParser()
mqtt_parser.add_argument("topic", type=str, required=True, help="MQTT topic to publish to")
mqtt_parser.add_argument("message", type=str, required=True, help="Message payload")

@ns_bins.route("/")
@ns_bins.expect(allbins_parser)
class BinList(Resource):
    @ns_bins.marshal_with(bin_model, as_list=True)
    def get(self):
        """List all bins"""
        return {"bins": []}, 200


@ns_bins.route("/<string:bin_id>")
@ns_bins.expect(bin_parser)
class BinItem(Resource):
    @ns_bins.marshal_with(bin_model)
    def get(self, bin_id):
        """Get details for a specific bin"""
        return {"bin_id": bin_id}, 200


@ns_bins.route("/<string:bin_id>/sensors")
class BinSensors(Resource):
    def get(self, bin_id):
        """List sensors on a specific bin"""
        return {"bin_id": bin_id, "sensors": []}, 200


@ns_bins.route("/<string:bin_id>/events")
@ns_bins.expect(events_parser)
class BinEvents(Resource):
    @ns_bins.marshal_list_with(event_model)
    def get(self, bin_id):
        """Get motion events for a specific bin"""
        args = events_parser.parse_args()
        events = load_events(
            EVENTS_FILE,
            limit=args.get("limit"),
            sensor_id=get_sensor_for_bin(bin_id),
        )
        return events


@ns_bins.route("/<string:bin_id>/emptied")
class BinEmptied(Resource):
    @ns_bins.marshal_with(bin_model)
    def post(self, bin_id):
        """Record that a bin was emptied"""
        return {"message": f"Bin {bin_id} emptied"}, 200


@ns_sensors.route("/")
class SensorList(Resource):
    def get(self):
        """List all sensors"""
        return {"sensors": []}, 200


@ns_sensors.route("/<string:sensor_id>")
class SensorItem(Resource):
    def get(self, sensor_id):
        """Get details for a specific sensor"""
        return {"sensor_id": sensor_id}, 200







@ns_mqtt.route("/publish")
@ns_mqtt.expect(mqtt_parser)
class MqttPublish(Resource):
    def post(self):
        """Publish a message to an MQTT topic"""
        try:
            args = mqtt_parser.parse_args()
            topic = args.get("topic")
            message = args.get("message")

            if not topic or message is None:
                return {"error": "Missing topic or message in payload"}, 400

            mqtt_client.publish(topic, message)
            return {"message": "Message published"}, 200
        except Exception as e:
            return {"message": str(e)}, 500
        





@ns_mqtt.route("/topics")
class MqttTopics(Resource):
    @ns_mqtt.marshal_list_with(sensor_model)
    def get(self):
        """List known MQTT topics and their last retained value"""
        with topic_lock:
            return list(topic_store.values()), 200


@ns_events.route("/")
class EventList(Resource):
    @ns_events.expect(events_parser)
    @ns_events.marshal_list_with(event_model)
    def get(self):
        """List all motion events produced by the pipeline"""
        args = events_parser.parse_args()
        events = load_events(
            EVENTS_FILE,
            limit=args.get("limit")
        )
        return events


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

