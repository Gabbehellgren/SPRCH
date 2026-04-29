#==============================#
#                              #
#           Färger             #
#                              #
#==============================#
# Oscar Hellgren Te23A Ebersteinska Gy

# Importer
from ansi_colors import Colors
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from time import time
from signal import signal, SIGINT
from os import system, name as osName

# Klasser/ansvar

# Klass som kan ta emot udp packet och läsa var de kommer ifrån
# 2026/04/17
class UdpReciver:
    def __init__(self, listenport: int, timeout: int = 10):
        self.listenport = listenport
        self.timeout = timeout

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.settimeout(1)
        self.socket.bind(("", self.listenport))

        self.running = True
        self.available_servers = []

        self.thread = Thread(target=self.mainloop)
        self.resetThread = Thread(target=self.reset)
        self.resetThread.start()
        self.thread.start()
    

    def mainloop(self):
        while self.running:
            try:
                data, address = self.socket.recvfrom(1024)

            except:
                pass

            else:
                message = data.decode("utf-8")
                ip = address[0]

                server = self.Server(message, ip)
                server_is_unique = True

                for unit in self.available_servers:
                    if hasattr(unit, "name"):
                        if server.name == unit.name:
                            server_is_unique = False

                if server_is_unique:
                    self.available_servers.append(server)

            
    def reset(self):
        point_in_time = 0

        while self.running:
            if (time() - point_in_time) >= self.timeout:
                self.available_servers = []
                point_in_time = time()


    def terminate(self):
        self.running = False
        self.thread.join()
        self.resetThread.join()
        self.socket.close()


    class Server:
        def __init__(self, name: str, ip: str, port: int = 5555):
            self.name = name
            self.ip = ip
            self.port = port


class TcpHandler:
    def __init__(self):

        def 


# Klass som ansvarar för alla kommandon och vad de gör. Ansvarar för signal interups också ev.
# 2026/04/17
class Commands(Colors):
    def __init__(self):
        super().__init__()
        self.terminations = []


    def add_term(self, func):
        self.terminations.append(func)


    def terminateAll(self):
        for func in self.terminations:
            func()

    #====Commands=================================

    def ls(self, servers: list):
        if len(servers) > 0:
            print("Listing servers:")
            for server in servers:
                index = servers.index(server) + 1
                print(end=" " + str(index) + ": ")
                print(self.Blue + server.name + "@" + server.ip + self.end + "\n")
        else:
            print("No servers discoverd\n")


    def clear(self):
        if osName == "nt":
            system("cls")

        else:
            system("clear")


    def stop(self):
        global running
        running = False
        self.terminateAll()

running = True

com = Commands()
com.clear()
udpReciver = UdpReciver(8888)
com.add_term(udpReciver.terminate)

while running:
    suspected_command = input("SPRCH-A: >>> ")
    command = suspected_command.lower()

    if command == "ls":
        com.ls(udpReciver.available_servers)

    elif command == "clear":
        com.clear()

    elif command in ["stop", "^c", "quit", "exit"]:
        com.stop()