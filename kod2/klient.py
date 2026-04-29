# ======
# Klient
# ======
# Detta är det så kallade "offret"
# Den ansluter till servern. 

from socket import socket, AF_INET, SOCK_STREAM, gethostname, error as so_error
from threading import Thread
from signal import signal, SIGINT, SIGTERM
from time import sleep, time

class Tcp:
    def __init__(self, target:str, port:int = 8888):
        self.target_ip = target
        self.port = port
        self.is_connected = False
        self.handshake = 0

        self.t = Thread(target=self.checkConnection)
        self.t.start()


    def connect(self):
        delay = 1
        while True:
            pit = time()
            try:
                print("Trying to connect...")
                self.socket = socket(AF_INET, SOCK_STREAM)
                self.socket.settimeout(1)
                self.socket.connect((self.target_ip, self.port))
                self.send(gethostname())
                if self.recv() == "connected".upper():
                    self.is_connected = True
                    print("Connected")
                    self.handshake = time()
                    break

            except so_error:
                pass

            elapsed = time() - pit
            sleep(max(0, delay - elapsed))

            
    def send(self, msg:str):
        try:
            self.socket.send(msg.upper().encode())

        except so_error:
            self.is_connected = False


    def recv(self):
        message = self.socket.recv(1024).decode().upper()
        return message
    

    def checkConnection(self):
        if time() - self.handshake >= 2:
            self.is_connected = False


    def terminate(self):
        self.socket.close()
        self.t.join()


running = True
tcp = Tcp("192.168.0.105", 8888)


def gracefullStop(sig, frame):
    print()
    global running
    running = False
    tcp.terminate()


signal(SIGINT, gracefullStop)
signal(SIGTERM, gracefullStop)


while running:
    if not tcp.is_connected:
        tcp.connect()

    try:
        message = tcp.recv()
    except OSError:
        pass
    
    if message == "STATUS":
        tcp.send("ALIVE")
        tcp.handshake = time()