import json 
import time
import pypot.dynamixel as dyn
import argparse
import utils.kinematics as kinematics
from utils.verbose_func import printVerbose
from pynput import keyboard

def get_motor_id(motor:str):
    return data["motors"][motor]["id"]

# ----------------- INIT -----------------

# get datas from json
with open("robotConfig.json", "r") as read_file:
    data = json.load(read_file)

attached_motors = data["controllers"]["dxl_controller_0"]["attached_motors"]
port = data["controllers"]["dxl_controller_0"]["port"]

# set communication with robot
if port == "auto":
    port = dyn.get_available_ports()[0]
printVerbose(port)
dxl_io = dyn.DxlIO(port, baudrate=1000000)

# get arguments
parser = argparse.ArgumentParser()
parser.add_argument("--mode", "-m", type=str, default="direct", help="test")
args = parser.parse_args()

t0 = time.time()
dxl_io.set_goal_position({11:0, 12:0, 13:0})
dxl_io.disable_torque([11, 12, 13])
while True:
    t = time.time() - t0
    # execute choosen mode
    if args.mode == "direct":
        alphas = dxl_io.get_present_position([get_motor_id("motor_11"), 
                                              get_motor_id("motor_12"),
                                              get_motor_id("motor_13")])
        points = kinematics.computeDKDetailed(alphas[0],
                                              alphas[1],
                                              alphas[2],
                                              use_rads=False
                                              )
        printVerbose("motor_11 : {:.3f}, motor_12 : {:.3f}, motor_13 : {:.3f}"
                     .format(alphas[0], alphas[1], alphas[2]))
        for point in points:
            printVerbose("x : {:.3f}, y : {:.3f}, z : {:.3f}"
                            .format(point[0], point[1], point[2]))
    printVerbose("time : {:.3f}".format(t))