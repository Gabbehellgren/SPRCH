#==============================#
#                              #
#      Server Programmet       #
#                              #
#==============================#
# Oscar Hellgren Te23A Ebersteinska Gy


# Importerfrom ssl import SOCK_STREAM
from concurrent.futures import thread
from time import time, sleep
from threading import Thread
from signal import signal, SIGINT, SIGTERM
from socket import gethostname, gethostbyname, socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, SOCK_STREAM
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
            self.nrm("Hostname: " + self.Green + self.name + self.end)

        except:
            self.cau("Could not retrieve hostname")

        try:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            self.address = ip
            self.nrm("Ip: " + self.Green + self.address + self.end)

        except:
            self.cau("Could not retrieve ip")

        self.udp_port = port_udp
        self.tcp_port = port_tcp

        self.brk()


# UDP klass som skickar udp paket ut i "rymden" för där kan ingen höra en fisa
# 2026/04/20
class Udp:
    def __init__(self, message: str, send_to: str, port: int, period: float = 1):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.send_to = send_to
        self.port = port
        self.period = period
        self.running = True
        self.message = message
        
        self.mainThread = Thread(target=self.mainloop)
        self.mainThread.start()

    def mainloop(self):
        pit = 0
        while self.running:
            pit = time()
            
            self.sock.sendto(self.message.encode(), (self.send_to, self.port))

            elapsed = time() - pit
            sleep(max(0, self.period - elapsed))


    def terminate(self):
        self.running = False
        self.mainThread.join()

console = ConsoleOutput("System\t\t")
info = ComputerInfo()
udp = Udp(info.name, "127.0.0.1", info.udp_port)

def stop(sig, dat):
    print()
    console.nrm("Closing program")
    udp.terminate()

signal(SIGINT, stop)
signal(SIGTERM, stop)