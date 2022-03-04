from threading import Thread;
from threading import Event;
import time;

 

class ChildThread(Thread):
    myStopSignal = 0
   
    def __init__(self,aStopSignal):
        Thread.__init__(self)
        self.myStopSignal = aStopSignal   


    def run(self):
        print("Child Thread:Started")
        for i in range(1,10):
            if(self.myStopSignal.wait(0)):
                print ("ChildThread:Asked to stop")
                break;       

            print("Doing some low priority task taking long time")
            time.sleep(2) #Just simulating time taken by task with sleep

        print("Child Thread:Exiting")
        

print("Main Thread:Started")
aStopSignal     = Event()           
aChildThread    = ChildThread(aStopSignal)
aChildThread.start()
aChildThread.join(4) # I can wait for 4 seconds only

 

if aChildThread.is_alive() is True:
    print("Child thread is alive")
    aStopSignal.set()
    aChildThread.join()
    

 

print("Main Thread; Exiting")