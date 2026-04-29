# ======
# Server
# ======
# Detta program ska köras på min hem server och bjussa på TCP anslutning.
# TIll en början behöver detta program två trådar (ev. main + en extra)
# Main har hand om de anslutningar som finns och routar trafik.
# extra tråd är till för att hantera nya anslutningar.

from socket import socket, AF_INET, SOCK_STREAM, gethostname, gethostbyname, SOL_SOCKET, SO_REUSEADDR, error as sockerr
from threading import Thread
from time import time, sleep, strftime, localtime
from signal import signal, SIGINT, SIGTERM, SIGTSTP
from os import error as oserr, system, name as os, get_terminal_size as tSize
from ansi_colors import Colors


# 2026-04-28
# En klass som kan ta hand om inkommande anslutningar. och skickar vidare trafik.
class Tcp:
    def __init__(self, port:int = 8888):
        self.ip = self.get_own_ip()
        self.port = port

        self.clients:list = []

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.settimeout(5)
        self.sock.bind((self.ip, self.port))
        self.sock.listen()

        self.t = Thread(target=self.listen_for_connection)
        

    def startT(self):
        self.t.start()


    def get_own_ip(self):
        with socket() as s:
            s.connect(("8.8.8.8", 443))
            return s.getsockname()[0]
        
    
    def listen_for_connection(self):
        while running:
            while paused: sleep(5)
            try:
                sock, address = self.sock.accept()
                client = self.Client(sock, address)
                client.name = client.recv()

                unique = True
                for computer in self.clients:
                    if computer.name == client.name and computer.ip == client.ip:
                        unique = False
                        break
                
                if unique:
                    self.clients.append(client)
                    client.send("connected".upper())

            except:
                pass


    def checkConnections(self):
        global last_error
        if len(self.clients) == 0: return

        clients = []
        for computer in self.clients:
            try:
                computer.send("STATUS")
                message = computer.recv()

                if message == "ALIVE":
                    clients.append(computer)
                    last_error += "puper found"
                else:
                    last_error += message

            except OSError:
                pass

        self.clients = clients
            

    def terminate(self):
        self.sock.close()
        self.t.join()


    class Client:
        def __init__(self, socket: socket, address: tuple):
            self.socket = socket
            self.name:str = None
            self.ip:str = address[0]


        def send(self, msg: str):
            self.socket.send(msg.encode())


        def recv(self):
            return self.socket.recv(1024).decode()




# 2026-04-28
# En klass som har koll på utskrift.
class Output(Colors):
    def __init__(self):
        super().__init__()
        self.time_format = "%Y-%m-%d %H:%M:%S"
        #self.started = datetime.now().strftime(self.time_format)
        self.started = time()
        

    def getTimeSinceStart(self):
        sec = int(time() - self.started)
        timmar = sec // 3600
        minuter = (sec % 3600) // 60
        sekunder = sec % 60
        return f"{timmar:02}:{minuter:02}:{sekunder:02}"


    def formatTime(self, sec: float):
        return strftime(self.time_format, localtime(sec))


    def clear(self):
        if os == "nt":
            system("cls")
        
        else:
            system("clear")


    def title(self):
        print(self.red + """                                                                                                                                                          
  ▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄▄    ▄▄▄  ▄    ▄              ▄▄▄▄                                                                       ▀                 
 █▀   ▀ █   ▀█ █   ▀█ ▄▀   ▀ █    █             █▀   ▀  ▄▄▄    ▄ ▄▄  ▄   ▄   ▄▄▄    ▄ ▄▄       ▄▄▄    ▄▄▄    ▄ ▄▄  ▄   ▄  ▄▄▄     ▄▄▄    ▄▄▄  
 ▀█▄▄▄  █▄▄▄█▀ █▄▄▄▄▀ █      █▄▄▄▄█             ▀█▄▄▄  █▀  █   █▀  ▀ ▀▄ ▄▀  █▀  █   █▀  ▀     █   ▀  █▀  █   █▀  ▀ ▀▄ ▄▀    █    █▀  ▀  █▀  █ 
     ▀█ █      █   ▀▄ █      █    █     ▀▀▀         ▀█ █▀▀▀▀   █      █▄█   █▀▀▀▀   █          ▀▀▀▄  █▀▀▀▀   █      █▄█     █    █      █▀▀▀▀ 
 ▀▄▄▄█▀ █      █    █  ▀▄▄▄▀ █    █             ▀▄▄▄█▀ ▀█▄▄▀   █       █    ▀█▄▄▀   █         ▀▄▄▄▀  ▀█▄▄▀   █       █    ▄▄█▄▄  ▀█▄▄▀  ▀█▄▄▀ 
    """ + self.end)
        print(self.Black + "="*tSize().columns + self.end + "\n")


    def desc(self):
        print("Program started: " + self.Green + self.formatTime(self.started) + self.end)
        print("Program has been running for: " + self.Magenta + self.getTimeSinceStart() + self.end)
        print("Welcome! This is the server side of the SPRCH service")
        print("\nTo " + self.Red + "CLOSE" + self.end + " the program press " + self.Red + "CTRL " + self.end + "+" + self.Red + " C" + self.end)
        print("The program also closes if e.g. computer is shutdown")
        print("\n" + self.Black + "-"*53 + self.end + "\n")


    def servers(self, computers: list = []):
        if len(computers) == 0:
            print("\tNo computers connected\n")
            return
        
        columns = (30, 17)

        blankline_under = self.underline + " "*columns[0] + " "*columns[1] + " " + self.end
        blanklineMiddle = " "*columns[0] + "|" + " "*columns[1]
        blanklineMiddle_under = self.underline + " "*columns[0] + "|" + " "*columns[1] + self.end

        print("Connected computers:")
        print(blankline_under)

        print(blanklineMiddle)
        print(self.bold + " Name:" + " "*(columns[0] - len(" Name:")) + self.end + "|" + self.bold +" IP adress:" + " "*(columns[1] - len(" IP adress:")))
        print(blanklineMiddle_under)

        for computer in computers:
            
            computer_name = computer.name
            computer_ip = computer.ip

            name_space = columns[0] - len(computer_name) - 1

            print(blanklineMiddle)
            print(" " + computer_name + " "*name_space + "| " + computer_ip)
            print(blanklineMiddle_under)


        print(self.end)


    def status(self):

        print("\n" + self.Black + "-"*53 + self.end + "\n")
        
        print(self.bold + "Status: ", end="")

        if paused:
            print(self.red + "○ " + "Paused" + self.end)

        else:
            print(self.green + "● " + "Running" + self.end)



    def update(self, computers: list = []):
        self.clear()
        self.title()
        self.desc()
        print(last_error)

        self.servers(computers)





running = True
paused = False
delay = 1

last_error = "No error"

out = Output()
tcp = Tcp()





def graceFullStop(sig, frame):
    print("\nQuitting")
    global running
    running = False
    tcp.terminate()




def pause(síg, frame):
    global paused
    paused = not paused




signal(SIGINT, graceFullStop)
signal(SIGTERM, graceFullStop)
signal(SIGTSTP, pause)


tcp.startT()


while running:
    pit = time()

    out.update(tcp.clients)
    tcp.checkConnections()

    elapsed = time() - pit
    sleep(max(0, delay - elapsed))

