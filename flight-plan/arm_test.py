# https://dronekit-python.readthedocs.io/en/latest/examples/running_examples.html

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Module

from dronekit import connect, VehicleMode
import time
import math
from pymavlink import mavutil

# Connect to Vehicle

print("Connecting to Vehicle: ASA-09")

vehicle = connect('tcp:192.168.1.111:5760', wait_ready = True)

# Heartbeat Counter

hb_counter = vehicle.last_heartbeat

if hb_counter == None:

    print("Can't Connect to the drone: ASA-09")

else:

    print("Successfully connect to the Vehicle: ASA-09")

# Change vehicle to 'GUIDED' Mode

vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

# Confirm vehicle armed

while not vehicle.armed:

    print(" Waiting for arming...")
    time.sleep(1)           