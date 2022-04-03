from ax12 import Ax12
import RPi.GPIO as GPIO
from positions import Positions
from time import sleep

# Create AX12 object for joints with ID 1 and ID 2
joint_1 = Ax12(1) 
joint_2 = Ax12(2)

boardPositions = Positions()

RESTING_HEIGHT = 85

gripper_pin = 38
magnet_pin = 16

class Gripper():
    # Piece Heights
    piece_heights = "{'k': 70, 'q': 70, 'r': 70, 'b': 70, 'k': 70, 'p': 60}"
    
    dict_piece_heights = eval(piece_heights)
    
    def init(self):
        print("Initilaizating gripper...")
        self.previous_z = None
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gripper_pin, GPIO.OUT)
        GPIO.setup(magnet_pin, GPIO.OUT)
        print("Gripper initialization complete!")
        
    def calibrate(self):
        print("Calibrating gripper...")
        self.move(70)
        sleep(1)
        self.move(RESTING_HEIGHT)
        print("Gripper calibration complete!")

        
    def move(self, z):
        z = max(0.0, min(z, 100.0))
        dc = (z * 0.067) + 4.0
        p = GPIO.PWM(gripper_pin, 50.0)
        p.start(dc)
        if self.previous_z is None:
            t = 3.0
        else:
            t = (abs(self.previous_z - z) / 10.0) + .5
        sleep(t)
        p.stop()
        del p
        self.previous_z = z
        
    def electromagnet(self, on):
        output = GPIO.HIGH if on else GPIO.LOW
        GPIO.output(magnet_pin, output)

    def pickup(self, piece, square):
        col = ord(square[0]) - 64 - 1
        row = int(square[1]) - 1
        
        offset = boardPositions.height_offset[row][col]
        piece_height = self.dict_piece_heights[piece] + offset
        
        self.move(piece_height)
        sleep(0.4)
        self.electromagnet(True)
        sleep(0.4)
        self.move(RESTING_HEIGHT)
        sleep(1)

    def dropoff(self, piece, square):
        col = ord(square[0]) - 64 - 1
        row = int(square[1]) - 1
        
        offset = boardPositions.height_offset[row][col]
        piece_height = self.dict_piece_heights[piece] + offset
        
        self.move(piece_height)
        sleep(0.4)
        self.electromagnet(False)
        sleep(0.4)
        self.move(RESTING_HEIGHT)
        sleep(1)

    def cleanup(self):
        GPIO.cleanup()

class Arm:
    gripper = None
    
    def init(self, gripperObj):
        print("Initializating arm control...")
        
        self.gripper = gripperObj
        
        Ax12.DEVICENAME = '/dev/ttyUSB0'
        Ax12.BAUDRATE = 38400

        # sets baudrate and opens com port
        Ax12.connect()

        # Give robot time to connect so we don't get "No status packet" error
        sleep(3)
        print("Arm initialization complete!")
        
    def calibrate(self):
        print("Calibrating arm control...")
        joint_1.set_moving_speed(120)
        joint_2.set_moving_speed(120)

        joint_1.set_moving_speed(120)
        joint_2.set_moving_speed(120)

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
        sleep(4)
        joint_2.set_goal_position(0)

        sleep(2)
        
#         joint_1.set_goal_position(512)
#         sleep(2)
#         joint_2.set_goal_position(512)
# 
#         sleep(2)
# 
#         joint_1.set_goal_position(1023)
#         sleep(2)
#         joint_2.set_goal_position(0)

        print("Arm calibration complete!")

    # BROKEN. Will continue research later
    def degradingMove(self, goalPosition):
        currentPosition = self.get_present_position()

        distance = abs(currentPosition - goalPosition)

        if(goalPosition > currentPosition):
            for count in range(5):
                self.set_goal_position(currentPosition)
                sleep((100-count)/1000)
                currentPosition += 20
            while(currentPosition != goalPosition - 100):
                self.set_goal_position(currentPosition)
                currentPosition += 20
            for count in range(5):
                self.set_goal_position(currentPosition)
                sleep((count-100)/1000)
                currentPosition += 20  
        else:
            for count in range(5):
                self.set_goal_position(currentPosition)
                sleep((100-count)/1000)
                currentPosition -= 20
            while(currentPosition != goalPosition):
                self.set_goal_position(currentPosition)
                currentPosition -= 20
            for count in range(5):
                self.set_goal_position(currentPosition)
                sleep((count-100)/1000)
                currentPosition -= 20

    def move(self, startSquare, finishSquare, piece):
        print(piece)
        col_start = ord(startSquare[0]) - 64 - 1
        row_start = int(startSquare[1]) - 1        

        col_end = ord(finishSquare[0]) - 64 - 1
        row_end = int(finishSquare[1]) - 1

        joint_1.set_goal_position(boardPositions.joint1_table[row_start][col_start])
        sleep(.1)
        joint_2.set_goal_position(boardPositions.joint2_table[row_start][col_start])
        
        # maybe make this according to distance rather than constant time so its more efficient
        sleep(5)
        
        self.gripper.pickup(piece, startSquare)

        joint_1.set_goal_position(boardPositions.joint1_table[row_end][col_end])
        sleep(.1)
        joint_2.set_goal_position(boardPositions.joint2_table[row_end][col_end])
        
        self.gripper.dropoff(piece, finishSquare)
        
    def testMove(self, startSquare):
        col_start = ord(startSquare[0]) - 64 - 1
        row_start = int(startSquare[1]) - 1        

        joint_1.set_goal_position(boardPositions.joint1_table[row_start][col_start])
        sleep(.1)
        joint_2.set_goal_position(boardPositions.joint2_table[row_start][col_start])
        
        sleep(5)

    def remove(self, gripper, sqaure, team):
        col = ord(sqaure[0]) - 64 - 1
        row = int(sqaure[1]) - 1

        joint_1.set_goal_position(boardPositions.joint1_table[row][col])
        sleep(.1)
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

    def dance(self, gripper):
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