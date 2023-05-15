from app import App, transfer_queue
import threading
import time

start_time = time.time_ns()


def verificationMessage(message):
        data = message["data"]

        if( len(data) == 0 ):
            print("Aucune donnée dans data")
            return -1
        
        if( len(data["legs"]) == len(data)):
            print("Aucun moteur renseigné")
            return -2
        
        if( len(data["legs"]) == 0):
            print("Aucune patte renseignée")
            return -3
        
        return 0


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

        if( not verificationMessage(message) ):
             print("Movement robot")





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