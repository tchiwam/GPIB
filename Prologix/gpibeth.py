import socket

class gpibeth:
    def __init__(self,host, port, addr):
        self.host   = host
        self.port   = port
        self.addr   = addr
        self.timeout = None
        self.verbose = False
        self.connect()
        self.setaddr(self.addr)

    def setverbose(self,state):
        self.verbose = state

    def settimeout(self,timeout):
        self.timeout = timeout
        self.s.settimeout(timeout)

    def read(self):
        data = self.s.recv(4096).decode().strip()
        if self.verbose:
            print(f"IN << {data:s}")
        return data

    def send(self,command):
        if self.verbose:
            print(f"OUT >> {command:s}")
        self.s.send(f'{command:s}\n'.encode())
        return True

    def setaddr(self, addr):
        self.addr = addr
        self.send(f'++addr {addr:02d}')
        self.getvalue('++addr')
        
    def getvalue(self,command):
        self.send(command)
        data = self.read()
        return data

    def connect(self):
        if self.verbose:
            print("Connecting")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(self.timeout)
        try :
            self.s.connect((self.host, self.port))
            if self.verbose:
                print( f'Connected to {self.host:s} {self.port:4d}')
        except :
            print( f'Unable to connect to {self.host:s} {self.port:4d}')
            return False
        return True

    def close(self):
        self.s.close()
        if self.verbose:
            print("Connection closed")
        return True

