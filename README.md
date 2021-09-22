# Demonstration of Eclipse Mosquitto

> Source code and slides  for the mid semester seminar submitted for my
> wireless networks course.

MQTT is a client server publish/subscribe messaging transport protocol,
ideal for constrained environments such as for communication in Machine
to Machine (M2M) and Internet of Things (IoT) contexts.

Eclipse Mosquitto is an open source MQTT broker and one of the popular
choices for a broker.

I have built an example application using Mosquitto and Paho's python
client library.

In terms of functionality, I have:
- Created subclasses of `mqtt.Client` - does not seem to be preferred
  way as [official documentation](https://github.com/eclipse/paho.mqtt.python/tree/master/examples) it has only one such example.
- Used `mosquitto_passwd` to manage authentication.
- Used Topics, QoS Levels, Retained Messages and Last Will And Testatement.

For some reason, the auto-generated client ids were not defined - MQTT
specfication specifies that broker must asssign a client id if client id
of zero bytes is sent with CONNECT packet. I need to check if the same
problem when I don't subclass it. One other alternative could be
generate client id on basis of pid (just like topics), and pass it to
the broker.

## Installation

- Install Mosquitto as an application or run it as an docker container (see slides 4-6 for more):
  - [How to Install The Mosquitto MQTT Broker on Linux](http://www.steves-internet-guide.com/install-mosquitto-linux/)
  - [Running the eclipse-mosquitto MQTT Broker in a docker container](https://blog.feabhas.com/2020/02/running-the-eclipse-mosquitto-mqtt-broker-in-a-docker-container/)

- Create a [python virtualenv](https://docs.python.org/3/tutorial/venv.html):

```bash
python3 -m venv pyenv
```

- Activate the virtual environment (the exact command will depend on
  your OS):

```bash
source pyenv/bin/activate
```

- Install the required packages:

```bash
pip install -r requirements.txt
```

- Start the docker container (if not done already):

```bash
docker start mosquitto
```

- Run the producer and consumer scripts:

```bash
python rng_producer.py
```

```bash
python rng_consumer.py
```
