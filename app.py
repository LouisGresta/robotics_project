import tkinter.ttk as ttk
import tkinter
import queue
import math
transfer_queue = queue.Queue(1) # max_size=1, we pass data one by one

MIN_X = -0.4
MIN_Y = -0.4
MIN_Z = -0.4

MAX_X = 0.4
MAX_Y = 0.4
MAX_Z = 0.4

MIN_MOTOR1 = -math.pi
MIN_MOTOR2 = -math.pi
MIN_MOTOR3 = -math.pi

MAX_MOTOR1 = math.pi
MAX_MOTOR2 = math.pi
MAX_MOTOR3 = math.pi

class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.message = {
            "loop":False
        }
        transfer_queue.put(self.message)

        self.legs = ['Leg_1', 'Leg_2', 'Leg_3',
                     'Leg_4', 'Leg_5', 'Leg_6']
        self.legsVar = tkinter.StringVar(value=self.legs)
        self.pack()

        self.notebook = ttk.Notebook(self)

        # Direct Mode
        self.directFrameInit()
        # Inverse Mode
        self.inverseFrameInit()
        # Triangle Mode
        self.triangleFrameInit()
        # Walk Mode
        self.walkFrameInit()
        # BOdyMove Mode
        self.bodyMoveFrameInit()

        # WIP
        rotationFrame = ttk.Frame(self.notebook)

        rotationLabel = ttk.Label(rotationFrame, text="rotation mode (WIP)")

        rotationLabel.pack(padx=5, pady= 5)

        # Add frames
        self.notebook.add(self.directFrame, text="Direct Mode")
        self.notebook.add(self.inverseFrame, text="Inverse Mode")
        self.notebook.add(self.triangleFrame, text="Triangle Mode")
        self.notebook.add(self.walkFrame, text="Walk Mode")
        self.notebook.add(self.bodyMoveFrame, text="Body Move Mode")
        self.notebook.add(rotationFrame, text="Rotation Mode (WIP)")
        
        self.notebook.pack()

        self.notebook.bind("<<NotebookTabChanged>>", self.initMessage)

    def directFrameInit(self):
        self.directFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        self.armlistDirect = tkinter.Listbox(self.directFrame, height=6, listvariable=self.legsVar, selectmode="extended")

        motor1Label = ttk.Label(self.directFrame, text="Motor 1 :")
        motor2Label = ttk.Label(self.directFrame, text="Motor 2 :")
        motor3Label = ttk.Label(self.directFrame, text="Motor 3 :")
        
        motor1Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=MIN_MOTOR1, to=MAX_MOTOR1)
        motor2Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=MIN_MOTOR2, to=MAX_MOTOR2)
        motor3Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=MIN_MOTOR3, to=MAX_MOTOR3)

        self.armlistDirect.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        motor1Label.grid(row=0, column=1, padx=(0, 10))
        motor2Label.grid(row=1, column=1, padx=(0, 10))
        motor3Label.grid(row=2, column=1, padx=(0, 10))

        motor1Scale.grid(row=0, column=2)
        motor2Scale.grid(row=1, column=2)
        motor3Scale.grid(row=2, column=2)

        # Bind
        motor1Scale.configure(command=lambda newValue : self.directMotor(newValue, 1))
        motor2Scale.configure(command=lambda newValue : self.directMotor(newValue, 2))
        motor3Scale.configure(command=lambda newValue : self.directMotor(newValue, 3))

    def inverseFrameInit(self):
        self.inverseFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        self.armlistInverse = tkinter.Listbox(self.inverseFrame, height=6, listvariable=self.legsVar, selectmode="extended")

        xInverseLabel = ttk.Label(self.inverseFrame, text="X :")
        yInverseLabel = ttk.Label(self.inverseFrame, text="Y :")
        zInverseLabel = ttk.Label(self.inverseFrame, text="Z :")
        
        xInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=MIN_X, to=MAX_X)
        yInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=MIN_Y, to=MAX_Y)
        zInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=MIN_Z, to=MAX_Z)

        self.armlistInverse.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        xInverseLabel.grid(row=0, column=1, padx=(0, 10))
        yInverseLabel.grid(row=1, column=1, padx=(0, 10))
        zInverseLabel.grid(row=2, column=1, padx=(0, 10))

        xInverseScale.grid(row=0, column=2)
        yInverseScale.grid(row=1, column=2)
        zInverseScale.grid(row=2, column=2)

        # Bind
        xInverseScale.configure(command=lambda newValue : self.inverseCoords(newValue, "x"))
        yInverseScale.configure(command=lambda newValue : self.inverseCoords(newValue, "y"))
        zInverseScale.configure(command=lambda newValue : self.inverseCoords(newValue, "z"))

    def triangleFrameInit(self):
        self.triangleFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        self.armlistTriangle = tkinter.Listbox(self.triangleFrame, height=6, listvariable=self.legsVar, selectmode="extended")

        xTriangleLabel = ttk.Label(self.triangleFrame, text="X :")
        zTriangleLabel = ttk.Label(self.triangleFrame, text="Z :")
        widthTriangleLabel = ttk.Label(self.triangleFrame, text="Width :")
        heightTriangleLabel = ttk.Label(self.triangleFrame, text="Height :")
        
        xTriangleScale = ttk.Scale(self.triangleFrame, orient="horizontal", length=200, from_=MIN_X, to=MAX_X)
        zTriangleScale = ttk.Scale(self.triangleFrame, orient="horizontal", length=200, from_=MIN_Y, to=MAX_Y)
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
        xTriangleScale.configure(command=lambda newValue : self.triangleParams(newValue, "x"))
        zTriangleScale.configure(command=lambda newValue : self.triangleParams(newValue, "z"))
        widthTriangleScale.configure(command=lambda newValue : self.triangleParams(newValue, "width"))
        heightTriangleScale.configure(command=lambda newValue : self.triangleParams(newValue, "height"))

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

    def bodyMoveFrameInit(self):
        self.bodyMoveFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))

        xBodyMoveLabel = ttk.Label(self.bodyMoveFrame, text="X :")
        yBodyMoveLabel = ttk.Label(self.bodyMoveFrame, text="Y :")
        zBodyMoveLabel = ttk.Label(self.bodyMoveFrame, text="Z :")
        
        xBodyMoveScale = ttk.Scale(self.bodyMoveFrame, orient="horizontal", length=300, from_=MIN_X, to=MAX_X)
        yBodyMoveScale = ttk.Scale(self.bodyMoveFrame, orient="horizontal", length=300, from_=MIN_Y, to=MAX_Y)
        zBodyMoveScale = ttk.Scale(self.bodyMoveFrame, orient="horizontal", length=300, from_=MIN_Z, to=MAX_Z)

        xBodyMoveLabel.grid(row=0, column=1, padx=(0, 10))
        yBodyMoveLabel.grid(row=1, column=1, padx=(0, 10))
        zBodyMoveLabel.grid(row=2, column=1, padx=(0, 10))

        xBodyMoveScale.grid(row=0, column=2)
        yBodyMoveScale.grid(row=1, column=2)
        zBodyMoveScale.grid(row=2, column=2)

        # Bind
        xBodyMoveScale.configure(command=lambda newValue : self.bodyMoveCoords(newValue, "x"))
        yBodyMoveScale.configure(command=lambda newValue : self.bodyMoveCoords(newValue, "y"))
        zBodyMoveScale.configure(command=lambda newValue : self.bodyMoveCoords(newValue, "z"))

    def toggleLoop(self):
        if self.message["loop"]:
            self.message["loop"] = False
        else:
            self.message["loop"] = True
        transfer_queue.put(self.message)

    def walkDirection(self, dir):
        self.message["mode"] = "walk"
        self.message["direction"] = float(dir)

    def directMotor(self, value, motor):
        leg_indexes = self.armlistDirect.curselection()
        legs = []
        for i in leg_indexes:
            legs.append(self.legs[i])
        self.message["motors"]["motor{}".format(motor)] = float(value)
        self.message["legs"] = legs
        transfer_queue.put(self.message)
    
    def inverseCoords(self, value, coord):
        leg_indexes = self.armlistInverse.curselection()
        legs = []
        for i in leg_indexes:
            legs.append(self.legs[i])
        self.message["coords"][coord] = float(value)
        self.message["legs"] = legs
        transfer_queue.put(self.message)

    def triangleParams(self, value, param):
        leg_indexes = self.armlistTriangle.curselection()
        legs = []
        for i in leg_indexes:
            legs.append(self.legs[i])
        self.message["params"][param] = float(value)
        self.message["legs"] = legs

    def bodyMoveCoords(self, value, coord):
        self.message["coords"][coord] = float(value)
        transfer_queue.put(self.message)

    def initMessage(self, event):
        print("mode changed")
        selectedTab = self.notebook.select()
        self.message = {}
        self.message["loop"] = False
        if selectedTab == ".!app.!notebook.!frame":
            self.message["mode"] = "direct"
            self.message["motors"] = {'motor1': 0, 'motor2': 0, 'motor3': 0}
            self.message["legs"] = [] 
        elif selectedTab == ".!app.!notebook.!frame2":
            self.message["mode"] = "inverse"
            self.message["coords"] = {'x': 0, 'y': 0, 'z': 0}
            self.message["legs"] = [] 
        elif selectedTab == ".!app.!notebook.!frame3":
            self.message["mode"] = "triangle"
            self.message["params"] = {'x': 0, 'z': 0, 'width': 0, 'height': 0}
            self.message["legs"] = [] 
        elif selectedTab == ".!app.!notebook.!frame4":
            self.message["mode"] = "walk"
            self.message["direction"] = 0
        elif selectedTab == ".!app.!notebook.!frame5":
            self.message["mode"] = "bodyMove"
            self.message["coords"] = {'x': 0, 'y': 0, 'z': 0}
        print(self.message)
