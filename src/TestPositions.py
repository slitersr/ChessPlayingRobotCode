from time import sleep
from robot import Arm
from robot import Gripper


def main(gripper, arm):
        piece = input("Enter piece(q, k, b, r, n, p): ")
        
        print(piece)
        
        pos_input = input("Enter positions: ")
        
        positions = [ x.strip() for x in pos_input.strip('[]').split(' ') ]
        
        print(positions)
        
        i = 0
        
        total = len(positions)
        
        print(total)
        
        for square in positions:
            if i != total - 1:
                arm.testMove(square)
                gripper.pickup(piece, square)
                arm.testMove(positions[i+1])
                gripper.dropoff(piece, square)
                sleep(2)
                i += 1
                
        
        
# SETUP SCRIPT
gripper = Gripper()
gripper.init()
gripper.calibrate()
            
arm = Arm()
arm.init(gripper)
arm.calibrate()
            
# pass in AX12 object
main(gripper, arm)

