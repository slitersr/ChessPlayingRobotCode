import RPi.GPIO as GPIO
from Ax12 import Ax12
from time import sleep
from pynput import keyboard

class Gripper():
    def __init__(self):
        self.previous_z = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gripper_pin, GPIO.OUT)
        
    def move(self, z):
        z = max(0.0, min(z, 100.0))
        dc = (z * 0.067) + 4.0
        p = GPIO.PWM(gripper_pin, 50.0)
        p.start(dc)
        if self.previous_z is None:
            t = 3.0
        else:
            t = (abs(self.previous_z - z) / 10.0) + 0.5
        sleep(t)
        p.stop()
        del p
        self.previous_z = z

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['up', 'down', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)


def user_input():
    """Check to see if user wants to continue"""
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True


def main(joint_1_object, joint_2_object, gripper):
    bool_loop = True
    while bool_loop:
        
        option = int(input("1. Joint 1 \n2. Joint 2\n3. Actuator \n4. Magnet \n5.  ArrowControl \n6. Exit\n\nEnter: "))
                           
        if option == 1:
            joint1_option = int(input("1. Move \n2. Torque\n3. Position\n4. Back\n\nEnter: "))
            
            if joint1_option == 1:
#                 joint_1_object.set_moving_speed(100)
#                 joint_1_object.print_status("Moving speed of ", joint_1_object.id, joint_1_object.get_moving_speed())

                print("\nPosition of dxl ID: %d is %d " %
                      (joint_1_object.id, joint_1_object.get_present_position()))

                # desired angle input joint 1
                input_pos_1 = int(input("Goal Pos of Joint 1: "))
                joint_1_object.set_goal_position(input_pos_1)
                print("Position of dxl ID: %d is now: %d " %
                      (joint_1_object.id, joint_1_object.get_present_position()))
            elif joint1_option == 2:
                torque_option = int(input("1. On \n2. Off\n\nEnter: "))
                if torque_option == 1:
                    joint_1_object.set_torque_enable(True)
                else:
                    joint_1_object.set_torque_enable(False)
            elif joint1_option == 3:
                print("Position of dxl ID: %d is now: %d " % (joint_2_object.id, joint_2_object.get_present_position()))
                           
        elif option == 2:
            joint2_option = int(input("1. Move \n2. Torque\n3. Position\n4. Back\n\nEnter: "))
            
            if joint2_option == 1:
#                 joint_2_object.set_moving_speed(100)
#                 joint_2_object.print_status("Moving speed of ", joint_2_object.id, joint_2_object.get_moving_speed())

                print("\nPosition of dxl ID: %d is %d " %
                      (joint_2_object.id, joint_2_object.get_present_position()))

                # desired angle input joint 2
                input_pos_2 = int(input("Goal Pos of Joint 2: "))
                joint_2_object.set_goal_position(input_pos_2)
                print("Position of dxl ID: %d is now: %d " % (joint_2_object.id, joint_2_object.get_present_position()))
            elif joint2_option == 2:           
                torque_option = int(input("1. On \n2. Off\n\nEnter: "))
                if torque_option == 1:
                    joint_2_object.set_torque_enable(True)
                else:
                    joint_2_object.set_torque_enable(False)
                
            elif joint2_option == 3:
                print("Position of dxl ID: %d is now: %d " %
                      (joint_2_object.id, joint_2_object.get_present_position()))
                           
        elif option == 3:
            z = int(input("Goal Pos of Actuator: "))
            if(z >= 40 and z <= 85):
                gripper.move(z)
            else:
                print("Too Low!\n")

        elif option == 4:
            activate = int(input("1. On\n2. Off\n\nEnter: "))
            if activate == 1:
                GPIO.output(magnet_pin, 1)
            else:
                GPIO.output(magnet_pin, 0)
                   
        elif option == 5:
            joint_1.set_torque_enable(0)
            joint_2.set_torque_enable(0)
            Ax12.disconnect()
            GPIO.cleanup()
            bool_loop = false

        elif option == 6:
            listener = keyboard.Listener(on_press=on_press)
            listener.start()  # start to listen on a separate thread
            listener.join()  # remove if main thread is polling self.keys

        else:
            print("Incorrect input. Try again")
            
# SETUP SCRIPT
            
# - AX12 SETUP - (joints)
# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyUSB0'

Ax12.BAUDRATE = 38400

# sets baudrate and opens com port
Ax12.connect()

# create AX12 instances with ID 1 and ID 2
joint_1 = Ax12(1) 
joint_2 = Ax12(2)

#  Return Delay = Amount of time it takes for signal to reach servo from arbotix
#  Moving Speed = Rate of turn on joint servos

joint_1.set_return_delay_time(50)
print("Return delay:", joint_1.get_return_delay_time())

joint_1.set_moving_speed(200)
joint_1.print_status("Moving speed of ", joint_1.id, joint_1.get_moving_speed())

joint_2.set_return_delay_time(50)
print("Return delay:", joint_2.get_return_delay_time())

joint_2.set_moving_speed(200)
joint_2.print_status("Moving speed of ", joint_2.id, joint_2.get_moving_speed())

# - GPIO SETUP - (gripper)
gripper_pin = 38
magnet_pin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(gripper_pin, GPIO.OUT)
GPIO.setup(magnet_pin, GPIO.OUT)

gripper = Gripper()
            
# pass in AX12 object
main(joint_1, joint_2, gripper)
 