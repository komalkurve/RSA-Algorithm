import socket
import time
import rsa
import mysql.connector
import datetime
import string


serversoc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversoc.bind(("127.0.0.1",9980))
serversoc.listen(5)

n, e, d = rsa.getPair(1024)

cnx = mysql.connector.connect(user="root", database="customers", password="komal")
cursor = cnx.cursor()

while True:
      clientsocket,addr = serversoc.accept()
      clientPublicData = clientsocket.recv(1024)
      clientN, clientE = [int(x) for x in clientPublicData.split(" ")]

      clientsocket.send(str(n) +" "+ str(e))

      found = False

      while found!=True:
          authenticationData = clientsocket.recv(30000)
          username,password = authenticationData.split(" ")
          username = rsa.decrypt(username, n, d)
          password = rsa.decrypt(password, n, d)
          query = 'SELECT TIMESTAMPDIFF(SECOND,lastAttempt,NOW()), trial FROM users WHERE Username="%s"' %(username)
          cursor.execute(query,username)

          for (diff, trial) in cursor:
              found = True
              log, count = int(diff), int(trial)
              #print log, count

          if found == False:
              clientsocket.send(rsa.encrypt("Invalid Username", clientN, clientE))
              break

          if found == True and count == 0 and log < 86400:

              clientsocket.send(rsa.encrypt("Account blocked for 24 hours", clientN, clientE))
              #query = 'UPDATE users set lastAttempt=NOW() WHERE Username="%s"' %(username)
              #cursor.execute(query,username)
              cnx.commit()
              break



          query = 'SELECT Lastlogin, Balance FROM users WHERE Username="%s" AND Password=password("%s")' %(username, password)
          cursor.execute(query,username)

          secondfound = False

          for (Lastlogin, Balance) in cursor:
              secondfound = True
              balance = Balance
              prevlog = Lastlogin
              #print balance
              #print prevlog


          if secondfound == False:
              if count == 0:
                 clientsocket.send(rsa.encrypt("Account blocked for 24 hours", clientN, clientE))
                 break
              else:
                 clientsocket.send(rsa.encrypt("Invalid Password", clientN, clientE))
                 query = 'UPDATE users set trial="%s" where Username="%s"' %(str(trial - 1),username)
                 cursor.execute(query,username)
                 query = 'UPDATE users set lastAttempt=NOW() WHERE Username="%s"' %(username)
                 cursor.execute(query,username)
                 cnx.commit()
                 break

          data = "Balance : " + str(balance) + "\n" + "Last login: " + str(prevlog) + "\n"
          query = 'UPDATE users set Lastlogin=NOW(), trial=3 WHERE Username="%s" AND Password=password("%s")' %(username, password)
          cursor.execute(query, username)
          cnx.commit()

          clientsocket.send(rsa.encrypt(data, clientN, clientE))

          clientsocket.close()
          cnx.commit()


cur.close()
cnx.close()
serversoc.close()
