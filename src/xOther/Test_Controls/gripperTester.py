import RPi.GPIO as GPIO
from time import sleep
# import chess
# 
gripper_pin = 38
# 
# PIECE_HEIGHTS = {
#     chess.KING: 41,
#     chess.QUEEN: 34,
#     chess.ROOK: 20,
#     chess.BISHOP: 28,
#     chess.KNIGHT: 24,
#     chess.PAWN: 19
# }
# 
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

#     def move(self, z):
#         p = GPIO.PWM(gripper_pin, 50.0)
#         p.start(z)
#         sleep(5)
#         p.stop()
        

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
# 
# while (True):
#     GPIO.output(16, 1)
#     sleep(2)
#     GPIO.output(16, 0)
#     sleep(2)


gripper = Gripper()
gripper.move(70)
sleep(1)
gripper.move(80)
sleep(3)

gripper.move(62)
GPIO.output(16, 1)
sleep(1)
gripper.move(80)
sleep(1)
gripper.move(62)
GPIO.output(16, 0)
sleep(1)
gripper.move(80)






