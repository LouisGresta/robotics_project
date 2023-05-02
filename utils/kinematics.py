from math import cos, sin, pi, radians, degrees, acos, atan2, sqrt
from utils.constants import *
from utils.verbose_func import printVerbose

def computeDK(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3, use_rads=True):
    if not use_rads :
        theta1 = radians(theta1)
        theta2 = radians(theta2)
        theta3 = radians(theta3)

    theta1 *= THETA1_MOTOR_SIGN 
    theta2 *= THETA2_MOTOR_SIGN 
    theta3 *= THETA3_MOTOR_SIGN 

    theta2 += theta2Correction
    theta3 += theta3Correction
    
    planContribution = l1 + l2*cos(theta2) + l3*cos(theta2 + theta3)

    x = cos(theta1) * planContribution
    y = sin(theta1) * planContribution
    z = l2*sin(theta2) + l3*sin(theta2 + theta3) * Z_DIRECTION

    return [x, y, z]

def computeDKDetailed(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3, use_rads=True):
    if not use_rads :
        theta1 = radians(theta1)
        theta2 = radians(theta2)
        theta3 = radians(theta3)

    theta1 *= THETA1_MOTOR_SIGN 
    theta2 *= THETA2_MOTOR_SIGN 
    theta3 *= THETA3_MOTOR_SIGN 

    theta2 += theta2Correction
    theta3 += theta3Correction

    x1 = l1 * cos(theta1)
    y1 = l1 * sin(theta1)
    z1 = 0

    x2 = (l1 + l2*cos(theta2)) * cos(theta1)
    y2 = (l1 + l2*cos(theta2)) * sin(theta1)
    z2 = l2 * sin(theta2) * Z_DIRECTION

    planContribution = l1 + l2*cos(theta2) + l3*cos(theta2 + theta3)

    x3 = cos(theta1) * planContribution
    y3 = sin(theta1) * planContribution
    z3 = l2*sin(theta2) + l3*sin(theta2 + theta3) * Z_DIRECTION

    return [[0, 0, 0], [x1, y1, z1], [x2, y2, z2], [x3, y3, z3]]

def computeDKSimple(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3, use_rads=True):
    if not use_rads :
        theta1 = radians(theta1)
        theta2 = radians(theta2)
        theta3 = radians(theta3)

    planContribution = l1 + l2*cos(theta2) + l3*cos(theta2 + theta3)

    x = cos(theta1) * planContribution
    y = sin(theta1) * planContribution
    z = l2*sin(theta2) + l3*sin(theta2 + theta3)

    return [x, y, z]

def computeIK(x, y, z, l1=constL1, l2=constL2, l3=constL3, use_rads=True):
    z *= Z_DIRECTION 
    printVerbose("[x = {:.2f}, y = {:.2f}, z = {:.2f}]".format(x, y, z))
    if sqrt(x**2 + y**2 + z**2) > l1+l2+l3:
        printVerbose("point impossible à atteindre")
    d = sqrt(z**2 + (sqrt(x**2+y**2)-l1)**2)
    theta1 = atan2(y, x)
    if (-l3**2 + l2**2 + d**2)/(2*l2*d) > 1 : 
        theta2 = atan2(z,(sqrt(x**2+y**2)-l1)) + ELBOW_SIGN * acos(1)
    elif (-l3**2 + l2**2 + d**2)/(2*l2*d) < -1 :
        theta2 = atan2(z,(sqrt(x**2+y**2)-l1)) + ELBOW_SIGN * acos(-1)
    else :
        theta2 = atan2(z,(sqrt(x**2+y**2)-l1)) + ELBOW_SIGN * acos((-l3**2 + l2**2 + d**2)/(2*l2*d))
    
    if (d**2-l2**2-l3**2)/(2*l2*l3) > 1 : 
        theta3 = -ELBOW_SIGN * acos(1)
    elif (d**2-l2**2-l3**2)/(2*l2*l3) < -1 :
        theta3 = -ELBOW_SIGN * acos(-1)
    else :
        theta3 = -ELBOW_SIGN * acos((d**2-l2**2-l3**2)/(2*l2*l3))
    
    theta2 -= theta2Correction
    theta3 -= theta3Correction

    theta1 *= THETA1_MOTOR_SIGN 
    theta2 *= THETA2_MOTOR_SIGN 
    theta3 *= THETA3_MOTOR_SIGN 

    if not use_rads :
        theta1 = degrees(theta1)
        theta2 = degrees(theta2)
        theta3 = degrees(theta3)
    return [theta1, theta2, theta3]

def computeIKOriented(x, y, z, l1=constL1, l2=constL2, l3=constL3, use_rads=True, leg_index=True, theta_add=0):
    if isinstance(leg_index, bool):
        return computeIK(x, y, z, l1, l2, l3, use_rads)
    x, y, z = rotation_2D(x, y, z, LEG_ANGLES[leg_index] + theta_add)
    x += LEG_X_OFFSET
    y += LEG_Y_OFFSET
    z += LEG_Z_OFFSET
    return computeIK(x, y, z, l1, l2, l3, use_rads)

def circle(x, z, r, t, duration):
    # x, z : position du centre du cercle
    # r : rayon du cercle
    # t : temps de simulation (en secondes)
    # duration : temps (en secondes) pour faire un cercle
    angle = (t*2*pi/duration)
    y = r*cos(angle)
    z = z + r*sin(angle)

    return computeIK(x, y, z)

