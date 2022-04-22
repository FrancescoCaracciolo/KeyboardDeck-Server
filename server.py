# SERVER
# Netstat -aut vede i processi in ascolto
from socket import *
from update import update
import json
serverPort = 12001

up = update()
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

print("Server in asconto")
while True:

    message, clientAddress = serverSocket.recvfrom(2048) #Bufsize dimensione massima stringa in byte

    message = message.decode('utf-8')
    message = json.loads(message)
    if message['request'] == 'send':
        up.add(message['event'])
        modifiedMessage = "ok"
    if message['request'] == 'get':
        data = up.print_remove()
        modifiedMessage = json.dumps(data)
    print(modifiedMessage)
    serverSocket.sendto(
        modifiedMessage.encode('utf-8'),
        clientAddress
    )
