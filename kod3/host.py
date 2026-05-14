#==============================
#|                            |
#|    Host/server program     |
#|                            |
#==============================

# Oscar Hellgren Te23A Ebersteinska gy
# Detta program ansvarar för att vänta på anslutningar från klienter och hantera ifall anslutning tappas, 
# kunna ta emot admin login försök och när det finns en admin fungera som en router och skicka kommandon till klienter


# Importer och då importerar jag de klasser och funktioner jag behöver
from socket import socket, AF_INET, SOCK_STREAM
from time import time, sleep




# Klasser:

# Klient klass
# Egentligen bara en template för hur en klient fungerar
# 2026-05-11
class Client:
    def __init__(self, sock: socket, address: tuple) -> None:
        self.sock = sock
        self.sock.settimeout(1)
        self.ip = address[0]
        self.port = address[1]
        self.name = ""

    
    def send(self, msg: str) -> None:
        Msg = msg.upper()
        payload = Msg.encode()
        self.sock.send(payload)

    
    def recv(self, size: int) -> str:
        payload = self.sock.recv(size)
        msg = payload.decode()
        Msg = msg.upper()
        return Msg




# TCP klass
# Ansvarar för att ta emot anslutningar, kolla ifall anslutningen tappas och -
# innehåller de verktyg för att bygga resten av koden (send, recv).
# 2026-05-14
class Tcp:
    def __init__(self, port: int = 8888):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(("0.0.0.0", port))
        self.socket.listen()
        self.clients: list[Client] = []


    def append_client(self, subject: Client):
        unique = True
        for client in self.clients[:]:
            if subject.name == client.name and subject.ip == client.ip:
                unique = False
                break

        if unique:
            self.clients.append(subject) 
            print(self.clients)


    def listen_for_connections(self):
        while running:
            pit = time()

            sock, addr = self.socket.accept()
            client = Client(sock, addr)

            try:
                client.name = client.recv(1024)
            
            except OSError: pass

            else:
                self.append_client(client)
                client.send("CONNECTED")

            elapsed = time() - pit
            sleep(max(0, min_loop_time - elapsed))




# Static:
running = True
min_loop_time = 1

tcp = Tcp()

tcp.listen_for_connections()