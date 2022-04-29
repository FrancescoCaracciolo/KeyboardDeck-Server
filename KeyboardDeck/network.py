from socket import *
from threading import Thread
from update import update
import json
class NetworkManager:
    def __init__(self, ip, port, timeout: int = 2):
        self.ip = ip
        self.port = port
        self.server = None
        self.client = None
        self.stop_threads = False
        self.server_running = False
        self.socket = clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.socket.settimeout(timeout)
    
    def sendUDP(self, message: str):
        try:
            self.socket.sendto(message.encode('utf-8'), (self.ip, self.port))
            result, serverAddress = self.socket.recvfrom(2048)
            result = result.decode('utf-8')
            return result
        except timeout:
            return None
    
    def start_server(self, port):
        up = update()
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(("", port))
        while True:
            if self.stop_threads:
                break
            message, clientAddress = serverSocket.recvfrom(2048)
            message = message.decode('utf-8')
            message = json.loads(message)
            if message['request'] == 'send':
                up.add(message['event'])
                modifiedMessage = "ok"
            if message['request'] == 'get':
                data = up.print_remove()
                modifiedMessage = json.dumps(data)
            serverSocket.sendto(
                modifiedMessage.encode('utf-8'),
                clientAddress
            )
    def start_server_th(self, port):
        self.server_running = True
        self.stop_threads = False
        self.thread = Thread(target= self.start_server, args=(port,))
        self.thread.start()
    
    def stop_server(self):
        if self.server_running:
            self.stop_threads = True
            self.thread.join()
            self.stop_threads = False
    
