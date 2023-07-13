import socket
import asyncio
MAXBYTES=1024
MAXHOSTS=24

class comms:
    def __init__(self, host, port, role):
        self.host=host
        self.port=port
        self.role=role
        self.soc = socket.socket()
        if(role == "server"):
            self.soc.settimeout(1.5)
            try:
                self.soc.bind((host, port))
                self.soc.listen(MAXHOSTS)
            except:
                print("Socket bind & listen unsuccessful")

    def clientrreaddata(self):
        return self.soc.recv(MAXBYTES).decode()

        
    def acceptconnection(self):
        self.conn, addr = self.soc.accept()
        print("connected to host at ", str(addr))

    def serverreaddata(self):
        data = self.conn.recv(1024).decode()
        if not data:
            return ""
        else:
            return data

    def serversenddata(self, data):
        print("server sending data")
        try:
            self.conn.send(str(data).encode())
        
        except:
            print("server disconnected on send... ")
            print("attempting to reconnect ")
            self.conn.servercloseconn(self)
            self.conn.connect(self)
            self.conn.send(str(data).encode())

    def servercloseconn(self):
        self.conn.close()


    def clientconnect(self):
        self.soc.connect((self.host, self.port))

    def clientsenddata(self, data):
        print("client sending data")
        try:
            self.soc.send(str(data).encode())

        except:
            print("client disconnected on send... ")
            print("attempting to reconnect ")
            self.clientclosesoc(self)
            self.conn.connect(self)
            self.soc.send(str(data).encode())

    def clientclosesoc(self):
        self.soc.close()

    def read(self):
        if(self.role == "server" ):
            data = self.serverreaddata()
        else:
            data = self.clientrreaddata()
        return data

    def write(self, data):
        if(self.role == "server"):
            self.serversenddata(data)
        else:
            self.clientsenddata(data)

    def connect(self):
        if(self.role == "server"):
            self.acceptconnection()
        else:
            self.clientconnect()

    def disconnect(self):
        if(self.role == "server"):
            self.servercloseconn()
        self.clientclosesoc()
            