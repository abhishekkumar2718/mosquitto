import time
import random
import os

import paho.mqtt.client as mqtt

class RngProducer(mqtt.Client):
    def __init__(self, pid):
        # Initialize the base class first
        super().__init__()

        self._pid = pid

        self._status_topic = f'status/{self._pid}'
        self._reading_topic = f'random_numbers/{self._pid}'

    def on_connect(self, mqttc, userdata, flags, rc):
        print(f'Connected with result code: {rc}')

        # Once connected, update the status.
        self.set_status('online')

    def blocking_read(self):
        """To simulate an IoT sensor, sleep for five seconds and "read" a random number."""
        time.sleep(5)

        return random.random(0, 50)

    def run(self):
        while True:
            reading = self.blocking_read()

            # It's okay if a few readings get dropped
            self.publish(self._reading_topic, payload=reading, qos=0)

    def set_status(self, status):
        # Use QoS 1 to make sure the message reaches the broker
        self.publish(self._status_topic, payload=status, qos=1)


if __name__ == "__main__":
    producer = RngProducer()

    try:
        # Connect to MQTT broker
        producer.connect("localhost")

        # Create a side-thread to process messages
        producer.loop_start()

        # Wait until connection is established
        while not producer.is_connected():
            time.sleep(0.1)

        producer.run()
    finally:
        # Update the status
        producer.set_status('offline')

        producer.disconnect()
        producer.loop_stop()
