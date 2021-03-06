import time
import random
import os

import paho.mqtt.client as mqtt

class RngProducer(mqtt.Client):
    def __init__(self, pid):
        # Initialize the base class first
        super().__init__(clean_session=True)

        self._pid = pid

        self._status_topic = f'status/{self._pid}'
        self._reading_topic = f'random_numbers/{self._pid}'

        # Set Last Will And Testament Message
        self.will_set(self._status_topic, 'offline', qos=1, retain=True)

    def on_connect(self, mqttc, userdata, flags, rc):
        print(f'Connected with result code: {rc}')

        if rc == 0:
            # Once connected, update the status.
            self.set_status('online')

            print(mqttc._client_id)

    def blocking_read(self):
        """To simulate an IoT sensor, "read" a random number."""
        return round(random.uniform(0, 50), 3)

    def run(self):
        while True:
            reading = self.blocking_read()

            print(f'[{self._pid}]: {reading}')

            # It's okay if a few readings get dropped
            self.publish(self._reading_topic, payload=reading, qos=0, retain=True)

            time.sleep(5)

    def set_status(self, status):
        # Use QoS 1 to make sure the message reaches the broker
        self.publish(self._status_topic, payload=status, qos=1, retain=True)

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
