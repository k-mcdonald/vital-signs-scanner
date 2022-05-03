"""
File: Scanner.py

This program connects to a nano33 BLE board and reads vital signs monitor data
from it, then adds it to a file. 

Authors:
    Kevin McDonald
    (Intern) Nico de la Fuente
"""
from time import localtime, strftime
from asyncio import run, sleep
from bleak import BleakClient, BleakError


# To enable debug logging, use the command line and enter:
# $env:BLEAK_LOGGING=1


DEVICE_ADDRESS = "3e:ea:0f:e8:d0:3f"
LOG_FILENAME = "C:\\Users\\LattePanda\\Desktop\\Readings\\readings.log"  #C:\\Users\\LattePanda\\Desktop\\Readings\\

UUID_SERVICE = "13012F00-F8C3-4F4A-A8F4-15CD926DA146"
UUID_HEART = "13012F01-F8C3-4F4A-A8F4-15CD926DA146"
UUID_SPO2 = "13012F02-F8C3-4F4A-A8F4-15CD926DA146"
UUID_TEMP = "13012F03-F8C3-4F4A-A8F4-15CD926DA146"
#UUID_TIME = "13012F04-F8C3-4F4A-A8F4-15CD926DA146"
TIME_FORMAT_STR = "%H:%M:%S"

class Reading:
    def __init__(self, heart_rate, blood_oxygen, temperature, time=None):
        self.heart_rate = self.data_to_str(heart_rate)
        self.blood_oxygen = self.data_to_str(blood_oxygen)
        self.temperature = self.data_to_str(temperature)
        self.time = self.get_time() if time is None else None
        
    def data_to_str(self, byte_array):
        return "".join(map(chr, byte_array))
    
    def get_time(self):
        return strftime(TIME_FORMAT_STR, localtime())

    def log(self, filename):
        file = open(filename, 'a')
        file.write("Heart rate " + self.heart_rate +",")
        file.write(" Blood oxygen " + self.blood_oxygen + ",")
        file.write(" Temperature " + self.temperature + ",")
        file.write(" Time: " + self.time + "\n")
        file.close()

class MyBleak(BleakClient):
    def connect(self, timeout=10.0):
        coroutine = super().connect(timeout=timeout)
        return run(coroutine)
    
    def read_all_gatt_chars(self):
        pass
    def read_gatt_char(self, char_specifier):
        coroutine = super().read_gatt_char(char_specifier)
        data = run(coroutine)
        return "".join(map(chr, data))
    

    
class DarrochStar:
    def __init__(self, address):
        self.client = BleakClient(address)
        self.client.set_disconnected_callback(self.disconnect_cb)

        print(f"Trying to connect to {address} >:(")
        self.connect()

        self.loop()
    
    def connect(self, retry=False):
        while retry:
            try:
                run(self.client.connect(timeout=1.0))
                print("Connected to device :D")
                break
            except BleakError as e:
                print("Could not connect to device :C")
                print(e)
    
    def disconnect_cb(client: BleakClient):
        """
        Callback function for unexpected disconnect event
        """

        print(f"Client with address {client.address} got disconnected!")
        print("Attempting to reconnect")

        DarrochStar.reconnect(client.address)

    def reconnect(self, address):
        # Reinitialize DarrochStar
        self.__init__(address)

    def loop(self):
        while self.client.is_connected:
            heart_rate = self.client.read_gatt_char(UUID_HEART)
            blood_oxygen = self.client.read_gatt_char(UUID_SPO2)
            temperature = self.client.read_gatt_char(UUID_TEMP)

            reading = Reading(heart_rate, blood_oxygen, temperature)
            reading.log(LOG_FILENAME)
            run(sleep(5))

            connected = self.client.is_connected
        self.reconnect(self.client.address)

if __name__ == "__main__":
    DarrochStar(DEVICE_ADDRESS)
