import sys
from PySide2.QtUiTools import QUiLoader #allows us to import .ui files
from PySide2.QtWidgets import QApplication, QLineEdit, QCheckBox
from PySide2.QtCore import QFile, QObject

_isConnected = False
serverID = ''

'''
Billie Jean is not my lover.
'''

def connect():
    print("Called connect")
    # TODO: Attempt to login

def verifyConnection():
    print("Called verify")
    # TODO
    
class MainWindow(QObject):

    #class constructor
    def __init__(self, ui_file, parent=None):

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
        self.window.Clear.clicked.connect(self.clear)

        #show window to user
        self.window.show()
    
    def clear(self):
        # TODO: Find un and pw and attempt a pingie-dingie
        for i in [0, 1]:
            self.binaryVals[i] = 0
            for n in list(range(8))[::-1]:
                box = self.window.findChild(QCheckBox, 'Reactant' + str(i+1) + '_' + str(n+1))
                if box.isChecked():
                    self.binaryVals[i] += 2 ** n

if __name__ == '__main__':
    main_window = MainWindow('login.ui')
    sys.exit(app.exec_())