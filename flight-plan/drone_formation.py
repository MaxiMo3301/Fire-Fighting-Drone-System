from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Execute The Simple Goto Function
def drone_go_to(drone_id, pos):

    drone_id.simple_goto(pos)

    time.sleep(30)

    print("delivery success...")    

# Main Function 

if __name__ == "__main__":

    # Connect to the Vehicle 
    # Need to use endpoint other than TCP in our case

    asa_01 = connect('192.168.1.101:14550')
    asa_11 = connect('192.168.1.111:14550')

    # Check the heartbeat of the connected drone

    print("Asa 01 heartbeat: ", asa_01.last_heartbeat)
    print("Asa 11 heartbeat: ", asa_11.last_heartbeat)

    # Send the vehicle to location

    point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
    point2 = LocationGlobalRelative(-35.361354, 149.165218, 20)

    # Send Vehicle 1 to point 1

    drone_go_to(asa_01, point1)

    # Send Vehicle 2 to point 2

    drone_go_to(asa_11, point2)

    """# Send Vehicle 3 to point 3

    drone_go_to(asa_01, point1)

    # Send Vehicle 4 to point 4

    drone_go_to(asa_11, point2)"""

    print("Formation Complete...")

    print("Return to Swarm Mode...")

    # close the connection of the vehicles

    print("Now close the connection with the Vehicles...")

    asa_01.close()
    asa_11.close()
    