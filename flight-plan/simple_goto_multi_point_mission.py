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

# Function for Arming the drone and takeoff
    
def Arm_and_Takeoff(aTargetAltitude):

    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Check if the drone is ready to arm")

    # Don't try to arm until autopilot is ready
    
    while not vehicle.is_armable:

        print("Wating for vhhicle to initialise... ")
        time.sleep(1)

    print("Now arming motors...")

    # Change vehicle to 'GUIDED' Mode

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off

    while not vehicle.armed:

        print(" Waiting for arming...")
        time.sleep(1)

    print("Now taking off...")

    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    """ Wait until the vehicle reaches a safe height before processing the goto
        (otherwise the command after Vehicle.simple_takeoff will execute
        immediately).
    """

    while True:

        print("Altitude: ", vehicle.location.global_relative_frame.alt)

        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Main Function To Execute The Whole Mission

if __name__ == "__main__":

    Arm_and_Takeoff(10)

    # setting the default airspeed

    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3

    # Go to 1st point

    print("Going towards first point for 30 seconds ...")
    point1 = LocationGlobalRelative(-35.361354, 149.165218, 10)
    vehicle.simple_goto(point1)

    # set mission delay
    time.sleep(30)

    # Go to 2nd point

    print("Going towards second point for 30 seconds ...")
    point2 = LocationGlobalRelative(-35.361354, 149.165218, 10)
    vehicle.simple_goto(point2)

    # set mission delay
    time.sleep(30)

    # Setting the modle of the "Landing"
    
    print("Now Landing the Drone...")
    vehicle.mode = VehicleMode("Landing")

    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()

    # End Of The Mission