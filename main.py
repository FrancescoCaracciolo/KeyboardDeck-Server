import sys
from pynput import keyboard
from KeyboardDeck.network import NetworkManager
from KeyboardDeck.music_info import NowPlaying
import KeyboardDeck.keyboard_events as kbfunc
import qdarkstyle
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QSpacerItem,
)


class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.np = NowPlaying()
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
        
        status = QFormLayout() # Status Layout
        self.capturelabel = QLabel("Capture: Off")
        self.serverlabel = QLabel("Server: Off")
        status.addRow(self.capturelabel)
        status.addRow(self.serverlabel)
        
        settings = QFormLayout()  # Settings Layout
        self.motd_line = QLineEdit("")
        edit_motd_button = QPushButton("Edit")
        edit_motd_button.clicked.connect(self.update_motd)
        settings.addRow("Current Motd:", self.motd_line)
        self.nowplaying = QCheckBox("Send Now Playing as MOTD")
        settings.addRow(self.nowplaying)
        self.nowplaying.clicked.connect(self.nowplaying_checked)
        
        if not self.np.is_supported():
            self.nowplaying.setCheckable(False)
            settings.addRow(QLabel("Not available on your OS"))
            
        settings.addRow(edit_motd_button)

        
        windowLayout.addLayout(form)
        windowLayout.addLayout(options)
        windowLayout.addLayout(settings)
        windowLayout.addSpacerItem(QSpacerItem(0,30))
        windowLayout.addLayout(status)
        start = QPushButton("Start")
        stop = QPushButton("Stop")
        start.clicked.connect(self.start)
        stop.clicked.connect(self.stop)
        windowLayout.addWidget(start)
        windowLayout.addWidget(stop)

        self.setLayout(windowLayout)
    
    def update_motd(self):
        self.network.update_motd_th(self.motd_line.text())
    
    def on_song_update(self, song: dict):
        string = song["title"] + "\\auth//" + song["artist"]
        self.network.update_motd_th(string)
        self.motd_line.setText(string)

    def nowplaying_checked(self):
        if self.nowplaying.isChecked():
            self.motd_line.setEnabled(False)
            self.np.music_listener_th(self.on_song_update)
        else:
            self.motd_line.setEnabled(True)
            self.np.stop_listener()

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
            self.np.stop_listener()
    
    def closeEvent(self, event) -> None:
        self.stop()
        
    def on_press(self, key):
        kbfunc.on_press(key, self.network, self.controlOn)
    
    def on_release(self, key):
        kbfunc.on_release(key, self.controlOn)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = Window()
    window.show()
    sys.exit(app.exec_())
