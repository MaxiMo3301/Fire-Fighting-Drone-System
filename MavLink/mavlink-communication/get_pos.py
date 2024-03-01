# import module

from pymavlink import mavutil
import time

# start a connection listening to a udp port

the_connection = mavutil.mavlink_connection('tcp:192.168.1.100:5760')


# wait for the first heartbeat
# This sets the system and component ID of remote system for the link

the_connection.wait_heartbeat()

print("Heartbeat from system (system %u component %u)" % 
      (the_connection.target_system, the_connection.target_component))

# Get the position from Mavlink


while 1:
    
    # get the position data from the drone GPS through MavLink
    """local_msg = the_connection.recv_match(
        type='LOCAL_POSITION_NED', blocking=True
    )
    
    print(local_msg)

    time.sleep(3) # Sleep for 3 seconds"""

    global_msg = the_connection.recv_math(
        type='GLOBAL_POSITION_INT', blocking=True
    )

    print(global_msg)

    time.sleep(3) # Sleep for 3 seconds