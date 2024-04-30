# https://dronekit-python.readthedocs.io/en/latest/examples/running_examples.html

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Module

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil

# Connect to Vehicle

print("Connecting to Vehicle: ASA-11")

vehicle = connect('tcp:192.168.1.111:5760', wait_ready = True)

# Heartbeat Counter

hb_counter = vehicle.last_heartbeat

if hb_counter == None:

    print("Can't Connect to the drone: ASA-11")

else:

    print("Successfully connect to the Vehicle: ASA-11")

# Change vehicle to 'GUIDED' Mode

vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

# Confirm vehicle armed

while not vehicle.armed:

    print(" Waiting for arming...")
    time.sleep(1)

print("Now taking off...")

vehicle.simple_takeoff(10)  # Take off to target altitude

""" 
    Wait until the vehicle reaches a safe height before processing the goto
    (otherwise the command after Vehicle.simple_takeoff will execute
    immediately).
"""

while True:

    print("Altitude: ", vehicle.location.global_relative_frame.alt)

    # Break and return from function just below target altitude.
    if vehicle.location.global_relative_frame.alt >= 10 * 0.95:
        print("Reached target altitude")
        break
    time.sleep(1)

# Setting the modle of the "Landing"
    
print("Now Landing the Drone...")
vehicle.mode = VehicleMode("Landing")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()