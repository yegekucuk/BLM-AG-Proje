import socket
import os
from Server import Server

class Client:
    def __init__(self, ip:str):
        self.host = ip
        self.port = 3000
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print("Sunucuya bağlanıldı.")

    def send_data(self, data):
        self.client_socket.send(data.encode("utf-8"))

    def receive_data(self):
        data = self.client_socket.recv(1024)
        return data.decode("utf-8")

    def disconnect(self):
        self.client_socket.close()
        print("Bağlantı kapatıldı.")


def printMatrix(matrix):
    for i in range(3):
        for j in range(3):
            print(matrix[i][j] + " ",end="")
        print("")


def check_win(matrix):
        count = 0

        for i in range(3):
            for j in range(3):
                if matrix[i][j] == ".":
                    count+=1
        
        if count == 0:
            return -2

        for i in range(3):
            if matrix[i][0] == matrix[i][1] == matrix[i][2] and matrix[i][0] != ".":
                if matrix[i][0] == "x":
                    return "x"
                else:
                    return "o"

        for i in range(3):
            if matrix[0][i] == matrix[1][i] == matrix[2][i] and matrix[0][i] != ".":
                if matrix[0][i] == "x":
                    return "x"
                else:
                    return "o"

        if matrix[0][0] == matrix[1][1] == matrix[2][2] and matrix[0][0] != ".":
                if matrix[0][0] == "x":
                    return "x"
                else:
                    return "o"

        if matrix[0][2] == matrix[1][1] == matrix[2][0] and matrix[0][2] != ".":
            if matrix[0][2] == "x":
                return "x"
            else:
                return "o"

        return -1

def bos_matrix(matrix):

    count = 0

    for i in range(3):
        for j in range(3):
            if matrix[i][j] == ".":
                count+=1
    
    return count == 9

def print_stats(wins, ties, losses):
    print(f"Wins: {wins}, Ties: {ties}, Losses: {losses}")

def write_stats(name, wins, ties, losses):
    writethis = "%s\n%d\n%d\n%d"%(name,wins,losses,ties)
    file = open("save.sav","w")
    file.write(writethis)
    file.close()
    
# main
name = None
wins = 0
losses = 0
ties = 0
writethis = "%s\n%d\n%d\n%d"%(name,wins,losses,ties)
file = open("save.sav","r")
list = [x.strip() for x in file.readlines()]
file.close()
# save bosluk check
if list == []:
    name = input("İsim giriniz: ")
    write_stats(name, wins, ties, losses)

print("Welcome %s"%(name))
host = "25.50.131.225"
ip = input("IP Adresi giriniz: ")
while ip != host:
    ip = input("IP Adresi giriniz: ")

client = Client(ip)
client.connect()


while True:
    data = client.receive_data()
    turn = bool(data)
    if turn:
        os.system("cls")
        print("You are " + data + "\n")
        guncelTahta = client.receive_data()
        
        # string to 3x3 matrix
        guncelTahta = guncelTahta.replace("\n","")
        matris = list(guncelTahta.split(" "))
        matris.pop()
        mymatrix = [matris[:3],matris[3:6],matris[6:9]]

        printMatrix(mymatrix)
        
        res = False

        result = check_win(mymatrix)
        if result == -2:
            print("Tie")
            ties += 1
            print_stats(wins, ties, losses)
            write_stats(name, wins, ties, losses)
            res = True
        elif result != -1:
            print("You lost")
            losses += 1
            print_stats(wins, ties, losses)
            write_stats(name, wins, ties, losses)
            res = True

        if res:

            if input("Press r to restart: ") != "r":
                client.disconnect()

            print("Restart")
            mymatrix = [[".", ".", "."],[".", ".", "."],[".", ".", "."]]
            printMatrix(mymatrix)
        

        # print(mymatrix) this is 3x3 matrix
        successful = False
        while not successful:
            try:
                x = int(input("X koordinatını gir : "))
                y = int(input("y koordinatını gir : "))
                if 1 <= x <= 3 and 1 <= y <= 3:
                        successful = True
            except:
                pass

        while mymatrix[x-1][y-1] != ".":
            successful = False
            while not successful:
                try:
                    x = int(input("X koordinatını gir : "))
                    y = int(input("y koordinatını gir : "))
                    if 1 <= x <= 3 and 1 <= y <= 3:
                        successful = True
                except:
                    pass

        client.send_data(str(x))
        client.send_data(str(y))
        mymatrix[x-1][y-1] = data
        printMatrix(mymatrix)

        wincon = check_win(mymatrix)

        if data == wincon:
            print("You Win")
            wins += 1
            print_stats(wins, ties, losses)
            write_stats(name, wins, ties, losses)
        elif wincon == -2:
            print("Tie")
            ties += 1
            print_stats(wins, ties, losses)
            write_stats(name, wins, ties, losses)
            

# while matrix[x][y] != ".":
#             x = int(server.receive_data(0)) - 1
#             y = int(server.receive_data(0)) - 1
