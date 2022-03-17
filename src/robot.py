from ax12 import Ax12
from positions import Positions
import time

# Create AX12 object for joints with ID 1 and ID 2
joint_1 = Ax12(1) 
joint_2 = Ax12(2)

boardPositions = Positions()

class Robot:
    def initRobot(self):
        print("Setting up robot control...")
        
        Ax12.DEVICENAME = 'COM3'
        Ax12.BAUDRATE = 38400

        # sets baudrate and opens com port
        Ax12.connect()

        # Give robot time to connect so we don't get "No status packet" error
        time.sleep(3)

        joint_1.set_moving_speed(150)
        joint_2.set_moving_speed(150)

        joint_1.set_moving_speed(150)
        joint_2.set_moving_speed(150)

        # Ensure moving speed was set
        joint_1.print_status("Moving speed of ", joint_1.id, joint_1.get_moving_speed())
        joint_2.print_status("Moving speed of ", joint_2.id, joint_2.get_moving_speed())

        # Enable torque
        joint_1.set_torque_enable(1)
        joint_2.set_torque_enable(1)

        # Ensure torque was enabled
        joint_1.print_status("Torque enabled: ", joint_1.id, joint_1.get_torque_enable())
        joint_2.print_status("Torque enabled: ", joint_1.id, joint_1.get_torque_enable())

        # Do complete extension of arms to ensure everything is moving correctly
        joint_1.set_goal_position(1023)
        joint_2.set_goal_position(0)

        time.sleep(2)
        
        joint_1.set_goal_position(512)
        joint_2.set_goal_position(512)

        time.sleep(2)

        joint_1.set_goal_position(1023)
        joint_2.set_goal_position(0)

        print("Robot control setup complete!")

    # BROKEN. Will continue research later
    def degradingMove(self, goalPosition):
        currentPosition = self.get_present_position()

        distance = abs(currentPosition - goalPosition)

        if(goalPosition > currentPosition):
            for count in range(5):
                self.set_goal_position(currentPosition)
                time.sleep((100-count)/1000)
                currentPosition += 20
            while(currentPosition != goalPosition - 100):
                self.set_goal_position(currentPosition)
                currentPosition += 20
            for count in range(5):
                self.set_goal_position(currentPosition)
                time.sleep((count-100)/1000)
                currentPosition += 20  
        else:
            for count in range(5):
                self.set_goal_position(currentPosition)
                time.sleep((100-count)/1000)
                currentPosition -= 20
            while(currentPosition != goalPosition):
                self.set_goal_position(currentPosition)
                currentPosition -= 20
            for count in range(5):
                self.set_goal_position(currentPosition)
                time.sleep((count-100)/1000)
                currentPosition -= 20

    def move(self, startSquare, finishSquare):
        col_start = ord(startSquare[0]) - 64 - 1
        row_start = int(startSquare[1]) - 1

        col_end = ord(finishSquare[0]) - 64 - 1
        row_end = int(finishSquare[1]) - 1

        joint_1.set_goal_position(boardPositions.joint1_table[row_start][col_start])
        time.sleep(.1)
        joint_2.set_goal_position(boardPositions.joint2_table[row_start][col_start])

        # Actuator Down
        # Magnet Engage
        # Actuator Up

        joint_1.set_goal_position(boardPositions.joint1_table[row_end][col_end])
        time.sleep(.1)
        joint_2.set_goal_position(boardPositions.joint2_table[row_end][col_end])

        # dropoff()
        # Actuator Down
        # Magnet Disengage
        # Actuator Up

    def pickup(pieceHeight):       
        print("Not avaliable")
        # PICK UP FUNCTION HERE

    def dropoff(peiceHeight):
        print("Not avaliable")
        # DROP OFF FUNCTION HERE

    def remove(self, sqaure, team):
        col = ord(sqaure[0]) - 64 - 1
        row = int(sqaure[1]) - 1

        joint_1.set_goal_position(boardPositions.joint1_table[row][col])
        time.sleep(.1)
        joint_2.set_goal_position(boardPositions.joint2_table[row][col])

        # COMBINE ALL THIS TO PERFORM PICKUP/DROPOFF

        # Magnet Off

        # Actuator Down

        # Magnet On

        # Actuator On
        
        # MOVE TO TEAM KILLZONE

        # Actuator Down

        # Magnet Off

        # Actuator Up

    def returnHome(self):
        # Ensure Actuator is up
        joint_1.set_goal_position(1023)
        joint_2.set_goal_position(0)

    def dance(self):
        joint_1.set_moving_speed(600)
        joint_2.set_moving_speed(600)

        joint_1.set_goal_position(700)
        joint_2.set_goal_position(400)

        joint_1.set_goal_position(400)
        joint_2.set_goal_position(700)

        joint_1.set_goal_position(700)
        joint_2.set_goal_position(400)

        joint_1.set_goal_position(400)
        joint_2.set_goal_position(700)


    def shutdown(self):
        joint_1.set_torque_enable(0)