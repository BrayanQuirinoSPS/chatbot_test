import time
import threading

#Intento de hacer una ssesion, no me meti por miedo a más problemas
class Session(threading.Thread):
    def __init__(self, pParam1, pParam2):  
        threading.Thread.__init__(self)  
        now = time.time() 
        self.future = now + 60
        self.stoprequest = threading.Event()
    def run(self):
        while time.time() < self.future:
            self.session=True
        self.session=False

