from app import App, transfer_queue
from utils import computeMessage, dictLegs
from math import degrees

import threading
import time
import pypot.dynamixel


ports = pypot.dynamixel.get_available_ports()

dxl_io = pypot.dynamixel.DxlIO(ports[0], baudrate=1000000)

list_ids = dxl_io.scan()
print(list_ids)


start_time = time.time()


#------------------------#
#----- LEGS CONTROL -----#
#------------------------#
def setLegPosition(id_leg, theta1, theta2, theta3):
    if not verifConnexionLeg(id_leg):
        return False
    dxl_io.set_goal_position({(id_leg*10+1):theta1,
                              (id_leg*10+2):theta2,
                              (id_leg*10+3):theta3})
    return True
    
def setMotorPosition(id_motor, theta):
    if not verifConnexionMotor(id_motor):
        return False
    dxl_io.set_goal_position({id_motor:theta})
    return True

def verifConnexionLeg(id_leg):
    return verifConnexionMotor(id_leg*10 + 1) and verifConnexionMotor(id_leg*10 + 2) and verifConnexionMotor(id_leg*10 + 3)

def verifConnexionMotor(id_motor):
    for id in list_ids:
        if( id == id_motor ):
            return True
    return False

#------------------------#


def robot_exec():
    message = transfer_queue.get()
    while True:
        if not message["loop"]:
            print("wait until loop starts")
            message = transfer_queue.get()
        current_time = time.time() - start_time

        if message is None:
            print("got None, exiting...")
            return
        #print("doing something with", message)
        targets = computeMessage(message, current_time)
        #print(targets)
        for leg in targets:
            id_leg = dictLegs[leg]
            theta1 = degrees(targets[leg][0])
            theta2 = degrees(targets[leg][1])
            theta3 = degrees(targets[leg][2])
            setLegPosition(id_leg, theta1, theta2, theta3)
            motor1 = dxl_io.get_present_position([id_leg*10 + 1])
            motor2 = dxl_io.get_present_position([id_leg*10 + 2])
            motor3 = dxl_io.get_present_position([id_leg*10 + 3])
            print(f"Motor1 {motor1}, motor2 {motor2}, motor3 {motor3}")
        # envoie targets au robot
        time.sleep(0.1)
        
# create the application
app = App()

# method calls to the window manager class<
app.master.title("Hexapod")
app.master.maxsize(1000, 400)

threading.Thread(target=robot_exec).start()
# start the program
app.mainloop()
# stop thread
transfer_queue.put(None)