import sys
import requests
from PySide2.QtUiTools import QUiLoader #allows us to import .ui files
from PySide2.QtWidgets import QApplication, QLineEdit, QCheckBox
from PySide2.QtCore import QFile, QObject

serverID = 'http://127.0.0.1:5000/'

def connect(un, pw):
    print("Called connect")
    for x in range(5):
        x = requests.post(serverID + 'login', {'un':un, 'pw':pw})
        if x.status_code == 200:
            return x.json()['ret']

def verifyConnection():
    print("Called verify")
    # TODO
    
class MainWindow(QObject):

    #class constructor
    def __init__(self, ui_file, parent=None):

        self.un = ""
        self.pw = ""
        self.connected = False
        #call parent QObject constructor
        super(MainWindow, self).__init__(parent)

        #load the UI file into Python
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        
        #always remember to close files
        ui_file.close()

        # perform login
        self.window.pushButton.clicked.connect(self.login)

        #show window to user
        self.window.show()
    
    def login(self):
        self.un = self.window.findChild(QLineEdit, 'Username').text()
        self.pw = self.window.findChild(QLineEdit, 'Password').text()
        self.connected = connect(self.un, self.pw)
        if self.connected:
            app.quit()
            # TODO: Reveal Pygame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow('client/login.ui')
    app.exec_()
    print("test")
    sys.exit(0)