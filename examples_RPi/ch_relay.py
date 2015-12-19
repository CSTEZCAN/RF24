#!/usr/bin/env python

#  Example using Dynamic Payloads
# 
#  This is an example of how to use payloads of a varying (dynamic) size.
# 
#  TarSens Version for Channel Change and Always ON Reading and Relaying Mode

from __future__ import print_function
import time
from RF24 import *

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/RPi/pyRF24/readme.md

# CE Pin, CSN Pin, SPI Speed

# Setup for GPIO 22 CE and GPIO 25 CSN with SPI Speed @ 1Mhz
#radio = RF24(RPI_V2_GPIO_P1_22, RPI_V2_GPIO_P1_18, BCM2835_SPI_SPEED_1MHZ)

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 4Mhz
#radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_4MHZ)

#RPi B - Works on all boards, flawlessly
# Setup for GPIO 15 CE and CE1 CSN with SPI Speed @ 8Mhz
radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

#RPi B+
# Setup for GPIO 22 CE and CE0 CSN for RPi B+ with SPI Speed @ 8Mhz
#radio = RF24(RPI_BPLUS_GPIO_J8_22, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)

##########################################

radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(15,15)
radio.printDetails()
radio.setChannel(13)
radio.enableDynamicPayloads()
radio.setPALevel(RF24_PA_MAX)
radio.setCRCLength(RF24_CRC_16)
radio.openWritingPipe(0xA1B2C3D4E5)
radio.openReadingPipe(0,0xA1B2C3D4F6)
radio.startListening()
#to test if radio has unique RF24 Chip enable below
#radio.setAutoAck()

#time.sleep helps to reduce cpu usage and power consumption disable if you have time critical relay op
time.sleep(0.05)
while 1:
	if radio.available():
            while radio.available():
                # Fetch the payload, and see if this was the last one.
	            len = radio.getDynamicPayloadSize()
	            receive_payload = radio.read(len)
	            # Spew it and see the data flow
	            print('Got payload size={} value="{}"'.format(len, receive_payload.decode('utf-8')))

            # First, stop listening so we can talk
            radio.stopListening()
            # Second, we have to powercycle the radio so we can open new frequency
            radio.powerdown()
            # Sleepy Radio
            time.sleep(0.01)
            # Fire it up
            radio.powerup()
            radio.enableDynamicPayloads()
            radio.setRetries(15,15)
            # Read from lucky 13 and write to hellish 66
            radio.setChannel(66)
            radio.enableDynamicPayloads()
            radio.setPALevel(RF24_PA_MAX)
            radio.setCRCLength(RF24_CRC_16)
            radio.openWritingPipe(0xA1B2C3D4E5)
            # Send the final one back.
            radio.write(receive_payload)
            #print('Sent response.')
            # Do the power cycle again
            radio.powerdown()
            # Sleepy Radio
            time.sleep(0.01)
            # Fire it up
            radio.powerup()
            radio.enableDynamicPayloads()
            radio.setRetries(15,15)
            # Sweet 13
            radio.setChannel(13)
            # Now, resume listening so we catch the next packets. Listen to the aliens, listen what they say.
            radio.startListening()
