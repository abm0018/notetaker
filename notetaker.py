import os
import sys
import re
from pdb import set_trace
from datetime import datetime
from PyQt6.QtWidgets import QLabel, QMainWindow
from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtWidgets import QLineEdit, QFileDialog
from PyQt6.QtWidgets import QCheckBox, QTextEdit 
'''
Quick and dirty script to help me take notes
very quickly at test events with timestamps
and other relevant paramters. 
'''
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.statusBar().showMessage('Ready!!!')
        self.currdir = os.getcwd()
        self.fullfilename = ''
        self.filename = ''
        self.runnum = ''
        self.f = None
        ########## BUTTONS #####################

        btn = QPushButton('Browse', self)
        btn.clicked.connect(self.updateCurrDir)
        btn.move(600, 15)
        
        btn2 = QPushButton('Clear', self)
        #moved slot / signal for clearing below txtbrowser
        btn2.move(20, 340)
       
        btn3 = QPushButton("Update Log", self)
        btn3.clicked.connect(self.updateLog)
        btn3.move(400, 340)

        btn4 = QPushButton("New File", self)
        btn4.clicked.connect(self.newFile)
        btn4.move(550, 340)

        ########## LABELS ####################

        lbl1 = QLabel("Filename: ", self)
        lbl1.move(10, 10)
        lbl1.show()
       
        lbl2 = QLabel("S/n:", self)
        lbl2.move(20, 75)
        lbl2.show()

        lbl3 = QLabel("Run #:", self)
        lbl3.move(220, 75)
        lbl3.show()

        ########## LINEEDITS ##################

        self.le1 = QLineEdit(self) #directory selection
        self.le1.move(75, 15)
        self.le1.setFixedWidth(500)
        self.le1.setText(self.currdir)
        self.le1.show()

        self.le2 = QLineEdit(self) # serial number entry
        self.le2.move(50, 75)
        self.le2.setFixedWidth(150)
        self.le2.show()

        self.le3 = QLineEdit(self) # run number entry
        self.le3.move(275, 75)
        self.le3.setText('0')
        self.le3.setFixedWidth(100)
        self.le3.show()

        ######## OTHER ###########################
        
        self.chk1 = QCheckBox("Auto Incr Run", self)
        self.chk1.move(275, 120)
        self.chk1.show()

        self.txtbrowser = QTextEdit(self)
        self.txtbrowser.move(400, 75)
        self.txtbrowser.resize(300, 250)
        self.txtbrowser.show()
        btn2.clicked.connect(self.txtbrowser.clear)

        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Notetaker Helper V0.1')
        self.show()

    def updateLog(self):
        if (self.f == None): #we need to open a file
            self.newFile()

        newdata = getCurrDateTime() + ': ' +  self.txtbrowser.toPlainText()
        newdata += '\n'
        self.txtbrowser.clear()
        self.updateStatus()
        self.f.write(newdata)

    def newFile(self):
        if (self.f != None):
            self.f.close() #close last file
        self.updateFileName()
        self.fullfilename = self.currdir + '/' + self.filename
        self.f = open(self.fullfilename, 'a') #open file and append new data
        self.txtbrowser.clear()
        

    def updateStatus(self): #placeholder function for updating status bar
        currtime = getCurrDateTime()
        utc = getCurrTimestamp()
        msg = f'Last Log Update: {currtime}'
        self.statusBar().showMessage(msg)

    def updateCurrDir(self):
        self.currdir = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if (self.currdir == ''): #if user exits out of dir selection
            self.currdir = os.getcwd()

        self.le1.setText(self.currdir)

    def updateFileName(self):
        # check if we need to increment the run number
        if (self.chk1.isChecked()): #no type checking, don't care
            self.runnum = int( self.le3.text()) + 1
            self.le3.setText(str(self.runnum))
        else:
            self.runnum = int(self.le3.text())

        tmpname = getCurrTimestamp()
        
        if (self.le2.text() != ''):
            tmpname += ('_' + self.le2.text())
        if (self.le3.text() != ''):
            tmpname += ('_' + str(self.runnum))
        tmpname += '.log'
        self.filename = tmpname
        self.le1.setText(self.currdir + '/' + self.filename)

def getTrailingNumber(st): #may use in future if allowing run numbers with starting text...
    m = re.search(r'\d+$', st)
    return int(m.group()) if m else None

def getCurrDateTime():
    return datetime.now().strftime('%m/%d/%Y %H:%M:%S')

def getCurrTimestamp():
    return datetime.utcnow().strftime("%s")

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
