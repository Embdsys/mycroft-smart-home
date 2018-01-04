# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os.path import dirname

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import LOG

import paho.mqtt.client as mqtt

__author__ = 'mikonse'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.


class MQTTSkill(MycroftSkill):

    def __init__(self):
        super(MQTTSkill, self).__init__(name="MQTTSkill")

        self.protocol = self.config.get("protocol")
        self.ssl = self.config.get("ssl")
        self.cert = self.config.get("certificate")
        self.host = self.config.get("host")
        self.port = self.config.get("port")
        self.auth = self.config.get("auth")
        self.user = self.config.get("username")
        self.password = self.config.get("password")

        if self.protocol == "mqtt":
            self.client = mqtt.Client("MycroftAI")
            if self.auth:
                self.client.username_pw_set(self.user, self.password)
            if self.ssl:
                self.client.tls_set(self.cert)
        else:
            self.client = None

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))
        self.__build_intents()

    def __build_intents(self):
        self.register_entity_file("action.entity")
        self.register_entity_file("command.entity")
        self.register_intent_file("device.action.intent", self.handle_action_intent)

    def handle_action_intent(self, message):
        self.speak("received action intent with message {}".format(message))

        self.client.connect(self.host, self.port)
        self.client.publish("")
        self.client.disconnect()

    def stop(self):
        pass


def create_skill():
    return MQTTSkill()
