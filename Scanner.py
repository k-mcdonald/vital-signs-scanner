"""
File: Scanner.py

This program connects to a nano33 BLE board and reads vital signs monitor data
from it, then adds it to a file. 

Authors:
    Kevin McDonald
    (Intern) Nico de la Fuente
"""

import asyncio
from bleak import BleakScanner, BleakClient


# To enable debug logging, use the command line and enter:
# $env:BLEAK_LOGGING=1


DEVICE_ADDRESS = "3e:ea:0f:e8:d0:3f"
LOG_FILENAME = "readings.log"

UUID_SERVICE = "13012F00-F8C3-4F4A-A8F4-15CD926DA146"
UUID_HEART = "13012F01-F8C3-4F4A-A8F4-15CD926DA146"
UUID_SPO2 = "13012F02-F8C3-4F4A-A8F4-15CD926DA146"
UUID_TEMP = "13012F03-F8C3-4F4A-A8F4-15CD926DA146"
UUID_TIME = "13012F04-F8C3-4F4A-A8F4-15CD926DA146"

class Reading:
    def __init__(self, heart_rate, blood_oxygen, temperature):
        self.heart_rate = "".join(map(chr, heart_rate))
        self.blood_oxygen = "".join(map(chr, blood_oxygen))
        self.temperature = "".join(map(chr, temperature))

    def log(self, filename):
        file = open(filename, 'a')

        file.write("Heart rate " + self.heart_rate + '\n')
        file.write("Blood oxygen " + self.blood_oxygen + '\n')
        file.write("Temperature " + self.temperature + '\n')

        file.close()


async def darroch_star(address, filename):
    print(f"Trying to connect to {address} >:(") # TODO replace angry face with smiley face
    client = BleakClient(address)
    try:
        connected = await client.connect()
        print("Connected to device!")
        while connected:
            heart_rate = await client.read_gatt_char(UUID_HEART)
            blood_oxygen = await client.read_gatt_char(UUID_SPO2)
            temperature = await client.read_gatt_char(UUID_TEMP)

            reading = Reading(heart_rate, blood_oxygen, temperature)
            reading.log(filename)

            connected = client.is_connected
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

asyncio.run(darroch_star(DEVICE_ADDRESS, LOG_FILENAME))