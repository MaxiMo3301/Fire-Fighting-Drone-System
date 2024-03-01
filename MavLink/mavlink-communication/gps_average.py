# import DroneKit-Python

from dronekit import connect, VehicleMode

import time

# Connect to the drone

print ("Connecting to vehicle: ASA-12")
vehicle = connect('tcp:192.168.1.4:5760', wait_ready=True)


# Global Varible

flag = 0
glo_lat = 0.0
glo_lon = 0.0
glo_total_lat = 0.0
glo_total_lon = 0.0

# Heartbeat Counter

counter = vehicle.last_heartbeat

if counter == None:

    print("Can't Connect to the drone: ASA-012")

else:

    print (" Last Heartbeat: %s" % vehicle.last_heartbeat)

    while 1:

        flag = flag + 1

        print ("\nData Set: ", flag)

        glo_lat = vehicle.location.global_frame.lat

        glo_lon = vehicle.location.global_frame.lon

        glo_total_lat = glo_total_lat + glo_lat

        glo_total_lon = glo_total_lon + glo_lon

        if flag >= 100:

            div = flag

            av_glo_lat = glo_total_lat / div
            av_glo_lon = glo_total_lon / div

            print ("\nGlobal Location: ")
            print ("lat = ", glo_lat)
            print ("lon = ", glo_lon)

            print ("\nAverage Global Location: ")
            print ("lat = ", av_glo_lat)
            print ("lon = ", av_glo_lon)

            time.sleep(2)
# Close vehicle object before exiting script

vehicle.close()

# End of the script
print("Completed")