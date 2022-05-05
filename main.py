import sys
from pynput import keyboard
from KeyboardDeck.network import NetworkManager
import KeyboardDeck.keyboard_events as kbfunc
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)


class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.controlOn = 0
        # Initialize the Keyboard Listener
        self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)

        self.setWindowTitle("KeyboardDeck Backend")
        # Initialize NetworkManager
        self.network = NetworkManager("127.0.0.1", 42069)
        
        windowLayout = QVBoxLayout()  # Main window layout
        
        form = QFormLayout()  # Form layout 
        self.server_ip = QLineEdit("127.0.0.1")
        self.server_port = QLineEdit("42069")
        form.addRow("Server IP:", self.server_ip)
        form.addRow("Port:", self.server_port)

        options = QVBoxLayout()  # Options Layout
        self.startcapture = QCheckBox("Start Capture")
        self.startserver = QCheckBox("Start Server")
        options.addWidget(self.startcapture)
        options.addWidget(self.startserver)
        
        status = QFormLayout() # Status Leyout
        self.capturelabel = QLabel("Capture: Off")
        self.serverlabel = QLabel("Server: Off")
        status.addRow(self.capturelabel)
        status.addRow(self.serverlabel)
        
        windowLayout.addLayout(form)
        windowLayout.addLayout(options)
        windowLayout.addLayout(status)
        start = QPushButton("Start")
        stop = QPushButton("Stop")
        start.clicked.connect(self.start)
        stop.clicked.connect(self.stop)
        windowLayout.addWidget(start)
        windowLayout.addWidget(stop)

        self.setLayout(windowLayout)
    
    def start(self):
        """Starts server/capture"""
        self.network = NetworkManager(self.server_ip.text(), int(self.server_port.text()))
        if self.startcapture.isChecked():
            self.capturelabel.setText("Capture: On, Port: " + str(self.network.port))
            if self.listener.is_alive:
                self.listener.stop()
                self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
            self.listener.start()
        if self.startserver.isChecked():
            self.serverlabel.setText("Server: On, Port: " + str(self.network.port))
            if self.network.server_running:
                self.network.stop_server()
            self.network.start_server_th(self.network.port)
    def stop(self):
        """Stops Server/Capture"""
        if (self.listener.is_alive):
            self.listener.stop()
            self.listener = keyboard.Listener(on_press= self.on_press, on_release= self.on_release)
            self.capturelabel.setText("Capture: Off")
        if self.network.server_running:
            self.network.stop_server()
            self.serverlabel.setText("Server: Off")
    
    def closeEvent(self, event) -> None:
        self.stop()
        
    def on_press(self, key):
        kbfunc.on_press(key, self.network, self.controlOn)
    
    def on_release(self, key):
        kbfunc.on_release(key, self.controlOn)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
