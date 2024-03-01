# import DroneKit-Python

#import dronekit
from dronekit import connect, VehicleMode

import time

# Connect to the drone

print("Connecting to vehicle: ASA-01" )
vehicle = connect('tcp:192.168.1.2:5760', wait_ready=True)


# Get some vehicle attributes (state)

print ("Get some vehicle attribute values:")


print (" Last Heartbeat: %s" % vehicle.last_heartbeat)


while 1:

    print ("\nGlobal Location: ")

    print ("lat = ", vehicle.location.global_frame.lat)

    print ("lon = ", vehicle.location.global_frame.lon)

    time.sleep(3)

    print ("\nGlobal Location (relative altitude): ")

    print ("lat = ", vehicle.location.global_relative_frame.lat)

    print ("lat = ", vehicle.location.global_relative_frame.lon)

    time.sleep(3)

    #print ("Local Location: ")    #NED

    #time.sleep(3)

    #print ("Attitude: %s" % vehicle.attitude)

    #time.sleep(1)


# Close vehicle object before exiting script

vehicle.close()

# End of the script
print("Completed")