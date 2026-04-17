#==============================#
#                              #
#      Server Programmet       #
#                              #
#==============================#
# Oscar Hellgren Te23A Ebersteinska Gy


# Importer
from time import time, sleep
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
    
    def showcase(self):
        self.nrm("Stands for NORMAL, nothing is wrong all good")
        self.cau("Stands for CAUTION, a warning but the program should continue as normal")
        self.ftl("Stands for FATAL When this message showed something is wrong")
        self.brk()

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
        super().__init__("ComputerInfo\t")
        
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

        self.nrm("Initilizing UDP broadcaster")

        self.message = message
        self.target = target_ip
        self.port = port
        self.delay = delay
        self.running = True
        self.broadcast = False
    
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.thread = Thread(None, self.mainloop)
        self.thread.start()

        self.nrm("UDP brodcaster successfully started")

        self.switchState()

        self.brk()


    def mainloop(self):
        packed_binary = self.message.encode("UTF-8")
        destination = (self.target, self.port)
        pit = 0

        while self.running:
            while self.broadcast:
                if (time() - pit) >= self.delay:
                    self.socket.sendto(packed_binary, destination)
                    pit = time()


    def switchState(self):
        self.broadcast = not self.broadcast
        if self.broadcast:
            self.cau(f"UDP broadcast started! A package is sent every {self.delay}s making your puper visible to others")
        else:
            self.nrm("The program is no-longer broadcasting")
    
    def terminate(self):
        self.nrm("Attemting to close UDP broadcaster")
        self.broadcast = False
        self.running = False
        self.thread.join()
        self.socket.close()
        self.nrm("Successfully closed the UDP broadcaster")
        self.brk()



out = ConsoleOutput("System\t\t")
info = ComputerInfo()
udp = UdpBroadcaster(info.name, "127.0.0.1", 8888, 1)
