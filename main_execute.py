# -*- coding: utf-8
# 3 8 11
import sys
import random
from itertools import count
from PyQt4 import QtGui, QtCore

from Objects import *

node_index_gen = count()
line_index_gen = count()


class MainGui(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainGui, self).__init__()
        self.node_list = []
        self.line_list = []
        self.node_posicion_map = dict()
        self.selected_node = None
        self.selected_line = None
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
        selected_obj = find_selected_odj(self.node_list+self.line_list, x, y)
        selected_line, selected_node2 = (None, None)
        if isinstance(selected_obj, Node):
            selected_node2 = selected_obj
        elif isinstance(selected_obj, Line):
            selected_line = selected_obj
        if selected_line:
            if self.selected_line:
                self.selected_line.selected = False
            self.selected_line = selected_line
            selected_line.selected = True
        else:
            if self.selected_line:
                self.selected_line.selected = False
            self.selected_line = None
            if self.selected_node:
                if selected_node2:
                    # draw line
                    new_line = Line(line_index_gen.next(), self.selected_node, selected_node2)
                    self.line_list.append(new_line)
                self.selected_node.selected = False
                self.selected_node = None 
            else:            
                if selected_node2:
                    self.selected_node = selected_node2
                    selected_node2.selected = True
                else:    
                    node_weight_dialog = DialogWindow()
                    weight, ans = node_weight_dialog.showDialog('Enter node weight:')
                    if ans:
                        new_node = Node(node_index_gen.next(), x, y)
                        new_node.set_weight(weight)
                        self.node_list.append(new_node)
                        self.node_posicion_map[(x, y)] = new_node



    def mouseMoveEvent(self, event):
        new_x = event.pos().x()
        new_y = event.pos().y()
        if self.selected_node:
            self.selected_node.set_new_coordinate(new_x, new_y)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_E:
            if self.selected_node:
                node_weight_dialog = DialogWindow()
                weight, ans = node_weight_dialog.showDialog('Enter new node weight:')
                if ans:
                    self.selected_node.set_weight(weight)
            elif self.selected_line:
                line_weight_dialog = DialogWindow()
                weight, ans = line_weight_dialog.showDialog('Enter new line weight:')
                if ans:
                    self.selected_line.set_weight(weight)

    
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

        for line in self.line_list:
            line.draw_itself(event, qp)
        for node in self.node_list:
            node.draw_itself(event, qp)


def find_selected_odj(obj_list, x, y):
    selected_obj = None
    for obj in obj_list:
        if obj.is_selected(x, y):
            selected_obj = obj
            break
    return selected_obj


class DialogWindow(QtGui.QWidget):
    
    def __init__(self):
        super(DialogWindow, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        self.le = QtGui.QLineEdit(self)
        self.le.move(130, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        
    def showDialog(self, input_label):
        
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            input_label)
        
        if ok:
            self.le.setText(str(text))
        return text, ok


app = QtGui.QApplication(sys.argv)
ex = MainGui()
ex.show()
app.exec_()