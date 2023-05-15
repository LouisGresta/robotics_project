#!/usr/bin/env python
import math
import sys
import os
import time
import argparse
import pybullet as p
from onshape_to_robot.simulation import Simulation
import kinematics
from utils import printVerbose
from constants import LEG_ANGLES

# from squaternion import Quaternion
from scipy.spatial.transform import Rotation


def to_pybullet_quaternion(roll, pitch, yaw, degrees=False):
    # q = Quaternion.from_euler(roll, pitch, yaw, degrees=degrees)
    # return [q[1], q[2], q[3], q[0]]

    # Create a rotation object from Euler angles specifying axes of rotation
    rot = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=degrees)

    # Convert to quaternions and print
    rot_quat = rot.as_quat()
    printVerbose(rot_quat)
    return rot_quat


# m_friction
parser = argparse.ArgumentParser()
parser.add_argument("--mode", "-m", type=str, default="direct", help="test")
args = parser.parse_args()
controls = {}
robotPath = "phantomx_description/urdf/phantomx.urdf"
sim = Simulation(robotPath, gui=True, panels=True, useUrdfInertia=False)
# sim.setFloorFrictions(lateral=0, spinning=0, rolling=0)
pos, rpy = sim.getRobotPose()
sim.setRobotPose([0, 0, 0.5], [0, 0, 0, 1])

leg_center_pos = [0.1248, -0.06164, 0.001116 + 0.5]
leg_angle = -math.pi / 4


if args.mode == "frozen-direct":
    crosses = []
    for i in range(4):
        crosses.append(p.loadURDF("target2/robot.urdf"))
    for name in sim.getJoints():
        printVerbose(name)
        if "c1" in name or "thigh" in name or "tibia" in name:
            controls[name] = p.addUserDebugParameter(name, -math.pi, math.pi, 0)
elif args.mode == "direct":
    for name in sim.getJoints():
        printVerbose(name)
        if "c1" in name or "thigh" in name or "tibia" in name:
            controls[name] = p.addUserDebugParameter(name, -math.pi, math.pi, 0)
elif args.mode == "inverse":
    cross = p.loadURDF("target2/robot.urdf")
    alphas = kinematics.computeDK(0, 0, 0, use_rads=True)
    controls["target_x"] = p.addUserDebugParameter("target_x", -0.4, 0.4, alphas[0])
    controls["target_y"] = p.addUserDebugParameter("target_y", -0.4, 0.4, alphas[1])
    controls["target_z"] = p.addUserDebugParameter("target_z", -0.4, 0.4, alphas[2])
elif args.mode == "inverse-oriented":
    cross = p.loadURDF("target2/robot.urdf")
    controls["target_x"] = p.addUserDebugParameter("target_x", -0.4, 0.4, 0)
    controls["target_y"] = p.addUserDebugParameter("target_y", -0.4, 0.4, 0)
    controls["target_z"] = p.addUserDebugParameter("target_z", -0.4, 0.4, 0)
elif args.mode == "triangle":
    controls["triangle_x"] = p.addUserDebugParameter("triangle_x", 0.01, 0.8, 0.1)
    controls["triangle_z"] = p.addUserDebugParameter("triangle_z", -0.2, 0.3, 0)
    controls["triangle_h"] = p.addUserDebugParameter("triangle_h", 0.01, 0.3, 0.1)
    controls["triangle_w"] = p.addUserDebugParameter("triangle_w", 0.01, 0.3, 0.2)
    controls["triangle_duration"] = p.addUserDebugParameter("triangle_duration", 0.01, 10, 3)
elif args.mode == "triangle-oriented":
    controls["triangle_x"] = p.addUserDebugParameter("triangle_x", -0.3, 0.3, 0)
    controls["triangle_z"] = p.addUserDebugParameter("triangle_z", -0.2, 0.3, 0)
    controls["triangle_h"] = p.addUserDebugParameter("triangle_h", 0.01, 0.3, 0.1)
    controls["triangle_w"] = p.addUserDebugParameter("triangle_w", 0.01, 0.3, 0.1)
    controls["triangle_duration"] = p.addUserDebugParameter("triangle_duration", 0.01, 10, 3)
elif args.mode == "walk":
    controls["duration"] = p.addUserDebugParameter("duration", 0.01, 10, 0.5)
    controls["dir_angle"] = p.addUserDebugParameter("dir_angle", -math.pi, math.pi, 0)
elif args.mode == "turnV1":
    controls["duration"] = p.addUserDebugParameter("duration", 0.01, 10, 0.5)
    controls["dir_angle"] = p.addUserDebugParameter("dir_angle", -math.pi, math.pi, 180)


