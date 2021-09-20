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
        """To simulate an IoT sensor, "read" a random number."""
        return round(random.uniform(0, 50), 3)

    def run(self):
        while True:
            reading = self.blocking_read()

            print(f'[{self._pid}]: {reading}')

            # It's okay if a few readings get dropped
            self.publish(self._reading_topic, payload=reading, qos=0)

            time.sleep(5)

    def set_status(self, status):
        # Use QoS 1 to make sure the message reaches the broker
        self.publish(self._status_topic, payload=status, qos=1)

        print(f'[{self._pid}]: {status}')


if __name__ == "__main__":
    producer = RngProducer(os.getpid())

    producer.username_pw_set('rng_producer', 'rng_producer')

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
