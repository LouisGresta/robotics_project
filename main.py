from app import App, transfer_queue
import threading
import time
from utils import readMessage
start_time = time.time_ns()

def robot_exec():
    message = transfer_queue.get()
    while True:
        if not message["loop"]:
            print("wait until loop starts")
            message = transfer_queue.get()
        current_time = time.time_ns() - start_time

        if message is None:
            print("got None, exiting...")
            return
        print("doing something with", message)


# create the application
app = App()

# method calls to the window manager class
app.master.title("Hexapod")
app.master.maxsize(1000, 400)

threading.Thread(target=robot_exec).start()
# start the program
app.mainloop()
# stop thread
transfer_queue.put(None)