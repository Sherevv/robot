from robot import Robot, RobotOrt, RobotRot

r = Robot()             # Robot create
if not r.is_mark():     # Check if current cell is marked
    r.mark()            # Mark cell
if not r.is_bord('w'):  # Check if border exists in West side
    r.step('w')         # Move to West
print(r.get_tmpr())     # Print temperature in current cell


ro = RobotOrt()         # Create orient robot
if not ro.is_bord():    # Check if border exists in front of robot
    ro.forward()        # Move forward
ro.right()              # Turn robot right
if not ro.is_bord():    # Check if border exists in front of robot
    ro.forward()        # Move forward
print(ro.get_side())    # Print robot orientation


rt = RobotRot()                # Create orient robot
if not rt.is_bord('forward'):  # Check if border exists in front of robot
    rt.forward()               # Move forward
if not rt.is_bord('right'):    # Check if border exists to the right of robot
    rt.rot('r')                # Turn robot right
    rt.forward()               # Move forward
print(ro.get_side())           # Print robot orientation


input()  # to prevent close plot window
