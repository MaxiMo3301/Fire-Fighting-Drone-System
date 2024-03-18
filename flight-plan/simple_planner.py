# https://dronekit-python.readthedocs.io/en/latest/examples/running_examples.html

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Module

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil

# Connect to Vehicle

print("Connecting to Vehicle : ASA-12 ")

vehicle = connect('tcp:192.168.1.5:5760', wait_ready = True)

# Heartbeat Counter

hb_counter = vehicle.last_heartbeat

if hb_counter == None:

    print ("Can't Connect to the drone: ASA-12")

else:

    print("Successfully connect to the drone: ASA-12")

# Relative Location Calculation

def get_location_metres(original_location, dNorth, dEast):

    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned Location has the same `alt` value
    as `original_location`.

    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """

    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))


    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt)

# Calculate Distance between waypoint and ground station

def get_distance_metres(aLocation1, aLocation2):

    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """

    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon

    return math.sqrt( (dlat*dlat) + (dlong*dlong)) * 1.113195e5

# Calculate distance between next point and current waypoint

def distance_to_current_waypoint():

    """
    Gets distance in metres to the current waypoint. 
    It returns None for the first waypoint (Home location).
    """

    nextwatpoint = vehicle.commands.next

    if nextwatpoint == 0:

        return None
    
    missionitem = vehicle.commands[nextwatpoint-1] # commands are zero indexe

    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z

    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)

    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)

    return distancetopoint


# Download the mission from the vehicle

def download_mission():

    cmds = vehicle.commands

    cmds.download()

    cmds.wait_ready() # wait util download is complete.

# Simple Mission Sample 1: Square Mission
    
def adds_square_mission(aLocation, aSize):

    """
    Adds a takeoff command and four waypoint commands to the current mission. 
    The waypoints are positioned to form a square of side length 2*aSize around the specified LocationGlobal (aLocation).

    The function assumes vehicle.commands matches the vehicle mission state 
    (you must have called download at least once in the session and after clearing the mission)
    """	

    cmds = vehicle.commands

    print ("Clear any existing commands...")
    cmds.clear()

    print ("Define / Add new commands...") # Add new commands. The meaning/order of the parameters is documented in the Command class.


    # 1: Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air. (default alt = 10 meters, change the last parameters for different altitude you want)

    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))


    # 2: Define the four MAV_CMD_NAV_WAYPOINT locations and add the commands

    point1 = get_location_metres(aLocation, aSize, -aSize)
    point2 = get_location_metres(aLocation, aSize, aSize)
    point3 = get_location_metres(aLocation, -aSize, aSize)
    point4 = get_location_metres(aLocation, -aSize, -aSize)

    # point 1
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 11))
    
    # point 2
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point2.lat, point2.lon, 12))
    
    # point 3
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point3.lat, point3.lon, 13))
    
    # point 4
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))

    # 3: add dummy waypoint "5" at point 4 (lets us know when have reached destination)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))    

    print(" Upload new commands to vehicle")
    cmds.upload()

# Arms the Vehicle and fly to your target altitude
    
def arm_and_takeoff (aTargetAltitude):

    print ("Basic pre-arm checks...")

    # Confirm the vehicle is ready before you arm the drone

    while not vehicle.is_armable:

        print ("Waiting for vehicle to initialise...")
        time.sleep(1)

    print ("Now arming the motors... ")

    # Change the drone mode to "GUIDED" mode:

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:

        print ("Waiting for arming...")
        time.sleep(1)


    print ("Taking off...")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait for the vehicle reaches a safe hight before processing the next command
    # If not pause, the simple takeoff command will execute immdiately

    while True:

        print ("Altitude: ", vehicle.location.global_relative_frame.alt)

        if vehicle.location.global_relative_frame.alt >= aTargetAltitude*0.95: #Trigger just below target alt

            print ("Reached target altitude...")
            break
    
        time.sleep(1)