# -*- coding: utf-8
# 3 8 11
import sys
import random
from itertools import count
from PyQt4 import QtGui, QtCore

from Objects import *

index_gen = count()


class MainGui(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainGui, self).__init__()
        self.node_list = []
        self.node_posicion_map = dict()
        self.selected_node = None
        self.initUI()
        self.initMenu()
    
    def initUI(self):
        self.setGeometry(350, 150, 800, 550)
        self.setWindowTitle('My magic application')

    def initMenu(self):
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)

        menubar = self.menuBar()   
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)


    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        if len(self.node_list):
            self.drawObjects(event, qp)
        self.update()
        qp.end()

    def mousePressEvent(self, event):
        x = event.pos().x()  # - CIRCLE_SIZE/2
        y = event.pos().y()  # - CIRCLE_SIZE/2
        self.selected_node = find_selected_node(self.node_list, x, y)
        if not self.selected_node:
            node_weight_dialog = DialogWindow()
            weight, ans = node_weight_dialog.showDialog()
            if ans:
                new_node = Node(index_gen.next(), x, y)
                new_node.set_weight(weight)
                self.node_list.append(new_node)
                self.node_posicion_map[(x, y)] = new_node


    def mouseMoveEvent(self, event):
        new_x = event.pos().x()
        new_y = event.pos().y()
        if self.selected_node:
            self.selected_node.set_new_coordinate(new_x, new_y)
    
    def drawPoints(self, qp):
        pen = QtGui.QPen(QtCore.Qt.blue, 3)
        qp.setPen(pen)

        size = self.size()
        
        for i in range(100):
            if i > 50:
                pen.setColor(QtCore.Qt.red)
                qp.setPen(pen)
            x = random.randint(1, size.width()-5)
            y = random.randint(1, size.height()-5)
            qp.drawPoint(x, y)

    def drawObjects(self, event, qp):
      
        color = QtGui.QColor(0, 0, 100)
        color.setNamedColor('#d4d4d4')
        pen = QtGui.QPen(QtCore.Qt.black, 3)
        qp.setPen(pen)

        for node in self.node_list:
            qp.setPen(QtGui.QPen(QtCore.Qt.black, 3))
            qp.drawEllipse(node.x, node.y, CIRCLE_SIZE, CIRCLE_SIZE)
            self.draw_id(event, qp, node)
            self.draw_weight(event, qp, node)


    def draw_id(self, event, qp, obj):
        text = str(obj.id)
        qp.setPen(QtGui.QColor(255, 80, 0))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(obj.x, obj.y, text)  

    def draw_weight(self, event, qp, obj):
        text = str(obj.weight)
        qp.setPen(QtCore.Qt.blue)
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(obj.center_x-5, obj.center_y+5, text)  


def find_selected_node(node_list, x, y):
    selected_node = None
    for node in node_list:
        if node.is_selected(x, y):
            selected_node = node
            break
    return selected_node


class DialogWindow(QtGui.QWidget):
    
    def __init__(self):
        super(DialogWindow, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        
    def showDialog(self):
        
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter node weight:')
        
        if ok:
            self.le.setText(str(text))
        return text, ok


app = QtGui.QApplication(sys.argv)
ex = MainGui()
ex.show()
app.exec_()