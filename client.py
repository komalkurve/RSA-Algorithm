import socket
import rsa
import getpass
import datetime
import string

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(("127.0.0.1",9980))

n, e, d = rsa.getPair(1024)

clientsocket.send(str(n)+" "+str(e))

serverPublicData = clientsocket.recv(3000)
serverN, serverE = [int(x) for x in serverPublicData.split(" ")]

print "\n\n\n\n\t\t\tXYZ BANK"
found = False

while found!=True:
    username = raw_input("\n\nEnter username : ")
    password = getpass.getpass("Enter password : ")
    print

    clientsocket.send(rsa.encrypt(username, serverN, serverE) + " " + rsa.encrypt(password, serverN, serverE))

    data = clientsocket.recv(100000)
    data = rsa.decrypt(data, n, d)

    if data == 'Invalid Username' or data == "Account blocked for 24 hours":
        print data
        break

    else:
        print data
        found = True

clientsocket.close()
