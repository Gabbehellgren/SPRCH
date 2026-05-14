#==============================
#|                            |
#|    Client/admin program    |
#|                            |
#==============================

# Oscar Hellgren Te23A Ebersteinska gy
# Detta program fyller två program, är klient delen och låter mig logga in som admin.


# Importer och då importerar jag de klasser och funktioner jag behöver
from socket import socket, AF_INET, SOCK_STREAM, gethostname
from time import time, sleep



# TCP klass
# Ansvarar för att ansluta till servern och se ifall det går för lång tid mellan "kolla anslutning"
# innehåller de verktyg för att bygga resten av koden (send, recv).
# 2026-05-14
class Tcp:
    def __init__(self, target_ip: str, port: int = 8888, threshold: int = 30):
        self.connected = False
        self.hand_shake = None 
        self.threshold = threshold

        self.target_ip = target_ip
        self.port = port


    def try_to_connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)

        self.socket.connect((self.target_ip, self.port))
        self.socket.settimeout(30)

        try:
            self.send(gethostname())

        except OSError: pass

        else:
            try:
                msg = self.recv(1024)
            
            except OSError: pass

            else:
                if msg == "CONNECTED":
                    self.connected = True
                    self.socket.settimeout(1)
                    self.hand_shake = time()


    def still_connected(self):
        if type(self.hand_shake) == float:
            if time() - self.hand_shake > self.threshold:
                self.connected = False
    

    def connections_handler(self):
        while running:
            if self.connected:
                pass

            else:
                self.try_to_connect()


    def recv(self, size: int):
        if type(self.socket) == socket:
            payload = self.socket.recv(size)
            msg = payload.decode()
            Msg = msg.upper()
            return Msg


    def send(self, msg: str):
        if type(self.socket) == socket:
            Msg = msg.upper()
            payload = Msg.encode()
            self.socket.send(payload)


    def on_recv(self):
        while running:
            while not self.connected: sleep(1)

            try: 
                msg = self.recv(1024)

            except OSError: pass

            else:
                match msg:
                    case "ALIVE?":
                        self.send("ALIVE")
                        self.hand_shake = time()




# Static
running = True
min_loop_time = 1


tcp = Tcp("vpn.hellgren.dev")

tcp.connections_handler()