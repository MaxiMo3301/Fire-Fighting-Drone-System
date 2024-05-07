from dronekit import connect, VehicleMode
import time

# Connect to the Vehicle (in this case a UDP endpoint)
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

        # Disarm the Vehicles

        asa_01.armed = False
        asa_11.armed = False

        break

# close the connection of the vehicles

print("The connection test is complete...")
print("Now close the connection with the Vehicles...")

asa_01.close()
asa_11.close()