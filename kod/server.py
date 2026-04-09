#==============================#
#                              #
#      Server Programmet       #
#                              #
#==============================#
# Oscar Hellgren Te23A Ebersteinska Gy


# Importer
from mailbox import Message
from time import time
from threading import Thread
from socket import gethostname, gethostbyname, socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from ansi_colors import Colors



# Klasser/ansvar:

# En klass som ansvarar för att skriva ut meddelanden som alla andra klasser ärver
# Den ska skicka ut vanliga, varnings och error meddelanden.
# 2026/04/09

class ConsoleOutput(Colors):
    def __init__(self, id:str):
        super().__init__()
        self.id = id

        self.rgb(255, 127, 0, False, "orange")
        self.rgb(175, 65, 20, True, "bg_orange")


    def nrm(self, message: str):
        print(self.bold + self.magenta + "@" + self.id, end=self.end)
        print(self.Black + " [" + self.bold + self.Black + "NRM" + self.end + self.black +"] -> ", end=self.end)
        print(message)


    def cau(self, message: str):
        print(self.bold + self.magenta + "@" + self.id, end=self.end)
        print(self.Black + " [" + self.bold + self.orange + "CAU" + self.end + self.black +"] -> ", end=self.end)
        print(message)


    def ftl(self, message: str):
        print(self.bold + self.magenta + "@" + self.id, end=self.end)
        print(self.Black + " [" + self.bold + self.Red + "FLT" + self.end + self.black +"] -> ", end=self.end)
        print(message)

    def brk(self):
        print()




# En klass som ansvarar för all info om datorn e.g. hostname; ip; portar
# 2026/04/09
class ComputerInfo(ConsoleOutput):
    def __init__(self, port_udp: int = 8888, port_tcp: int = 5555):
        super().__init__("ComputerInfo")
        
        self.nrm("Fetching computer info...")

        try:
            self.name = gethostname()
            self.nrm("Hostname: " + self.Green + self.name)

        except:
            self.cau("Could not retrieve hostname")

        try:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            self.address = ip
            self.nrm("Ip: " + self.Green + self.address)

        except:
            self.cau("Could not retrieve ip")

        self.udp_port = port_udp
        self.tcp_port = port_tcp

        self.brk()




# En klass som ansvarar för udp anrop
# Som default bör den skrika datorns Hostname (Mitt fall "Marathon")
# Denna klass ska sälv ansvara för att skicka udp anrop men ska också ha en terminerings metod
# Egen mainloop som kan köras asyncront
# 2026/04/06
class UdpBroadcaster(ConsoleOutput):
    def __init__(self, message: str, target_ip: str, port: int, delay: float = 1):
        super().__init__("UDP-broadcaster")

        self.nrm("Initializing UDP broadcaster...")

        self.nrm("Setting options...")
        self.message = message
        self.target = target_ip
        self.port = port
        self.delay = delay
        self.running = True
        self.nrm("Options set")
        self.nrm("Message: " + self.Green + "'" + self.message + "'")
        self.nrm("Target ip: " + self.Green + self.target)
        self.nrm("Port: " + self.Green + str(self.port))
        self.nrm("Broadcasting every " + self.Green + str(self.delay) + self.end + "s")

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.thread = Thread(None, self.mainloop)
        #self.thread.start()


    def mainloop(self):
        packed_binary = self.message.encode("UTF-8")
        destination = (self.target, self.port)
        pit = 0

        while self.running:
            if (time() - pit) >= self.delay:
                self.socket.sendto(packed_binary, destination)
                pit = time()


    
    def stop(self):
        self.running = False
        self.thread.join()
        self.socket.close()

info = ComputerInfo()
udp = UdpBroadcaster(info.name, "<broadcast>", 8888, 1)
