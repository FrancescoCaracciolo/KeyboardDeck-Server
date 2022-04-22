import keyboard
from socket import *
import json

IP = "localhost"
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)  # AF_INET6 per IPV6, SOCK_STREAM TCP, SOCK_DGRAM UDP


while True:
    try:
        n = keyboard.read_hotkey()
        message = {
            "request": "send",
            "event": str(n),
        }
        print(n)
        message = json.dumps(message)
        if n:
            clientSocket.settimeout(2)
            clientSocket.sendto(message.encode('utf-8'), (IP, serverPort))
            try:
                modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
                modifiedMessage = modifiedMessage.decode('utf-8')
                #print("Numero di consontanti: ", modifiedMessage)
            except timeout:
                print("Il server non ha risposto")
    except KeyboardInterrupt:
        clientSocket.close()
        exit()

