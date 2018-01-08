import json

import time
from paho.mqtt import client as mqtt

from mycroft.util import LOG


class Message(object):

    def __init__(self, type, destination, data=None):
        self.type = type
        self.destination = destination
        self.data = data or {}

    def serialize(self):
        return json.dumps({
            'type': self.type,
            'destination': self.destination,
            'data': self.data
        })

    @staticmethod
    def deserialize(value):
        obj = json.loads(value)
        return Message(
            type=obj.get('type'),
            destination=obj.get('destination'),
            data=obj.get('data')
        )


class Client(object):
    def __init__(self, settings, protocol):
        super(Client, self).__init__()
        self.protocol = protocol

    def connect(self):
        pass

    def disconnect(self):
        pass

    def send(self, message):
        pass

    def receive(self, message):
        pass

    def subscribe(self, topic, handler):
        pass


class HTTPClient(Client):
    pass


class MQTTClient(Client):
    """Client class for interaction over the IoT protocol mqtt
    """

    def __init__(self, settings):
        super(MQTTClient, self).__init__(settings=settings, protocol='mqtt')

        self.ssl = settings.get('mqtt-ssl')
        self.cert = settings.get('mqtt-certificate')
        self.host = settings.get('mqtt-host')
        self.port = settings.get('mqtt-port')
        self.auth = settings.get('mqtt-auth')
        self.user = settings.get('mqtt-username')
        self.password = settings.get('mqtt-password')

        self.registered_handlers = {}
        self.connected = False

        self.client = mqtt.Client('MycroftAI')
        if self.auth:
            self.client.username_pw_set(self.user, self.password)
        if self.ssl:
            self.client.tls_set(self.cert)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def connect(self):
        self.client.connect(self.host, self.port)
        self.client.loop_start()

        while not self.connected:
            time.sleep(0.1)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            LOG.info("MQTT Client connected successfully to host {}"
                     .format(self.host))
            self.connected = True
        else:
            LOG.error("MQTT Client could not connect to host {}"
                      .format(self.host))

    def _on_message(self, client, userdata, message):
        if message.topic in self.registered_handlers:
            format_message = Message(
                type='mqtt',
                destination=str(message.topic).split('/'),
                data=json.loads(str(message.payload))
            )
            self.registered_handlers[message.topic](format_message)
        else:
            LOG.error("No handler was registered for message on topic {}"
                      .format(message.topic))

    def send(self, message):
        dest = '/'.join(message.destination)
        self.client.publish(dest, message.data)

    def receive(self, message):
        pass

    def subscribe(self, topic, handler):
        topic = ','.join(topic)
        self.registered_handlers['topic'] = handler
        self.client.subscribe(topic)


def create_client(protocol, settings):
    """Create the appropriate client for a specified protocol

    Args:
        protocol(str): protocol to be used
        settings(dict): skill settings object containing

    Returns:
        Client: Client object
    """
    if protocol == "mqtt":
        return MQTTClient(settings)
    else:
        LOG.error("Protocol {} not supported".format(protocol))
