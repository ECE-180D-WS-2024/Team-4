import numpy as np
import math
import time


#Returns a velocity within the range
#max power angle is pi

#SAMPLE DISPLACEMENT VALUES every 0.01 seconds (time TBD)
#Calculate euclidian distances between 
#Select median value of top 20% of swing (critical for selecting proper velocity)
#Divide by 0.01 to get the velocity value
#Scale to make power between between 0 and pi

#POWER ANGLE IS BETWEEN 0 and MATH.PI

#power = (math.pi - powerAngle) * 5#
#power is 0-90 

m_vel = 0
#Normalize and multiple our velocity by math.pi to properly scale
#norm_vel = velocity / (max)
#if velocity > threshold
def getVelocity():
    global m_vel
    run()
    scaled_velocity = (1-m_vel) * math.pi

    #print(scaled_velocity)
    
    #TESTING
    #scaled_velocity = 0

    return scaled_velocity

def setVelocity(velocity):
    global m_vel
    normalization_factor = 2000
    velocity_int = int(float(velocity))
    norm_vel = velocity_int / normalization_factor

    if(norm_vel <= 0):
        norm_vel = 0
    if(norm_vel >= 1):
        norm_vel = 1
    
    #else normalized value is between 0 and 1
    m_vel = norm_vel

import paho.mqtt.client as mqtt
# Define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/testteam4", qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')


# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
        decoded_payload = message.payload.decode('utf-8')
        input_vel = decoded_payload
        #print(input_vel)
        setVelocity(input_vel)

# Create a client instance.


def run():
        
    client = mqtt.Client()

    # Add additional client options (security, certifications, etc.)
    # Many default options should be good to start off.

    # Add callbacks to the client.
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to a broker using one of the connect*() functions.
    # client.connect_async("test.mosquitto.org")
    client.connect_async('mqtt.eclipseprojects.io')
    # client.connect("test.mosquitto.org", 1883, 60)
    # client.connect("mqtt.eclipse.org")

    # Call one of the loop*() functions to maintain network traffic flow with the broker.
    client.loop_start()
    #client.loop_forever()
    
    
    while True:  # THIS IS WHERE BUTTON LINKING SCRIPT WILL OCCUR, AFTER BUTTON IS RELEASED WE CAN STOP READING
        #DELAY 
        #SEEM TO NEED A DELAY OF 0.5 seconds here to allow for the data to be transmitted
        #perhaps future tests could establish something else
        #print(1)
        #Can i go lower?
        time.sleep(0.5)
        #decoded_payload = message.payload.decode('utf-8')
        break
        
        #pass  # Do your non-blocked other stuff here, like receive IMU data or something.
    # Use subscribe() to subscribe to a topic and receive messages.
    # Use publish() to publish messages to the broker.
    # Use disconnect() to disconnect from the broker.

    client.loop_stop()
    client.disconnect()