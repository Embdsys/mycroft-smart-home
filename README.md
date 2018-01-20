# mycroft smart home skill

This skill is designed to communicate with generic IoT devices via different protocols.

A very basic use case would be turning on a led strip by using an ESP8266.

## Example
An example command would be **Turn on the light in the kitchen**. 
This would send a command over all configured protocols to **/light/kitchen** with the data **{"action": "on"}**.

## Usage
The protocols to be used can be configured on mycroft home.

## Current state

Working features:
 - MQTT Client interface fully implemented

TODO:
 - HTTP Client
 - add MQTT subscribe functionality to voice commands
 - context sensitive location
 
## Implementation
Just a standard mycroft skill.
Protocols are implemented in **client.py** subclassing a generic Client class.
This enables multiple protocols to be used at the same time.
