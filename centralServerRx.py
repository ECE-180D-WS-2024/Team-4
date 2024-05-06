import paho.mqtt.client as mqtt

# MQTT Broker (replace with your broker's IP address)
broker_address = "localhost"
# MQTT Topic to subscribe to
topic = "float_value"

# List to store client names that are allowed to send data
allowed_clients = []

# Callback function to handle incoming messages
def on_message(client, userdata, message):
    global allowed_clients
    # Convert the message payload from bytes to string
    message_str = message.payload.decode("utf-8")
    if message_str.startswith("REGISTER:"):
        # Register new client
        client_name = message_str.split(":")[1]
        if client_name not in allowed_clients:
            allowed_clients.append(client_name)
            print("Client '{}' registered successfully.".format(client_name))
    elif message_str.startswith("ALLOW:"):
        # Allow client to send data
        client_name = message_str.split(":")[1]
        if client_name in allowed_clients:
            print("Allowing client '{}' to send data.".format(client_name))
        else:
            print("Client '{}' is not registered.".format(client_name))
    else:
        print("Received message from client:", message_str)

# Create MQTT client instance
client = mqtt.Client()
# Assign callback function for when a message is received
client.on_message = on_message
# Connect to MQTT broker
client.connect(broker_address)
# Subscribe to the topic
client.subscribe(topic)
# Loop to listen for incoming messages
client.loop_forever()