def triangle(x, z, h, w, t, duration = 3, leg_index=True):
    # x, z : position du centre du segment de la hauteur du triangle
    # (centre du triangle)
    # h : hauteur du triangle
    # w : largeur du triangle
    # t : temps de simulation (en secondes)
    # duration : temps (en secondes) pour tracer le triangle
    dist_cote = sqrt(h**2 + (w/2)**2)
    perimetre = w + dist_cote*2
    duration_width = (w/perimetre)*duration
    duration_hyp = (dist_cote/perimetre)*duration
    t %= duration
    pt_a, pt_b, pt_c = triangle_points(x, z, h, w)

    if t < duration_width :
        printVerbose("segment bas")
        return segment(pt_a[0], pt_a[1], pt_a[2],
                pt_c[0], pt_c[1], pt_c[2],
                t, duration_width, 
                leg_index)
    elif t < (duration_width + duration_hyp) :
        printVerbose("segment droite")
        return segment(pt_c[0], pt_c[1], pt_c[2],
                pt_b[0], pt_b[1], pt_b[2],
                t-duration_width, duration_hyp, 
                leg_index)
    else :
        printVerbose("segment gauche")
        return segment(pt_b[0], pt_b[1], pt_b[2],
                pt_a[0], pt_a[1], pt_a[2],
                t-(duration_width+duration_hyp), duration_hyp, 
                leg_index)

def triangle_synchro(x, z, h, w, t, duration = 3, leg_index=True, theta_add=0):
    # x, z : position du centre du segment de la hauteur du triangle
    # (centre du triangle)
    # h : hauteur du triangle
    # w : largeur du triangle
    # t : temps de simulation (en secondes)
    # duration : temps (en secondes) pour tracer le triangle
    duration_hyp = duration/4
    duration_width = duration/2
    t %= duration
    pt_a, pt_b, pt_c = triangle_points(x, z, h, w)

    if t < duration_width :
        printVerbose("segment bas")
        return segment(pt_a[0], pt_a[1], pt_a[2],
                pt_c[0], pt_c[1], pt_c[2],
                t, duration_width, 
                leg_index, theta_add)
    elif t < (duration_width + duration_hyp) :
        printVerbose("segment droite")
        return segment(pt_c[0], pt_c[1], pt_c[2],
                pt_b[0], pt_b[1], pt_b[2],
                t-duration_width, duration_hyp, 
                leg_index, theta_add)
    else :
        printVerbose("segment gauche")
        return segment(pt_b[0], pt_b[1], pt_b[2],
                pt_a[0], pt_a[1], pt_a[2],
                t-(duration_width+duration_hyp), duration_hyp, 
                leg_index, theta_add)

def triangle_points(x, z, h, w):
    pt_a = (x, 0-w/2, z-h/2)
    pt_b = (x, 0, z+h/2)
    pt_c = (x, 0+w/2, z-h/2)
    return [pt_a, pt_b, pt_c]

def segment(seg_x1, seg_y1, seg_z1,
            seg_x2, seg_y2, seg_z2,
            t, duration, leg_index=True, theta_add=0, loop = False):
    if loop :
        t %= duration
    elif t >= duration :
        return computeIKOriented(seg_x2, seg_y2, seg_z2, leg_index=leg_index, theta_add=theta_add)
    
    x = (t/duration) * (seg_x2 - seg_x1) + seg_x1
    y = (t/duration) * (seg_y2 - seg_y1) + seg_y1
    z = (t/duration) * (seg_z2 - seg_z1) + seg_z1

    return computeIKOriented(x, y, z, leg_index=leg_index, theta_add=theta_add)

def rotation_2D(x, y, z, theta) :
    x_rot = x*cos(theta) - y*sin(theta)
    y_rot = x*sin(theta) + y*cos(theta)
    return [x_rot , y_rot, z]

def main():
    print("Testing the kinematic funtions...")

    # ComputeDKSimple
    print(
        "computeDKSimple(0, 0, 0) = {}".format(
            computeDKSimple(radians(0), radians(0), radians(0), l1=constL1, l2=constL2, l3=constL3)
        )
    )
    print(
        "computeDKSimple(90, 0, 0) = {}".format(
            computeDKSimple(radians(90), radians(0), radians(0), l1=constL1, l2=constL2, l3=constL3)
        )
    )
    print(
        "computeDKSimple(30, 30, 30) = {}".format(
            computeDKSimple(radians(30), radians(30), radians(30), l1=constL1, l2=constL2, l3=constL3)
        )
    )

    # ComputeDK
    print(
        "computeDK(0, 0, 0) = {}".format(
            computeDK(radians(0), radians(0), radians(0), l1=constL1, l2=constL2, l3=constL3)
        )
    )
    print(
        "computeDK(90, 0, 0) = {}".format(
            computeDK(radians(90), radians(0), radians(0), l1=constL1, l2=constL2, l3=constL3)
        )
    )
    print(
        "computeDK(30, 30, 30) = {}".format(
            computeDK(radians(30), radians(30), radians(30), l1=constL1, l2=constL2, l3=constL3)
        )
    )


if __name__ == "__main__":
    main()
