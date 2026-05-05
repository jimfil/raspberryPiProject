from flask import Flask, request
from flask_restx import Api, Resource, reqparse, fields
import json
import paho.mqtt.client as mqtt
from apiFunc import load_json,load_events
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


# Request Models
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


# request parser for events endpoint
events_parser = reqparse.RequestParser()
events_parser.add_argument("limit", type=int, default=50, help="Max events to return")
events_parser.add_argument("start", type=str, help="Start datetime (ISO format)")
events_parser.add_argument("end", type=str, help="End datetime (ISO format)")


@ns_bins.route("/")
class BinList(Resource):
    @ns_bins.expect(events_parser)
    @ns_bins.marshal_with(bin_model, as_list=True)
    def get(self):
        """List all bins"""
        return {"bins": []}, 200


@ns_bins.route("/<string:bin_id>")
@ns_bins.param("bin_id", "The bin identifier")
@ns_bins.response(404, "Bin not found")
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
    def get(self, bin_id):
        """Get motion events for a specific bin"""
        return {"bin_id": bin_id, "events": []}, 200


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
    def get(self):
        """List all motion events produced by the pipeline"""
        events = []
        try:
            events = load_events("events.log")
            return {"events": events}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
        


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

