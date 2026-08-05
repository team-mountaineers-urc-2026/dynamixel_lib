#proposed test code for dynamixel_lib, needs reviewed
from dynamixel_lib import Dynamixel, U2D2
from dynamixel_lib import MX106, XL430
import time

def test_motors(motor_id: int):
    #fix this address
    u2d2 = U2D2('/dev/ttyUSB0',9600)
    motor = Dynamixel(MX106,motor_id,u2d2)
    #motor2 = Dynamixel(XL430,motor_id2,u2d2)

    motor.write(MX106.TorqueEnable,0)

    motor.write(MX106.OperatingMode,3)
    motor.write(MX106.TorqueEnable,1)

    motor.write(MX106.GoalPosition,4000)

    time.sleep(2)

    
    result = motor.read(MX106.PresentPosition)

    print(result)

    #time.sleep(10)

    #motor.reboot(motor_id)

    #time.sleep(10)

    #motor.write(XL430.TorqueEnable,0)

    #motor.write(XL430.OperatingMode,3)
    #motor.write(XL430.TorqueEnable,1)

    #motor.write(XL430.GoalPosition,0)
        
    #for x in range(5):
    #    for n in range(300):
    #motor.write(MX106.GoalVelocity,200)
    #if(motor.read(MX106.PresentPosition) != 2048):
    #    motor.write(MX106.GoalPosition,2048)

    #motor.write(MX106.GoalVelocity,0)

    #motor.write(MX106.TorqueEnable,0)
    #motor2.write(XL430.TorqueEnable,0)

test_motors(2)

