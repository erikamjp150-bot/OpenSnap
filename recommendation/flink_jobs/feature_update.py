# PyFlink real-time feature update job
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import MapFunction
import json
import requests

env = StreamExecutionEnvironment.get_execution_environment()

class FeatureUpdateFunction(MapFunction):
    def map(self, value):
        event = json.loads(value)
        user_id = event['user_id']
        action = event['action']
        content_id = event['content_id']
        
        # Update user features in Hopsworks feature store
        # This is a simplified version; in production, this would batch updates
        feature_payload = {
            "user_id": user_id,
            "feature_group": "user_interactions",
            "features": {
                "last_action": action,
                "last_content_id": content_id,
                "timestamp": event['timestamp']
            }
        }
        
        # POST to Hopsworks feature store API
        # response = requests.post("http://hopsworks-api:8080/features", json=feature_payload)
        
        return {"user_id": user_id, "updated": True}

# Kafka consumer config
kafka_props = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'feature-update-group',
    'auto.offset.reset': 'latest'
}

# Source: Kafka topic 'user_interactions'
stream = env.add_source(
    FlinkKafkaConsumer(
        topics=['user_interactions'],
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )
)

# Process stream
updated_stream = stream.map(FeatureUpdateFunction())

# Sink: log output (in production, store in feature store)
updated_stream.print()

# Execute job
env.execute("Feature Update Pipeline")
