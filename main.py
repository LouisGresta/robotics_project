from app import App, transfer_queue
import threading
import time
import sys 

def robot_exec():
    while True:
        message = transfer_queue.get()
        if message is None:
            print("thread_target: got None, exiting...")
            return

        print("thread_target: doing something with", message, "...")


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