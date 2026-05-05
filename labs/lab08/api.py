from flask import Flask, request
from flask_restx import Api, Resource, fields
from apiFunc import load_events, EVENTS_FILE
import json
import paho.mqtt.client as mqtt

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

event_model = api.model('Event', {
    '@context': fields.Raw(description='JSON-LD Context'),
    '@type': fields.String(description='Entity Type'),
    'device_id': fields.String(description='Device ID'),
    'sensor_ref': fields.String(description='Sensor Reference'),
    'wastebin_ref': fields.String(description='Wastebin Reference'),
    'environment_ref': fields.String(description='Environment Reference'),
    'event_time': fields.String(description='Event Time'),
    'event_type': fields.String(description='Event Type'),
    'motion_state': fields.String(description='Motion State'),
    'seq': fields.Integer(description='Sequence Number'),
    'run_id': fields.String(description='Run ID'),
    'ingest_time': fields.String(description='Ingest Time'),
    'pipeline_latency_ms': fields.Float(description='Pipeline Latency (ms)')
})

events_parser = api.parser()
events_parser.add_argument('limit', type=int, help='Maximum number of events to return', location='args')

def get_sensor_for_bin(bin_id):
    mapping = {
        "bin-01": "urn:dev:team05:pir-01"
    }
    return mapping.get(bin_id)


@ns_bins.route("/")
class BinList(Resource):
    def get(self):
        """List all bins"""
        return {"bins": []}, 200


@ns_bins.route("/<string:bin_id>")
class BinItem(Resource):
    def get(self, bin_id):
        """Get details for a specific bin"""
        return {"bin_id": bin_id}, 200


@ns_bins.route("/<string:bin_id>/sensors")
class BinSensors(Resource):
    def get(self, bin_id):
        """List sensors on a specific bin"""
        return {"bin_id": bin_id, "sensors": []}, 200


@ns_bins.route("/<string:bin_id>/events")
class BinEvents(Resource):
    @ns_bins.expect(events_parser)
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
class MqttPublish(Resource):
    def post(self):
        """Publish a message to an MQTT topic"""
        try:
            payload = request.get_json()
            topic = payload.get("topic")
            message = payload.get("message")

            if not topic or message is None:
                return {"error": "Missing topic or message in payload"}, 400

            client = mqtt.Client()
            client.connect("localhost", 1883, keepalive=60)
            client.publish(topic, message)
            client.disconnect()
            return {"message": "Message published"}, 200
        except Exception as e:
            return {"message": str(e)}, 500
        


@ns_mqtt.route("/topics")
class MqttTopics(Resource):
    def get(self):
        """List known MQTT topics and their last retained value"""
        return {"topics": []}, 200


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

