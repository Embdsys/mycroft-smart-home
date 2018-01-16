from os.path import dirname, abspath

import sys

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import LOG

sys.path.append(abspath(dirname(__file__)))
create_client = __import__('message_client').create_client
Message = __import__('message_client').Message

__author__ = 'mikonse'


class SmartHomeSkill(MycroftSkill):

    def __init__(self):
        super(SmartHomeSkill, self).__init__(name='Smart Home skill')

        self.protocols = ",".split(self.settings.get('protocols'))
        self.clients = []

        for protocol in self.protocols:
            self.clients.append(create_client(protocol, self.settings))

    def initialize(self):
        self.load_data_files(dirname(__file__))
        self.__build_intents()

        for client in self.clients:
            client.start()

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
        new_message = Message(
            type="",
            destination=destination,
            data=data
        )
        for client in self.clients:
            client.send(new_message)

    def stop(self):
        pass


def create_skill():
    return SmartHomeSkill()
