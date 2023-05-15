import tkinter.ttk as ttk
import tkinter
import queue
import math
import time

from kinematics import *

transfer_queue = queue.Queue(1) # max_size=1, we pass data one by one

message = {
    'mode':'direct',
    'loop': False,
    'data': {}
           }
transfer_queue.put(message)

class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.legs = ['Leg_1', 'Leg_2', 'Leg_3',
                     'Leg_4', 'Leg_5', 'Leg_6']
        self.legsVar = tkinter.StringVar(value=self.legs)
        self.pack()

        self.start_time = time.time_ns()

        self.notebook = ttk.Notebook(self)

        # Direct Mode
        self.directFrameInit()
        # Inverse Mode
        self.inverseFrameInit()
        # Triangle Mode
        self.triangleFrameInit()
        # Walk Mode
        self.walkFrameInit()

        # WIP
        bodyMoveFrame = ttk.Frame(self.notebook)
        rotationFrame = ttk.Frame(self.notebook)

        bodyMoveLabel = ttk.Label(bodyMoveFrame, text="body move mode (WIP)")
        rotationLabel = ttk.Label(rotationFrame, text="rotation mode (WIP)")

        bodyMoveLabel.pack(padx=5, pady= 5)
        rotationLabel.pack(padx=5, pady= 5)

        # Add frames
        self.notebook.add(self.directFrame, text="Direct Mode")
        self.notebook.add(self.inverseFrame, text="Inverse Mode")
        self.notebook.add(self.triangleFrame, text="Triangle Mode")
        self.notebook.add(self.walkFrame, text="Walk Mode")
        self.notebook.add(bodyMoveFrame, text="Body Move Mode (WIP)")
        self.notebook.add(rotationFrame, text="Rotation Mode (WIP)")
        
        self.notebook.pack()

        self.notebook.bind("<<NotebookTabChanged>>", self.initMessage)

    def directFrameInit(self):
        self.directFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        self.armlistDirect = tkinter.Listbox(self.directFrame, height=6, listvariable=self.legsVar, selectmode="extended")

        motor1Label = ttk.Label(self.directFrame, text="Motor 1 :")
        motor2Label = ttk.Label(self.directFrame, text="Motor 2 :")
        motor3Label = ttk.Label(self.directFrame, text="Motor 3 :")
        
        motor1Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=1.0, to=100.0)
        motor2Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=1.0, to=100.0)
        motor3Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=1.0, to=100.0)

        self.armlistDirect.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        motor1Label.grid(row=0, column=1, padx=(0, 10))
        motor2Label.grid(row=1, column=1, padx=(0, 10))
        motor3Label.grid(row=2, column=1, padx=(0, 10))

        motor1Scale.grid(row=0, column=2)
        motor2Scale.grid(row=1, column=2)
        motor3Scale.grid(row=2, column=2)

        # Bind
        motor1Scale.configure(command=lambda newvalue : self.directMotor(newvalue, 1))
        motor2Scale.configure(command=lambda newvalue : self.directMotor(newvalue, 2))
        motor3Scale.configure(command=lambda newvalue : self.directMotor(newvalue, 3))

    def inverseFrameInit(self):
        self.inverseFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        self.armlistInverse = tkinter.Listbox(self.inverseFrame, height=6, listvariable=self.legsVar, selectmode="extended")

        xInverseLabel = ttk.Label(self.inverseFrame, text="X :")
        yInverseLabel = ttk.Label(self.inverseFrame, text="Y :")
        zInverseLabel = ttk.Label(self.inverseFrame, text="Z :")
        
        xInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=1.0, to=100.0)
        yInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=1.0, to=100.0)
        zInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=1.0, to=100.0)

        self.armlistInverse.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        xInverseLabel.grid(row=0, column=1, padx=(0, 10))
        yInverseLabel.grid(row=1, column=1, padx=(0, 10))
        zInverseLabel.grid(row=2, column=1, padx=(0, 10))

        xInverseScale.grid(row=0, column=2)
        yInverseScale.grid(row=1, column=2)
        zInverseScale.grid(row=2, column=2)

        # Bind
        xInverseScale.configure(command=lambda newvalue : self.inverseCoords(newvalue, "x"))
        yInverseScale.configure(command=lambda newvalue : self.inverseCoords(newvalue, "y"))
        zInverseScale.configure(command=lambda newvalue : self.inverseCoords(newvalue, "z"))

    def triangleFrameInit(self):
        self.triangleFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        self.armlistTriangle = tkinter.Listbox(self.triangleFrame, height=6, listvariable=self.legsVar, selectmode="extended")

        xTriangleLabel = ttk.Label(self.triangleFrame, text="X :")
        zTriangleLabel = ttk.Label(self.triangleFrame, text="Z :")
        widthTriangleLabel = ttk.Label(self.triangleFrame, text="Width :")
        heightTriangleLabel = ttk.Label(self.triangleFrame, text="Height :")
        
        xTriangleScale = ttk.Scale(self.triangleFrame, orient="horizontal", length=200, from_=1.0, to=100.0)
        zTriangleScale = ttk.Scale(self.triangleFrame, orient="horizontal", length=200, from_=1.0, to=100.0)
        widthTriangleScale = ttk.Scale(self.triangleFrame, orient="horizontal", length=200, from_=1.0, to=100.0)
        heightTriangleScale = ttk.Scale(self.triangleFrame, orient="vertical", length=100, from_=1.0, to=100.0)

        startStopTriangleButton = ttk.Button(self.triangleFrame, text="Start/Stop")

        self.armlistTriangle.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        xTriangleLabel.grid(row=0, column=1, padx=(0, 10))
        zTriangleLabel.grid(row=1, column=1, padx=(0, 10))
        widthTriangleLabel.grid(row=2, column=1, padx=(0, 10))
        heightTriangleLabel.grid(row=0, column=3, padx=10, rowspan=3)

        xTriangleScale.grid(row=0, column=2)
        zTriangleScale.grid(row=1, column=2)
        widthTriangleScale.grid(row=2, column=2)
        heightTriangleScale.grid(row=0, column=4, sticky='w', rowspan=3)

        startStopTriangleButton.grid(row=3, column=2, columnspan=5, pady=20)

        # Bind
        startStopTriangleButton.configure(command=self.toggleLoop)
        xTriangleScale.configure(command=lambda newvalue : self.triangleParams(newvalue, "x"))
        zTriangleScale.configure(command=lambda newvalue : self.triangleParams(newvalue, "z"))
        widthTriangleScale.configure(command=lambda newvalue : self.triangleParams(newvalue, "width"))
        heightTriangleScale.configure(command=lambda newvalue : self.triangleParams(newvalue, "height"))

    def walkFrameInit(self):
        # Init
        self.walkFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))

        nordButton = ttk.Button(self.walkFrame, text="↑")
        nordEastButton = ttk.Button(self.walkFrame, text="↗")
        eastButton = ttk.Button(self.walkFrame, text="→")
        southEastButton = ttk.Button(self.walkFrame, text="↘")
        southButton = ttk.Button(self.walkFrame, text="↓")
        southWestButton = ttk.Button(self.walkFrame, text="↙")
        westButton = ttk.Button(self.walkFrame, text="←")
        nordWestButton = ttk.Button(self.walkFrame, text="↖")

        minusPiLabel = ttk.Label(self.walkFrame, text="-π")
        directionScale = ttk.Scale(self.walkFrame, orient="horizontal", length=200, from_=-math.pi, to=math.pi, value=0)
        piLabel = ttk.Label(self.walkFrame, text="π")

        startStopWalkButton = ttk.Button(self.walkFrame, text="Start/Stop")

        # Position
        nordButton.grid(row=0,column=2)
        nordEastButton.grid(row=1, column=3)
        eastButton.grid(row=2, column=4)
        southEastButton.grid(row=3, column=3)
        southButton.grid(row=4, column=2)
        southWestButton.grid(row=3, column=1)
        westButton.grid(row=2, column=0)
        nordWestButton.grid(row=1, column=1)

        ttk.Separator(self.walkFrame, orient="vertical").grid(row=0, column=5, sticky="ns", rowspan=5, padx=30)

        minusPiLabel.grid(row=0, column=6, rowspan=5)
        directionScale.grid(row=0, column=7, rowspan=5)
        piLabel.grid(row=0, column=8, rowspan=5)

        startStopWalkButton.grid(row=6, column=1, columnspan=10, pady=20)

        # Bind
        startStopWalkButton.configure(command=self.toggleLoop)
        nordButton.configure(command=lambda : self.walkDirection(0))
        nordEastButton.configure(command=lambda : self.walkDirection(-math.pi/4))
        eastButton.configure(command=lambda : self.walkDirection(-math.pi/2))
        southEastButton.configure(command=lambda : self.walkDirection(-3*math.pi/4))
        southButton.configure(command=lambda : self.walkDirection(math.pi))
        southWestButton.configure(command=lambda : self.walkDirection(3*math.pi/4))
        westButton.configure(command=lambda : self.walkDirection(math.pi/2))
        nordWestButton.configure(command=lambda : self.walkDirection(math.pi/4))
        directionScale.configure(command=self.walkDirection)

    def toggleLoop(self):
        if message["loop"]:
            message["loop"] = False
        else:
            message["loop"] = True
        transfer_queue.put(message)

    def walkDirection(self, dir):
        message["mode"] = "walk"
        message["data"]["direction"] = dir


    def writeMessage(self, theta, motor, leg_indexes, mode, loop=False):
        legs = []
        for i in leg_indexes:
            legs.append(self.legs[i])
        message["data"]["motor{}".format(motor)] = theta
        message["data"]["legs"] = legs
        message["mode"] = mode
        message["loop"] = loop


    # Direct kinematic movement for one motor
    def directMotor(self, value, motor):
        leg_indexes = self.armlistDirect.curselection()

        theta = value

        self.writeMessage(theta, motor, leg_indexes, mode="Direct")

        transfer_queue.put(message)
    

    # Inverse kinematic movement
    def inverseCoords(self, value):
        leg_indexes = self.armlistInverse.curselection()

        thetas = computeIK(value[0], value[1], value[2])

        for i in range(3):
            self.writeMessage(thetas[i], i, leg_indexes, mode="Inverse")
            transfer_queue.put(message)



    def triangleParams(self, value):
        leg_indexes = self.armlistInverse.curselection()

        thetas = triangle(value[0], value[1], value[2],
                          self.start_time - time.time_ns())

        for i in range(3):
            self.writeMessage(thetas[i], i, leg_indexes, mode="Triangle", loop=True)
            transfer_queue.put(message)


    def initMessage(self, event):
        print("tab changed")
        selectedTab = self.notebook.select()
        print(selectedTab)
        message = {}
        message["loop"] = False
        if selectedTab == ".!app.!notebook.!frame":
            message["mode"] = "direct"
            message["motors"] = {'motor1': 0, 'motor2': 0, 'motor3': 0}
            message["legs"] = [] 
        elif selectedTab == ".!app.!notebook.!frame2":
            message["mode"] = "inverse"
            message["coords"] = {'x': 0, 'y': 0, 'z': 0}
            message["legs"] = [] 
        elif selectedTab == ".!app.!notebook.!frame3":
            message["mode"] = "triangle"
            message["params"] = {'x': 0, 'z': 0, 'width': 0, 'height': 0}
            message["legs"] = [] 
        elif selectedTab == ".!app.!notebook.!frame4":
            message["mode"] = "walk"
            message["direction"] = 0
        print(message)
