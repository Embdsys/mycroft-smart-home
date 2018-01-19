from os.path import dirname, abspath

import sys
import importlib
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import LOG

sys.path.append(abspath(dirname(__file__)))

client = importlib.import_module('client')

__author__ = 'mikonse'


class SmartHomeSkill(MycroftSkill):

    def __init__(self):
        super(SmartHomeSkill, self).__init__(name='Smart Home skill')
        
        if self.settings.get('protocols') == '' or self.settings.get('protocols') is None:
            self.protocols = []
        else: 
            self.protocols = str(self.settings.get('protocols', 'mqtt')).split(',')
        self.clients = []
        
        for protocol in self.protocols:
            self.clients.append(client.create_client(protocol, self.settings))
        LOG.debug(repr(self.clients))

    def initialize(self):
        self.load_data_files(dirname(__file__))
        self.__build_intents()

        for c in self.clients:
            c.connect()

    def __build_intents(self):
        self.register_entity_file('action.entity')
        self.register_entity_file('command.entity')
        self.register_entity_file('module.entity')
        self.register_entity_file('room.entity')
        self.register_intent_file(
            'device.action.intent',
            self.handle_action_intent
        )

    def handle_action_intent(self, message):
        self.speak('received action intent with message {}'
                   .format(message.serialize()))
        data = {
            'action': message.data.get('action')
        }
        destination = [message.data.get('module')]
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
