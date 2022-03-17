from Ax12 import Ax12

# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = 'COM3'

Ax12.BAUDRATE = 38400

# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with ID 10 
motor_id = 1
my_dxl = Ax12(motor_id)  
my_dxl.set_moving_speed(200)


def user_input():
    """Check to see if user wants to continue"""
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True


def main(motor_object):
    """ sets goal position based on user input """
    bool_test = True
    while bool_test:
        
        bool_test = user_input()

# pass in AX12 object
main(my_dxl)

# disconnect
my_dxl.set_torque_enable(0)
Ax12.disconnect()