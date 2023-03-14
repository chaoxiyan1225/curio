#coding=utf8
import threading
import time
import queue
import pyttsx3

q = queue.Queue()
engine = pyttsx3.init()
def speak(msg):
    print('call say')
    engine.say(msg)
    print('call startLoop')
    engine.startLoop(False)
    #engine.runAndWait()
    #time.sleep(2)
    print('call endLoop')
    engine.endLoop()

def consume():
    while True:
        try:
            msg = q.get(block=False)
            if not msg:
               print("sleep now 1s")
               time.sleep(2)
            
            speak(msg)
            print(f'{msg} monitor success')
            time.sleep(2)

        except queue.Empty:
               time.sleep(2)

def addMonitorMsg(msg:str):
    q.put(msg)
    print("%s add success" % (msg))

try:
    c = threading.Thread(target=consume)
    c.setDaemon(True)
    c.start()
except Exception as e:
    print(e)
