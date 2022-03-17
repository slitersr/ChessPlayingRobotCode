from Ax12 import Ax12

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = 'COM3'

Ax12.BAUDRATE = 38400

# sets baudrate and opens com port
Ax12.connect()

# create AX12300 instance with ID 10 
joint_1 = Ax12(1) 
joint_2 = Ax12(2)  


joint_1.set_return_delay_time(50)
print("Return delay:", joint_1.get_return_delay_time())
#joint_1.set_register2(33, 300)

joint_1.set_moving_speed(100)

joint_1.print_status("Moving speed of ", joint_1.id, joint_1.get_moving_speed())



def user_input():
    """Check to see if user wants to continue"""
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True


def main(joint_1_object, joint_2_object):
    """ sets goal position based on user input """
    bool_test = True
    while bool_test:
        joint_1_object.set_moving_speed(100)
        joint_1_object.print_status("Moving speed of ", joint_1_object.id, joint_1_object.get_moving_speed())

        print("\nPosition of dxl ID: %d is %d " %
              (joint_1_object.id, joint_1_object.get_present_position()))

        # desired angle input joint 1
        input_pos_1 = int(input("goal pos 1: "))
        joint_1_object.set_goal_position(input_pos_1)
        print("Position of dxl ID: %d is now: %d " %
              (joint_1_object.id, joint_1_object.get_present_position()))

        joint_2_object.set_moving_speed(100)
        joint_2_object.print_status("Moving speed of ", joint_2_object.id, joint_2_object.get_moving_speed())

        print("\nPosition of dxl ID: %d is %d " %
              (joint_2_object.id, joint_2_object.get_present_position()))

        # desired angle input joint 2
        input_pos_2 = int(input("goal pos 2: "))
        joint_2_object.set_goal_position(input_pos_2)
        print("Position of dxl ID: %d is now: %d " %
              (joint_2_object.id, joint_2_object.get_present_position()))
        bool_test = user_input()

# pass in AX12 object
main(joint_1, joint_2)

# disconnect
joint_1.set_torque_enable(0)
joint_2.set_torque_enable(0)
Ax12.disconnect()