# ======
# Server
# ======
# Detta program ska köras på min hem server och bjussa på TCP anslutning.
# TIll en början behöver detta program två trådar (ev. main + en extra)
# Main har hand om de anslutningar som finns och routar trafik.
# extra tråd är till för att hantera nya anslutningar.

from ast import Name
from curses import tparm
from socket import socket, AF_INET, SOCK_STREAM, gethostname, gethostbyname, SOL_SOCKET, SO_REUSEADDR, error as sock_error
from threading import Thread
from time import time, sleep, strftime, localtime
from signal import signal, SIGINT, SIGTERM, SIGTSTP
from os import system, name as osType, get_terminal_size as tSize
from ansi_colors import Colors


# 2026-04-29
# En klass som kan ta hand om inkommande anslutningar. och skickar vidare trafik.
class Tcp:
    def __init__(self, port: int = 8888, time_between_catchups: int = 30):
        self.port = port
        self.ip = self.get_ip()
        self.time_between_catchups = time_between_catchups 

        self.computers: list[Tcp.Computer] = []

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.settimeout(1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

        self.listen_for_connections_thread = Thread(target=self.listen_for_connections)
        self.stay_in_touch_thread = Thread(target=self.stay_in_touch)

        self.listen_for_connections_thread.start()
        self.stay_in_touch_thread.start()


    def get_ip(self) -> str:
        with socket() as tmpSock:
            tmpSock.connect(("8.8.8.8", 443))
            return tmpSock.getsockname()[0]
        
    
    def listen_for_connections(self):
        while running:
            try:
                socket, address = self.socket.accept()

            except OSError: pass

            else:
                computer = self.Computer(socket, address)

                try:
                    computer.name = computer.recv(1024)
                    
                except OSError: pass

                else:
                    unique = True
                    for stored_computer in self.computers:
                        if computer.name == stored_computer.name or computer.ip == stored_computer:
                            unique = False
                            break

                    if unique:
                        try:
                            computer.send("CONNECTED")

                        except OSError: pass
                        
                        else:
                            self.computers.append(computer)

    
    def stay_in_touch(self):
        while running:
            pit = time()
            
            tmp_computers = []
            for computer in self.computers:
                try:
                    computer.send("ALIVE?")
                
                except OSError:
                    pass

                else:
                    try:
                        reply = computer.recv(1024)

                    except OSError:
                        pass

                    else:
                        if reply == "ALIVE":
                            tmp_computers.append(computer)
            
            self.computers = tmp_computers

            elapsed = time() - pit
            sleep(max(0, self.time_between_catchups - elapsed))


    def terminate(self):
        self.socket.close()
        self.listen_for_connections_thread.join()
        self.stay_in_touch_thread.join()


    class Computer:
        def __init__(self, socket: socket, _retadress, name: str = "", timeout: int = 5):
            self.socket = socket
            self.socket.settimeout(timeout)
            self.ip: str = _retadress[0]
            self.port: int = _retadress[1]
            self.name = name

        def send(self, msg: str):
            self.socket.send(msg.upper().encode())

        def recv(self, size: int):
            return self.socket.recv(size).decode().upper()            

        



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
        if osType == "nt":
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
        


    def servers(self, computers: list = []):
        
        if len(computers) == 0:
            print("\tNo computers connected\n")
            print(self.Black + "-"*53 + self.end + "\n")
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
        print("\n" + self.Black + "-"*53 + self.end + "\n")


    def update(self, computers: list = []):
        self.clear()
        self.title()
        self.servers(computers)
        self.desc()




running = True
paused = False
delay = 1


out = Output()
tcp = Tcp()


def graceFullStop(sig, frame):
    print("\nQuitting")
    global running
    running = False
    tcp.terminate()




def lockout(sig, frame):
    print(" is locked..")




signal(SIGINT, graceFullStop)
signal(SIGTERM, graceFullStop)
signal(SIGTSTP, lockout)


while running:
    pit = time()

    out.update(tcp.computers)

    elapsed = time() - pit
    sleep(max(0, delay - elapsed))

