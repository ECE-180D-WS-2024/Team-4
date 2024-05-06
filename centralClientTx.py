import paho.mqtt.client as mqtt
import random
import time
import velocity

# MQTT Broker (replace with your broker's IP address)
broker_address = "localhost"
# MQTT Topic to publish to
topic = "velocity_value/powerup...."
# Client name
client_name = "player1"  # Change this to a unique name for each client

# Create MQTT client instance
client = mqtt.Client(client_name)
# Connect to MQTT broker
client.connect(broker_address)

# Function to register with the server
def register():
    client.publish(topic, "REGISTER:" + client_name)

# Function to request permission to send data
def request_permission():
    client.publish(topic, "ALLOW:" + client_name)

# Register with the server
register()

while True:
    # Request permission to send data
    request_permission()
    # Generate a random float value
    float_value = random.uniform(0.0, 100.0)
    print("Publishing float value:", float_value)
    # Publish the float value to the topic
    client.publish(topic, str(float_value))
    # Wait for some time before publishing the next value (e.g., every 5 seconds)
    time.sleep(5)
