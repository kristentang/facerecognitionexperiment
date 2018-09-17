# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 18:19:21 2016

@author: matthaberland
"""

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import QTimer

import socket
from sys import stdout

class ChatApp(QWidget):
    def __init__(self):
        super(ChatApp,self).__init__()
        self.initUi()
        self.initNetwork()
        self.initChat()
    
    def initChat(self):            
        self.qt = QTimer(self)
        self.qt.timeout.connect(self.receiveMessage)
        self.qt.start(2000) 
        
    def receiveMessage(self):
  
        try:
            message = self.s.recv(1024)
            if message == "":
                self.qt.stop()
                message = "<connection closed>"
            self.l1.setText(str(message))
        except:
            pass
        
    def closeEvent(self,e):
         self.s.close()
    
    def initNetwork(self):
        try:
            # self.l1.setText("<attempting to connect>")
            self.beClient()
        except:
            # self.l1.setText("<waiting for connection>")
            self.beServer()
        self.s.settimeout(0.25)

    def beServer(self):
        self.ss = socket.socket()
        self.ss.bind(("localhost",5100))
        self.ss.listen(1)
        self.s,add = self.ss.accept()
        self.ss.close()
        self.l1.setText("<connected>")
#        self.isServer = True
    
    def beClient(self):
        self.s = socket.socket()
        self.s.connect(("localhost",5100))
        self.l1.setText("<connected>")
#        self.isServer = False
        
    def initUi(self):
        self.setGeometry(100,100,300,100)
        title = "Chat App"
#        if self.isServer:
#            title = "Chat App - Server"
#        else:
#            title = "Chat App - Client"
            
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        
        self.t1 = QLineEdit(self)
        self.t1.returnPressed.connect(self.sendMessage)
        
        self.l1 = QLabel("",self)

        self.layout.addWidget(self.t1)
        self.layout.addWidget(self.l1)
        
        self.setLayout(self.layout)
        self.show()
        
    def sendMessage(self):
        message = self.t1.text()
        if message != "":
            self.s.send(message)
        
def main():
    
    app = QApplication([])
    w = ChatApp()
    app.exec_()
    
if __name__=="__main__":
    main()
