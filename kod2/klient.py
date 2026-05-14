# ======
# Klient
# ======
# Detta är det så kallade "offret"
# Den ansluter till servern. 

from socket import socket, AF_INET, SOCK_STREAM, gethostname
from types import NoneType
from ansi_colors import Colors
from threading import Thread
from signal import signal, SIGINT, SIGTERM
from time import sleep, time
from os import system, name as OSname, get_terminal_size as tsize


# 2026-05-02
class Tcp:
    def __init__(self, target_ip: str, port: int = 8888):
        self.target_ip = target_ip
        self.port = port
        
        self.connected = False
        self.last_handshake: float = None
        self.threshold: int = 30
        self.min_loop_time = 1

        self.socket = socket()
        
        self.main_thread = Thread(target=self.mainloop)
        self.main_thread.start()


    def send(self, msg: str):
        self.socket.send(msg.upper().encode())


    def recv(self, size: int = 1024):
        return self.socket.recv(size).decode().upper()
    

    def connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(1)

        try: 
            self.socket.connect((self.target_ip, self.port))
            
        except OSError: pass


        else: 
            try: 
                self.send(gethostname())

            except OSError: pass


            else:
                try: 
                    message = self.recv()

                except OSError: pass

                else:
                    if message == "CONNECTED":
                        self.connected = True
                        self.last_handshake = time()


    def check_dead_connection(self):
        if (time() - self.last_handshake) > self.threshold:
            self.connected = False

    
    def answer_alive(self):
        self.send("ALIVE")
        self.last_handshake = time()


    def terminate(self):
        self.socket.close()
        self.main_thread.join()


running = True
block = False
admin = False
passwd = None
min_loop_time = 0.5
recv_buffer: list[str] = []
send_buffer: list[str] = []

tcp = Tcp("sprch.hellgren.dev", 8888)


def gracefullStop(sig, frame):
    global running
    running = False


signal(SIGINT, gracefullStop)
signal(SIGTERM, gracefullStop)


def client():
    while not admin and passwd is None:
        pit = time()

        try:
            message = tcp.recv()

        except OSError: pass

        else: 
            recv_buffer.append(message)

        try: 
            tcp.send(send_buffer(0))
            send_buffer.pop(0)

        except OSError: pass



        elapsed = time() - pit
        sleep(max(0, min_loop_time - elapsed))

while running:
    pit = time()

    client()

    elapsed = time() - pit
    sleep(max(0, min_loop_time - elapsed))

tcp.terminate()