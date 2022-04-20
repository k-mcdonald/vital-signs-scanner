"""
File: Scanner.py

This program connects to a nano33 BLE board and reads vital signs monitor data
from it, then adds it to a file. 

Authors:
    Kevin McDonald
    (Intern) Nico de la Fuente
"""

from pybluez import bluetooth
from datetime import datetime


out_file = "output.log"



def find_device(dev_address=None, dev_name=None):
    """
    Scans for 
    """

    nearby_devices = bluetooth.discover_devices(duration = 20, lookup_names=True, flush_cache=True)

    print(f"({datetime.now()}) Scanning for bluetooth devices:")
    for address, name in nearby_devices:
        print("Name:", name)
        print("Address:", address)

if __name__ == "__main__":
    dev_address = "3e:ea:0f:e8:d0:3f"
    dev_name = "Nano33 with MAXREFDES"

    find_device()