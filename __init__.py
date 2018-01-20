from os.path import dirname, abspath

import sys
import importlib

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

sys.path.append(abspath(dirname(__file__)))

client = importlib.import_module('client')

__author__ = 'mikonse'


class SmartHomeSkill(MycroftSkill):
    def __init__(self):
        super(SmartHomeSkill, self).__init__(name='Smart Home skill')

        if self.settings.get('protocols') == '' or self.settings.get(
                'protocols') is None:
            self.protocols = []
        else:
            self.protocols = \
                str(self.settings.get('protocols', 'mqtt')).split(',')
        self.clients = []

        for protocol in self.protocols:
            self.clients.append(client.create_client(protocol, self.settings))
        LOG.debug(repr(self.clients))

    def initialize(self):
        for c in self.clients:
            c.connect()

    @intent_handler(
        IntentBuilder('DeviceIntent').require('ActionKeyword').require(
            'CommandKeyword').require('ModuleKeyword').optionally(
            'RoomKeyword').build)
    def handle_action_intent(self, message):
        self.speak('received action intent with message {}'
                   .format(message.serialize()))
        data = {
            'action': message.data.get('ActionKeyword')
        }

        destination = [message.data.get('ModuleKeyword')]
        if message.data.get('RoomKeyword') is not None:
            destination.append(message.data.get('RoomKeyword'))

        new_message = client.Message(
            type="",
            destination=destination,
            data=data
        )
        for c in self.clients:
            c.send(new_message)

    def stop(self):
        for c in self.clients:
            c.disconnect()


def create_skill():
    return SmartHomeSkill()
