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
        self.threshold: int = 45

        self.socket = socket()
        
        self.check_connection_thread = Thread(target=self.check_connection)
        self.check_connection_thread.daemon = True
        self.check_connection_thread.start()


    def send(self, msg: str):
        self.socket.send(msg.upper().encode())


    def recv(self, size: int = 1024):
        return self.socket.recv(size).decode().upper()
    

    def connect(self):
        delay = 1

        while not self.connected and running:
            pit = time()

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
                            break


            elapsed = time() - pit
            sleep(max(0, delay - elapsed))


    def terminate(self):
        self.socket.close()
        self.check_connection_thread.join()

            


running = True
tcp = Tcp("sprch.hellgren.dev", 8888)

def gracefullStop(sig, frame):
    global running
    running = False


signal(SIGINT, gracefullStop)
signal(SIGTERM, gracefullStop)


def tcp_mainloop():
    while running:
        pit = time()

        tcp.connect()
        
        try:
            message = tcp.recv()

        except OSError: pass
        
        else:
            match message:
                case "ALIVE?":
                    tcp.send("ALIVE")
                    print("ALIVE")

        elapsed = time() - pit
        sleep(max(0, 1 - elapsed))

tcp_thread = Thread(target=tcp_mainloop)
tcp_thread.start()




while running:
    pit = time()

    elapsed = time() - pit
    sleep(max(0, 1 - elapsed))




tcp.terminate()
tcp_thread.join()