# SERVER
from socket import *
from update import update
from KeyboardDeck.network import NetworkManager
serverPort = 42069


network = NetworkManager("0.0.0.0", serverPort, 3)
network.start_server(serverPort, True)
