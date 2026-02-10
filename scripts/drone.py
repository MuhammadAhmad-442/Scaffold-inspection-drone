from dronekit_sitl import SITL
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to the vehicle
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

# Arm and takeoff to 5 meters
print("Arming motors...")
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True
while not vehicle.armed:
    time.sleep(1)
print("Vehicle armed!")

print("Taking off...")
vehicle.simple_takeoff(2)  # Take off to 2 meters altitude
while True:
    if vehicle.location.global_relative_frame.alt >= 2 * 0.95:  # Trigger just below target altitude
        print("Reached target altitude")
        break
    time.sleep(1)

# Move the drone slightly forward
print("Moving forward...")
vehicle.velocity[0] = 0.5  # Set forward velocity
time.sleep(2)  # Move forward for 2 seconds
vehicle.velocity[0] = 0  # Stop

# Move the drone slightly backward
print("Moving backward...")
vehicle.velocity[0] = -0.5  # Set backward velocity
time.sleep(2)  # Move backward for 2 seconds
vehicle.velocity[0] = 0  # Stop

# Move the drone slightly left
print("Moving left...")
vehicle.velocity[1] = -0.5  # Set left velocity
time.sleep(2)  # Move left for 2 seconds
vehicle.velocity[1] = 0  # Stop

# Move the drone slightly right
print("Moving right...")
vehicle.velocity[1] = 0.5  # Set right velocity
time.sleep(2)  # Move right for 2 seconds
vehicle.velocity[1] = 0  # Stop

# Move the drone slightly up
print("Moving up...")
vehicle.velocity[2] = 0.5  # Set upward velocity
time.sleep(2)  # Move up for 2 seconds
vehicle.velocity[2] = 0  # Stop

print("Moving down...")
target_altitude = vehicle.location.global_relative_frame.alt - 1  # Descend 1 meter
if target_altitude < 0:  # Ensure we don't go below ground level
    target_altitude = 0
target_location = LocationGlobalRelative(vehicle.location.global_relative_frame.lat, 
                                         vehicle.location.global_relative_frame.lon, 
                                         target_altitude)
vehicle.simple_goto(target_location)
while vehicle.location.global_relative_frame.alt > target_altitude + 0.5:
    time.sleep(1)
vehicle.velocity[2] = 0  # Stop

# Return to Launch (RTL)
print("Returning to Launch (RTL)...")
vehicle.mode = VehicleMode("RTL")
while vehicle.mode.name != "RTL":
    time.sleep(1)
print("RTL command sent.")

# Disarm the vehicle
print("Disarming...")
vehicle.armed = False
while vehicle.armed:
    time.sleep(1)
print("Vehicle disarmed!")

# Close the connection
vehicle.close()

# Shut down SITL
sitl.stop()
