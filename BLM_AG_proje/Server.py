class SharedObject:
    def __init__(self, value: list):
        self.matrix = value

shared_variable = SharedObject([[".", ".", "."],[".", ".", "."],[".", ".", "."]])

import socket
class Server:
    def __init__(self):
        self.host = "25.50.131.225"
        self.port = 3000
        self.server_socket = None
        self.client_sockets = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)  # İki istemciye kadar bağlantı kabul et
        print("Server dinlemede...")

        for _ in range(2):  # İki istemci kabul et
            client_socket, addr = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print("Bağlantı alındı:", addr)

    def receive_data(self, client_index):
        client_socket = self.client_sockets[client_index]
        data = client_socket.recv(1024)
        return data.decode("utf-8")

    def send_data(self, client_index, data):
        client_socket = self.client_sockets[client_index]
        client_socket.send(data.encode("utf-8"))

    def stop(self):
        for client_socket in self.client_sockets:
            client_socket.close()
        self.server_socket.close()
        print("Server durduruldu.")

if __name__ == "__main__":

    def mattostr(matrix):
        str = ""
        for i in range(3):
            for j in range(3):
                str += matrix[i][j]
                str += " "
            str += "\n"
        return str

    def check_win(matrix):

        for i in range(3):
            if matrix[i][0] == matrix[i][1] == matrix[i][2] and matrix[i][0] != ".":
                return True

        for i in range(3):
            if matrix[0][i] == matrix[1][i] == matrix[2][i] and matrix[0][i] != ".":
                return True

        if matrix[0][0] == matrix[1][1] == matrix[2][2] and matrix[0][0] != ".":
            return True

        if matrix[0][2] == matrix[1][1] == matrix[2][0] and matrix[0][2] != ".":
            return True
        
        return False
    

    def check_tie(matrix):

        count = 0

        for i in range(3):
            for j in range(3):
                if matrix[i][j] == ".":
                    count+=1
        
        return count == 0
    

    def restart():
        shared_variable.matrix = [[".", ".", "."],[".", ".", "."],[".", ".", "."]]


    clients = ["x", "o"]  # gelen clientlere otomatik o veya x atıyor
    server = Server()
    server.start()

    counter = 0
    resetTheMatrix = False

    while True:
        # turn bilgisi
        if counter%2==0:
            firstplayerturn = True
            secondplayerturn = False
            server.send_data(0, "x") # true gidecek
            server.send_data(1, "") # false gidecek
        else:
            firstplayerturn = False
            secondplayerturn = True
            server.send_data(0, "") # false gidecek
            server.send_data(1, "o") # true gidecek

        
        if firstplayerturn:
            server.send_data(0, mattostr(shared_variable.matrix))
            if resetTheMatrix:
                restart()
            x = int(server.receive_data(0)) - 1
            y = int(server.receive_data(0)) - 1
            shared_variable.matrix[x][y] = clients[0]

        elif secondplayerturn:
            server.send_data(1, mattostr(shared_variable.matrix))
            if resetTheMatrix:
                restart()
            x = int(server.receive_data(1)) - 1
            y = int(server.receive_data(1)) - 1
            shared_variable.matrix[x][y] = clients[1]


        result_win = check_win(shared_variable.matrix)
        result_tie = check_tie(shared_variable.matrix)

        
        if result_win or result_tie:
            resetTheMatrix = True
        else:
            resetTheMatrix = False



        counter+=1
