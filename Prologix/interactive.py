import socket, select, string, sys

GPIBHOST = "192.168.0.118"
GPIBPORT = 1234
GPIBADDR = 25

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try :
	s.connect((GPIBHOST, GPIBPORT))
except :
	print( 'Unable to connect')
	sys.exit()

print( 'Connected to remote host')

script = [
"++addr {GPIBADDR:%02d}",
"*RST"
"*IDN?"
"*OPT?"
]

while True:
        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for sock in read_sockets:
            if sock == s:
                print("Incoming")
                data = sock.recv(4096)
                if not data :
                    print( 'Connection closed')
                    sys.exit()
                else :
                    print("data:" ,data)
                    sys.stdout.write(data.decode())
                    sys.stdout.flush()
            else :
                print("Outgoing")
                msg = sys.stdin.readline()
                s.send(msg.encode())
