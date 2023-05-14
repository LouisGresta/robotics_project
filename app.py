import tkinter.ttk as ttk
import tkinter
import queue
import sys
import math
transfer_queue = queue.Queue(1) # max_size=1, we pass data one by one

message = {
    'mode':'direct',
    'start': False,
    'data': []
           }
transfer_queue.put(message)

class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        legs = ['Leg_1', 'Leg_2', 'Leg_3',
                     'Leg_4', 'Leg_5', 'Leg_6']
        self.legsVar = tkinter.StringVar(value=legs)
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

    def directFrameInit(self):
        self.directFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        armlistDirect = tkinter.Listbox(self.directFrame, height=6, listvariable=self.legsVar)

        motor1Label = ttk.Label(self.directFrame, text="Motor 1 :")
        motor2Label = ttk.Label(self.directFrame, text="Motor 2 :")
        motor3Label = ttk.Label(self.directFrame, text="Motor 3 :")
        
        motor1Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=1.0, to=100.0)
        motor2Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=1.0, to=100.0)
        motor3Scale = ttk.Scale(self.directFrame, orient="horizontal", length=300, from_=1.0, to=100.0)

        armlistDirect.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        motor1Label.grid(row=0, column=1, padx=(0, 10))
        motor2Label.grid(row=1, column=1, padx=(0, 10))
        motor3Label.grid(row=2, column=1, padx=(0, 10))

        motor1Scale.grid(row=0, column=2)
        motor2Scale.grid(row=1, column=2)
        motor3Scale.grid(row=2, column=2)

    def inverseFrameInit(self):
        self.inverseFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        armlistInverse = tkinter.Listbox(self.inverseFrame, height=6, listvariable=self.legsVar)

        xInverseLabel = ttk.Label(self.inverseFrame, text="X :")
        yInverseLabel = ttk.Label(self.inverseFrame, text="Y :")
        zInverseLabel = ttk.Label(self.inverseFrame, text="Z :")
        
        xInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=1.0, to=100.0)
        yInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=1.0, to=100.0)
        zInverseScale = ttk.Scale(self.inverseFrame, orient="horizontal", length=300, from_=1.0, to=100.0)

        armlistInverse.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        xInverseLabel.grid(row=0, column=1, padx=(0, 10))
        yInverseLabel.grid(row=1, column=1, padx=(0, 10))
        zInverseLabel.grid(row=2, column=1, padx=(0, 10))

        xInverseScale.grid(row=0, column=2)
        yInverseScale.grid(row=1, column=2)
        zInverseScale.grid(row=2, column=2)

    def triangleFrameInit(self):
        self.triangleFrame = ttk.Frame(self.notebook, padding=(0,20,0,0))
        armlistTriangle = tkinter.Listbox(self.triangleFrame, height=6, listvariable=self.legsVar)

        xTriangleLabel = ttk.Label(self.triangleFrame, text="X :")
        zTriangleLabel = ttk.Label(self.triangleFrame, text="Z :")
        widthTriangleLabel = ttk.Label(self.triangleFrame, text="Width :")
        heightTriangleLabel = ttk.Label(self.triangleFrame, text="Height :")
        
        xTriangleScale = ttk.Scale(self.triangleFrame, orient="horizontal", length=200, from_=1.0, to=100.0)
        zTriangleScale = ttk.Scale(self.triangleFrame, orient="horizontal", length=200, from_=1.0, to=100.0)
        widthTriangleScale = ttk.Scale(self.triangleFrame, orient="horizontal", length=200, from_=1.0, to=100.0)
        heightTriangleScale = ttk.Scale(self.triangleFrame, orient="vertical", length=100, from_=1.0, to=100.0)

        startStopTriangleButton = ttk.Button(self.triangleFrame, text="Start/Stop")

        armlistTriangle.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        xTriangleLabel.grid(row=0, column=1, padx=(0, 10))
        zTriangleLabel.grid(row=1, column=1, padx=(0, 10))
        widthTriangleLabel.grid(row=2, column=1, padx=(0, 10))
        heightTriangleLabel.grid(row=0, column=3, padx=10, rowspan=3)

        xTriangleScale.grid(row=0, column=2)
        zTriangleScale.grid(row=1, column=2)
        widthTriangleScale.grid(row=2, column=2)
        heightTriangleScale.grid(row=0, column=4, sticky='w', rowspan=3)

        startStopTriangleButton.grid(row=3, column=2, columnspan=5, pady=20)

    def walkFrameInit(self):
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
        directionScale = ttk.Scale(self.walkFrame, orient="horizontal", length=200, from_=-math.pi, to=math.pi)
        piLabel = ttk.Label(self.walkFrame, text="π")

        useArrows = tkinter.BooleanVar(self.walkFrame, value=None)
        arrowsRadioButton = ttk.Radiobutton(self.walkFrame, text="Use It", variable=useArrows, value=True)
        scaleRadioButton = ttk.Radiobutton(self.walkFrame, text="Use It", variable=useArrows, value=False)
        
        startStopWalkButton = ttk.Button(self.walkFrame, text="Start/Stop")

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

        arrowsRadioButton.grid(row=5, column=0, columnspan=5, pady=10)
        scaleRadioButton.grid(row=5, column=7, columnspan=5, pady=10)

        startStopWalkButton.grid(row=6, column=1, columnspan=10, pady=20)

    def on_click(self):
        transfer_queue.put(message)

