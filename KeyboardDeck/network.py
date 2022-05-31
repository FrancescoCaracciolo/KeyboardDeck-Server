from socket import *
from threading import Thread
from update import update
import json


class NetworkManager:
    def __init__(self, ip, port, timeout: int = 2):
        """Main class to manage connections

        Args:
            ip (str): IP of the server
            port (int): Port of the server
            timeout (int, optional): UDP requests timeout. Defaults to 2.
        """
        self.ip = ip
        self.port = port
        self.server = None
        self.client = None
        self.stop_threads = False
        self.server_running = False
        self.timeout = timeout
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.settimeout(timeout)
    
    def sendUDP(self, message: str):
        """Sends udp requests to the server

        Args:
            message (str): Message to send to the server

        Returns:
            str: Response from the server
        """
        try:
            self.socket.sendto(message.encode('utf-8'), (self.ip, self.port))
            result, server_address = self.socket.recvfrom(2048)
            result = result.decode('utf-8')
            return result
        except timeout:
            return None
    
    def get_updates(self) -> str:
        """Send a get request to get updates from the server
        """
        message = {
            "request": "get",
        }
        message = json.dumps(message)
        self.sendUDP(message)
    def send_keypress(self, key : str):
        """Sends a keypress to the server

        Args:
            key (str): The key pressed
        """
        message = {
            "request": 'keypress',
            "key": key,
        }
        message = json.dumps(message)
        self.sendUDP(message)
        
    def update_motd(self, motd : str):
        """Updates the current motd

        Args:
            motd (str): New motd
        """
        message = {
            "request": 'updatemotd',
            "motd": motd,
        }
        message = json.dumps(message)
        self.sendUDP(message)
    
    def update_motd_th(self, motd : str):
        """Updates the current motd on another thread

        Args:
            motd (str): New motd
        """
        message = {
            "request": 'updatemotd',
            "motd": motd,
        }
        message = json.dumps(message)
        thread = Thread(target= self.sendUDP, args=(message,))
        thread.start()
        
    
    def start_server(self, port: int, debug: bool = False):
        """Starts the server on current thread

        Args:
            port (int): Port where the server is started
        """
        motd = ""
        up = update()
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", port))
        server_socket.settimeout(self.timeout)
        while True:
            if self.stop_threads:
                break
            try:
                result = ""
                message, client_address = server_socket.recvfrom(2048)
                message = message.decode('utf-8')
                print(message + "\n" if debug else "", end="")
                message = json.loads(message)
                if message['request'] == 'keypress':
                    up.add(message['key'])
                    result = json.dumps({"ok": True})
                if message['request'] == 'updatemotd':
                    motd = message['motd']
                if message['request'] == 'get':
                    data = up.print_remove()
                    res = {
                        "ok": True,
                        "keys": data,
                        "motd": motd,
                    }
                    result = json.dumps(res)
                print(result + "\n" if debug else "", end="")
                server_socket.sendto(
                    result.encode('utf-8'),
                    client_address
                )
            except timeout:
                pass

    def start_server_th(self, port: int):
        """Starts server on another thread

        Args:
            port (int): port of the server
        """
        self.server_running = True
        self.stop_threads = False
        self.thread = Thread(target= self.start_server, args=(port,))
        self.thread.start()
    
    def stop_server(self):
        """Stops the server if it is running on another thread
        """
        if self.server_running:
            self.stop_threads = True
            self.thread.join()
            self.stop_threads = False
    
