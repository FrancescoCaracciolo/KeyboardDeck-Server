from socket import *
class NetworkManager:
    def __init__(self, ip, port, timeout: int = 2):
        self.ip = ip
        self.port = port
        self.server = None
        self.client = None
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
    
