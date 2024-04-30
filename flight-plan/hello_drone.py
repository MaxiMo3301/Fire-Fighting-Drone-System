import dronekit_sitl
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

print("Connection ID = %s", connection_string)

# Import DroneKit-Python
from dronekit import connect, VehicleMode

drone_id = "tcp:192.168.1.111:5760"

# Connect to the Vehicle.
print("Connecting to Vehicle: ASA-11")
vehicle = connect(drone_id, wait_ready=True)

# Get some vehicle attributes (state)
print ("Get some vehicle attribute values:")
print (" GPS: %s" % vehicle.gps_0)
print (" Battery: %s" % vehicle.battery)
print (" Last Heartbeat: %s" % vehicle.last_heartbeat)
print (" Is Armable?: %s" % vehicle.is_armable)
print (" System status: %s" % vehicle.system_status.state)
print (" Mode: %s" % vehicle.mode.name)    # settable

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
print("Completed")