while True:
    targets = {}
    for name in sim.getJoints():
        if "c1" in name or "thigh" in name or "tibia" in name:
            targets[name] = 0
    if args.mode == "frozen-direct":
        for name in controls.keys():
            targets[name] = p.readUserDebugParameter(controls[name])
        points = kinematics.computeDKDetailed(
            targets["j_c1_rf"],
            targets["j_thigh_rf"],
            targets["j_tibia_rf"],
            use_rads=True,
        )
        i = -1
        T = []
        for pt in points:
            # Drawing each step of the DK calculation
            i += 1
            T.append(kinematics.rotation_2D(pt[0], pt[1], pt[2], leg_angle))
            T[-1][0] += leg_center_pos[0]
            T[-1][1] += leg_center_pos[1]
            T[-1][2] += leg_center_pos[2]
            printVerbose("Drawing cross {} at {}".format(i, T))
            p.resetBasePositionAndOrientation(
                crosses[i], T[-1], to_pybullet_quaternion(0, 0, leg_angle)
            )

        # Temp
        sim.setRobotPose([0, 0, 0.5], to_pybullet_quaternion(0, 0, 0))
        # sim.setRobotPose(
        #     leg_center_pos, to_pybullet_quaternion(0, 0, 0),
        # )
        state = sim.setJoints(targets)
    elif args.mode == "direct":
        for name in controls.keys():
            targets[name] = p.readUserDebugParameter(controls[name])
        state = sim.setJoints(targets)
    elif args.mode == "inverse":
        x = p.readUserDebugParameter(controls["target_x"])
        y = p.readUserDebugParameter(controls["target_y"])
        z = p.readUserDebugParameter(controls["target_z"])
        alphas = kinematics.computeIK(x, y, z, use_rads=True)

        dk0 = kinematics.computeDK(0, 0, 0, use_rads=True)
        targets["j_c1_rf"] = alphas[0]
        targets["j_thigh_rf"] = alphas[1]
        targets["j_tibia_rf"] = alphas[2]

        state = sim.setJoints(targets)
        # Temp
        sim.setRobotPose([0, 0, 0.5], [0, 0, 0, 1])

        T = kinematics.rotation_2D(x, y, z, leg_angle)
        T[0] += leg_center_pos[0]
        T[1] += leg_center_pos[1]
        T[2] += leg_center_pos[2]
        printVerbose("Drawing cross at {}".format(T))
        p.resetBasePositionAndOrientation(
            cross, T, to_pybullet_quaternion(0, 0, leg_angle)
        )
    elif args.mode == "triangle":
        x = p.readUserDebugParameter(controls["triangle_x"])
        z = p.readUserDebugParameter(controls["triangle_z"])
        h = p.readUserDebugParameter(controls["triangle_h"])
        w = p.readUserDebugParameter(controls["triangle_w"])
        duration = p.readUserDebugParameter(controls["triangle_duration"])
        alphas = kinematics.triangle(x, z, h, w, sim.t, duration)

        targets["j_c1_rf"] = alphas[0]
        targets["j_thigh_rf"] = alphas[1]
        targets["j_tibia_rf"] = alphas[2]

        state = sim.setJoints(targets)

        # Temp
        sim.setRobotPose([0, 0, 0.5], [0, 0, 0, 1])

        T = kinematics.computeDK(alphas[0], alphas[1], alphas[2])
        T = kinematics.rotation_2D(T[0], T[1], T[2], leg_angle)
        T[0] += leg_center_pos[0]
        T[1] += leg_center_pos[1]
        T[2] += leg_center_pos[2]
        sim.addDebugPosition(T, duration=3)
    elif args.mode == "inverse-oriented":
        x = p.readUserDebugParameter(controls["target_x"])
        y = p.readUserDebugParameter(controls["target_y"])
        z = p.readUserDebugParameter(controls["target_z"])
        alphas = kinematics.computeIKOriented(x, y, z, leg_index=0, use_rads=True)

        dk0 = kinematics.computeDK(0, 0, 0, use_rads=True)
        targets["j_c1_rf"] = alphas[0]
        targets["j_thigh_rf"] = alphas[1]
        targets["j_tibia_rf"] = alphas[2]

        state = sim.setJoints(targets)
        # Temp
        sim.setRobotPose([0, 0, 0.5], [0, 0, 0, 1])

        T = kinematics.computeDK(alphas[0], alphas[1], alphas[2])
        T = kinematics.rotation_2D(T[0], T[1], T[2], leg_angle)
        T[0] += leg_center_pos[0]
        T[1] += leg_center_pos[1]
        T[2] += leg_center_pos[2]

        printVerbose("Drawing cross at {}".format(T))
        p.resetBasePositionAndOrientation(
            cross, T, to_pybullet_quaternion(0, 0, leg_angle)
        )
    elif args.mode == "triangle-oriented":
        x = p.readUserDebugParameter(controls["triangle_x"])
        z = p.readUserDebugParameter(controls["triangle_z"])
        h = p.readUserDebugParameter(controls["triangle_h"])
        w = p.readUserDebugParameter(controls["triangle_w"])
        duration = p.readUserDebugParameter(controls["triangle_duration"])
        alphas = kinematics.triangle(x, z, h, w, sim.t, duration, leg_index=0)

        targets["j_c1_rf"] = alphas[0]
        targets["j_thigh_rf"] = alphas[1]
        targets["j_tibia_rf"] = alphas[2]

        state = sim.setJoints(targets)

        # Temp
        sim.setRobotPose([0, 0, 0.5], [0, 0, 0, 1])

        T = kinematics.computeDK(alphas[0], alphas[1], alphas[2])
        T = kinematics.rotation_2D(T[0], T[1], T[2], leg_angle)
        T[0] += leg_center_pos[0]
        T[1] += leg_center_pos[1]
        T[2] += leg_center_pos[2]
        sim.addDebugPosition(T, duration=3)
    elif args.mode == "walk":
        x = 0
        z = 0.05
        h = 0.05
        w = 0.125
        duration = p.readUserDebugParameter(controls["duration"])
        dir_angle = p.readUserDebugParameter(controls["dir_angle"])

        for key in targets.keys():

            if "rf" in key :
                alphas = kinematics.triangle_synchro(x, z, h, w, sim.t + duration/2, duration, 
                                                     leg_index=0, theta_add= LEG_ANGLES[1])
            if "lf" in key:
                alphas = kinematics.triangle_synchro(x, z, h, w, sim.t, duration, 
                                                     leg_index=1, theta_add= LEG_ANGLES[0])
            if "lm" in key:
                alphas = kinematics.triangle_synchro(x, z, h, w, sim.t + duration/2, duration, 
                                                     leg_index=2, theta_add= LEG_ANGLES[5])
            if "lr" in key:
                alphas = kinematics.triangle_synchro(x, z, h, w, sim.t, duration, 
                                                     leg_index=3, theta_add= LEG_ANGLES[4])
            if "rr" in key:
                alphas = kinematics.triangle_synchro(x, z, h, w, sim.t + duration/2, duration, 
                                                     leg_index=4, theta_add= LEG_ANGLES[3])
            if "rm" in key:
                alphas = kinematics.triangle_synchro(x, z, h, w, sim.t, duration, 
                                                     leg_index=5, theta_add= LEG_ANGLES[2])
            
            if "c1" in key:
                targets[key] = alphas[0]
            if "thigh" in key:
                targets[key] = alphas[1]
            if "tibia" in key:
                targets[key] = alphas[2]

        state = sim.setJoints(targets)

    elif args.mode == "turnV1":

        x = 0
        z = 0.05
        h = 0.05
        w = 0.125
        
        duration = p.readUserDebugParameter(controls["duration"])
        dir_angle = p.readUserDebugParameter(controls["dir_angle"])

        for key in targets.keys():

            if "rf" in key :
                alphas = kinematics.triangle_synchro_turn(x, z, h, w, sim.t + duration/2, duration, 
                                                     leg_index=0, theta_add=LEG_ANGLES[1])
            if "lf" in key:
                alphas = kinematics.triangle_synchro_turn(x, z, h, w, sim.t, duration, 
                                                     leg_index=1, theta_add=LEG_ANGLES[0])
            if "lm" in key:
                alphas = kinematics.triangle_synchro_turn(x, z, h, w, sim.t + duration/2, duration, 
                                                     leg_index=2, theta_add=LEG_ANGLES[5])
            if "lr" in key:
                alphas = kinematics.triangle_synchro_turn(x, z, h, w, sim.t, duration, 
                                                     leg_index=3, theta_add=LEG_ANGLES[4])
            if "rr" in key:
                alphas = kinematics.triangle_synchro_turn(x, z, h, w, sim.t + duration/2, duration, 
                                                     leg_index=4, theta_add=LEG_ANGLES[3])
            if "rm" in key:
                alphas = kinematics.triangle_synchro_turn(x, z, h, w, sim.t, duration, 
                                                     leg_index=5, theta_add=LEG_ANGLES[2])

            if "c1" in key:
                targets[key] = alphas[0]
            if "thigh" in key:
                targets[key] = alphas[1]
            if "tibia" in key:
                targets[key] = alphas[2]

        state = sim.setJoints(targets)

    sim.tick()

