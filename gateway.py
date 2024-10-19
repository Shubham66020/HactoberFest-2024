import paho.mqtt.client as mqtt
import random
import time

# MQTT Broker settings
BROKER_ADDRESS = "test.mosquitto.org"
BROKER_PORT = 1883

# MQTT Topics for each sensor
TOPIC_TEMPERATURE = "iot/sensor/temperature"
TOPIC_HUMIDITY = "iot/sensor/humidity"
TOPIC_LIGHT = "iot/sensor/light"

# Function to simulate sensor data
def simulate_temperature():
    return round(random.uniform(15.0, 35.0), 2)

def simulate_humidity():
    return round(random.uniform(30.0, 70.0), 2)

def simulate_light_intensity():
    return round(random.uniform(100, 1000), 2)

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message published successfully, ID: {mid}")

# Create the MQTT client
client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the broker
client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# Start the network loop
client.loop_start()

try:
    while True:
        # Simulate sensor readings
        temperature = simulate_temperature()
        humidity = simulate_humidity()
        light_intensity = simulate_light_intensity()

        # Print the sensor data to the console
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Light: {light_intensity} lux")

        # Publish data to corresponding topics
        client.publish(TOPIC_TEMPERATURE, payload=temperature, qos=0, retain=False)
        client.publish(TOPIC_HUMIDITY, payload=humidity, qos=0, retain=False)
        client.publish(TOPIC_LIGHT, payload=light_intensity, qos=0, retain=False)

        # Wait before sending the next set of data
        time.sleep(5)

except KeyboardInterrupt:
    print("MQTT Gateway shutting down...")
finally:
    # Stop the network loop and disconnect from the broker
    client.loop_stop()
    client.disconnect()
