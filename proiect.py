from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys 
import serial.tools.list_ports
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0,len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 115200
serialInst.port = portVar
serialInst.open()

class MainWindow(QtWidgets.QMainWindow):

    lux_val=0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.widget = QWidget()
        layout = QGridLayout()
        self.widget.setLayout(layout)

        
        self.graphWidget = pg.PlotWidget()
        
        layout.addWidget(self.graphWidget, 0, 0)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Lux values")
        
        self.x = list(range(100)) 
        self.y = [30 for _ in range(100)] 

        self.graphWidget.setBackground('w')

        color = pg.mkPen(color=(255,0,0))
        self.line =  self.graphWidget.plot(self.x, self.y, pen=color)
        
    def update(self):
        self.x = self.x[1:] 
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:] 
        self.y.append(self.lux_val)  
        if self.lux_val<2000:
            color1 = pg.mkPen(color=(0,255,0))    
            self.line.setData(self.x, self.y, pen = color1)
        elif self.lux_val<4000:
            color2 = pg.mkPen(color=(255,255,0))    
            self.line.setData(self.x, self.y, pen=color2)
        else :
            color3 = pg.mkPen(color=(255,0,0))    
            self.line.setData(self.x, self.y, pen=color3)

def collect_data():
    global window
    global data
    if serialInst.in_waiting:
        packet=serialInst.readline()
        buffer=packet.decode('utf', errors='replace').strip("\n")
        if "Light" in buffer:
            print(buffer)
            aux=buffer.split("=")
            data=aux[1]
            print(data)
            window.lux_val=int(data)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()


timer = QtCore.QTimer()
timer2 = QtCore.QTimer()

timer.setInterval(50)
timer2.setInterval(1)
timer2.timeout.connect(collect_data)

timer.timeout.connect(window.update)
timer2.start()
timer.start()

sys.exit(app.exec_())
            