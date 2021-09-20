import sys

import paho.mqtt.client as mqtt

class RngConsumer(mqtt.Client):
    def __init__(self, client_id=None):
        if client_id:
            super().__init__(client_id=client_id, clean_session=False)
        else:
            super().__init__()

        self._readings = {}
        self._online_producers = set()

    def on_connect(self, mqttc, userdata, flags, rc):
        print(f'Connected with result code: {rc}')

        if rc == 0:
            print(mqttc.client_id)

    def on_message(self, mqttc, userdata, message):
        if message.topic == '$SYS/broker/clients/connected':
            self.handle_clients_connected_message(message)
        elif message.topic.startswith('status'):
            self.handle_status_message(message)
        elif message.topic.startswith('random_numbers'):
            self.handle_random_numbers_message(message)

    def handle_clients_connected_message(self, message):
        print(f'{int(message.payload)} client(s) connected!')

    def handle_status_message(self, message):
        pid = message.topic[7:]
        status = str(message.payload)

        if status == 'online':
            self._online_producers.add(pid)
        else:
            self._online_producers.discard(pid)

        print(f'Online producers: {self._online_producers}')

    def handle_random_numbers_message(self, message):
        pid = message.topic[15:]
        payload = round(float(message.payload), 3)

        if pid not in self._readings:
            self._readings[pid] = []

        self._readings[pid].append(payload)

        average = round(sum(self._readings[pid]) / len(self._readings[pid]), 3)

        print(f'[{pid}]: {payload}, {average}')


if __name__ == "__main__":
    client_id = None
    if len(sys.argv) > 1:
        client_id = sys.argv[1]

    consumer = RngConsumer(client_id)

    consumer.username_pw_set('rng_consumer', 'rng_consumer')

    try:
        consumer.connect("localhost")

        # Subscribe to status of producers with QoS 2
        # as multiple 'disconnect' will try to clear allocated
        # buffer multiple times.
        consumer.subscribe('status/+', qos=2)

        # Subscribe to readings by producer with QoS 0.
        consumer.subscribe('random_numbers/+', qos=0)

        # Subscribe to the special topic - number of clients connected to broker
        consumer.subscribe('$SYS/broker/clients/connected')

        consumer.loop_forever()
    finally:
        consumer.disconnect()
        consumer.loop_stop()
