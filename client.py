from socket import *
import json

IP = "mc.silveros.it"
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)  # AF_INET6 per IPV6, SOCK_STREAM TCP, SOCK_DGRAM UDP


while True:
    try:
        message = {
            "request": "get",
        }
        message = json.dumps(message)
        clientSocket.settimeout(2)
        clientSocket.sendto(message.encode('utf-8'), (IP, serverPort))
        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            modifiedMessage = modifiedMessage.decode('utf-8')
            if modifiedMessage != "{}":
                print(modifiedMessage)
            #print("Numero di consontanti: ", modifiedMessage)
        except TimeoutError:
            print("Il server non ha risposto")
    except KeyboardInterrupt:
        clientSocket.close()
