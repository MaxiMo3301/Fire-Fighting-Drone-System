from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to the Vehicle (should use UDP endpoint)

asa_01 = connect('tcp:192.168.1.101:5760')
asa_11 = connect('tcp:192.168.1.111:5760')

# Wait on default attributes to populate

asa_01.wait_ready(True)
asa_11.wait_ready(True)

# Check the heartbeat of the connected drone

print("Asa 01 heartbeat: ", asa_01.last_heartbeat)
print("Asa 11 heartbeat: ", asa_11.last_heartbeat)

# check the mode of the vehicles

print("ASA 01 mode: ",asa_01.mode)
print("ASA 11 mode: ",asa_11.mode)

if asa_01.mode != "STABILIZE":

    asa_01.mode = VehicleMode("STABILIZE")
    print ("ASA 01 updated mode: ",asa_01.mode)


if asa_11.mode != "STABILIZE":

    asa_11.mode = VehicleMode("STABILIZE")
    print ("ASA 11 updated mode: ",asa_11.mode)

while(1):
    if asa_01.mode == "STABILIZE" and asa_11.mode == "STABILIZE":

        # Arm the vehicles

        asa_01.armed = True
        asa_11.armed = True

        time.sleep(5)

        # Take off the Vehicles

        print("Taking Off...")
    
        asa_01.simple_takeoff(10)
        asa_11.simple_takeoff(10)

        time.sleep(20)

        # Set the Vehicle speed 

        asa_01.airspeed = 3
        asa_11.airspeed = 3

        print("Go to mission start")

        point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
        point2 = LocationGlobalRelative(-35.361354, 149.165218, 20)

        # Vehicle1 execute mission

        asa_01.simple_goto(point1)

        # Wait for the first vehicle arrived

        time.sleep(30)

        # Vehicle2 execute mission
        
        asa_11.simple_goto(point2)

        # Wait for the second vehicle arrived

        time.sleep(30)

        # Landing the all the vehicles

        asa_01.mode = VehicleMode("LAND")
        asa_11.mode = VehicleMode("LAND")

        break

# close the connection of the vehicles

print("The connection test is complete...")
print("Now close the connection with the Vehicles...")

asa_01.close()
asa_11.close()