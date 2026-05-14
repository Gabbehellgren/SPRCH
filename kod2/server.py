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
    def __init__(self, port: int = 8888, min_loop_time: int = 1):
        self.port = port
        self.ip = self.get_ip()
        self.min_loop_time = min_loop_time 

        self.computers: list[Tcp.Computer] = []

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.settimeout(1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

        self.main_thread = Thread(target=self.mainloop)

        self.main_thread.start()


    def get_ip(self) -> str:
        with socket() as tmpSock:
            tmpSock.connect(("8.8.8.8", 443))
            return tmpSock.getsockname()[0]
        
    
    def listen_for_connections(self):
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


    def handle_dead_clients(self):
        tmp_list: list[Tcp.Computer] = []
        for computer in self.computers:
            if not computer.dead:
                tmp_list.append(computer)
            
            else:
                computer.terminate()
            
        self.computers = tmp_list


    def mainloop(self):
        while running:
            pit = time()

            self.listen_for_connections()
            self.handle_dead_clients()

            elapsed = time() - pit
            sleep(max(0, self.min_loop_time - elapsed))


    def terminate(self):
        for computer in self.computers:
            computer.terminate()

        self.socket.close()
        self.main_thread.join()


    class Computer:
        def __init__(self, socket: socket, _retadress, name: str = "", timeout: int = 5):
            self.socket = socket
            self.socket.settimeout(timeout)
            self.ip: str = _retadress[0]
            self.port: int = _retadress[1]
            self.name = name

            self.dead = False
            self.admin = False

            self.mainThread = Thread(target=self.mainloop)
            self.mainThread.start()

            self.time_between_checkup = 10
            self.loop_min_time = 1
            

        def send(self, msg: str):
            self.socket.send(msg.upper().encode())


        def recv(self, size: int):
            return self.socket.recv(size).decode().upper()


        def stay_in_touch(self):
            try:
                self.send("ALIVE?")

            except OSError: self.dead = True
            
            else:
                try: 
                    message = self.recv(1024)
                
                except OSError: self.dead = True

                else: 
                    if message != "ALIVE":
                        self.dead = True

        
        def listen(self):
            try:
                message = self.recv(1024)

            except OSError: pass

            else:
                return message
            

        def mainloop(self):
            last_check = 0
            while running and not self.dead:
                pit = time()

                if (time() - last_check) >= self.time_between_checkup:
                    self.stay_in_touch()
                    last_check = time()

                message = self.listen()
                match message:
                    case "LOGIN":
                        pass

                elapsed = time() - pit
                sleep(max(0, self.loop_min_time - elapsed))


        def terminate(self):
            self.socket.close()
            self.mainThread.join()




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


tcp.terminate()