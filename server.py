# SERVER
from socket import *
from update import update
import json
serverPort = 42069

up = update()
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

print("Server running")
while True:

    message, clientAddress = serverSocket.recvfrom(2048)

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
