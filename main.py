from app import App, transfer_queue
import threading
import time
import pypot.dynamixel

FREQUENCY = 1

ports = pypot.dynamixel.get_available_ports()

dxl_io = pypot.dynamixel.DxlIO(ports[0], baudrate=1000000)

list_ids = dxl_io.scan()
print(list_ids)

start_time = time.time()



#------------------------#
#----- LEGS CONTROL -----#
#------------------------#
dictLegs = {
    'Leg_1':1,
    'Leg_2':2,
    'Leg_3':3,
    'Leg_4':4,
    'Leg_5':5,
    'Leg_6':6
}

def setLegPosition(id_leg, theta1, theta2, theta3):
    dxl_io.set_goal_position({(id_leg*10+1):theta1,
                              (id_leg*10+2):theta2,
                              (id_leg*10+3):theta3})
    
def setMotorPosition(id_motor, theta):
    dxl_io.set_goal_position({id_motor:theta})

def verifConnexionLeg(id_leg):
    return verifConnexionMotor(id_leg*10 + 1) and verifConnexionMotor(id_leg*10 + 2) and verifConnexionMotor(id_leg*10 + 3)

def verifConnexionMotor(id_motor):
    for id in list_ids:
        if( id == id_motor ):
            return True
    return False

#------------------------#



def verificationMessage(message):
        if( len(message["motors"]) == 0):
            print("Aucun moteur renseigné")
            return -1
        
        if( len(message["legs"]) == 0):
            print("Aucune patte renseignée")
            return -2
        
        return 0



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
        print("doing something with", message)

        if( not verificationMessage(message) ):
            print("Movement robot")

            v_motor1 = message["motors"]["motor1"]
            v_motor2 = message["motors"]["motor2"]
            v_motor3 = message["motors"]["motor3"]

            print(f"Motor1 {v_motor1}, motor2 {v_motor2}, motor3 {v_motor3}")

            for leg in message["legs"]:
                id_leg = dictLegs[leg]
                id_theta1 = id_leg*10 + 1
                id_theta2 = id_leg*10 + 2
                id_theta3 = id_leg*10 + 3
                print(f"Leg {id_leg}, pot1 {id_theta1}, pot2 {id_theta2}, pot3 {id_theta3}")
                print(verifConnexionLeg(id_leg))



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