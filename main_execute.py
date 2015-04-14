# -*- coding: utf-8
# 3 8 11
import sys
import random
import json
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
        self.selected_node = None
        self.selected_line = None
        self.line_map = dict()
        self.mode_type = 'task'
        self.initUI()
        self.initMenu()
    
    def initUI(self):
        self.setGeometry(350, 150, 800, 550)
        self.setWindowTitle('My magic application')
        self.modeButton = QtGui.QPushButton(self.get_mode_button_text(), self)
        self.connect(self.modeButton, QtCore.SIGNAL('clicked()'), self.mode_button_heandler)

    def initMenu(self):
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        
        saveAction = QtGui.QAction(QtGui.QIcon('save.png'), '&Save as..', self)
        saveAction.triggered.connect(self.save_into_file)

        openFileAction = QtGui.QAction(QtGui.QIcon('open.png'), '&Open file', self)
        openFileAction.triggered.connect(self.open_file)

        menubar = self.menuBar()   
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openFileAction)
    
    def get_current_mode(self):
        pass

    def get_mode_button_text(self):
        if self.mode_type == 'task':
            return 'System mode'
        else:
            return 'Task mode'

    def mode_button_heandler(self):
        if self.mode_type == 'task':
            self.mode_type = 'system'
        else:
            self.mode_type = 'task'
        lable = self.get_mode_button_text()
        self.modeButton.setText(lable)

    def save_into_file(self):
        save_file_dialog = DialogWindow()
        file_name, ans = save_file_dialog.showDialog('Enter file name:')
        if ans:
            data = dict(
                node_list=self.node_list,
                line_list=self.line_list,
                node_last_index=node_index_gen.next(),
                line_last_index=line_index_gen.next(),
                line_map=self.line_map,
            )
            with open(file_name, 'w') as f:
                json.dump(data, f)
        print 'file was saved'

    def open_file(self):
        global node_index_gen, line_index_gen
        open_file_dialog = DialogWindow()
        file_name, ans = open_file_dialog.showDialog('Enter file name:')
        if ans:
            with open(file_name, 'r') as f:
                data = json.load(f)
                print type(data)
                if data:
                    self.line_map = data['line_map']
                    self.node_list = data['node_list']
                    self.line_list = data['line_list']
                    node_index_gen = count(data['node_last_index'])
                    line_index_gen = count(data['line_last_index'])
                    print 'line indx ', line_last_index.next(), data['line_last_index']
                    print 'node indx ', node_index_gen.next(), data['node_last_index']

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
        for k, v in self.line_map.iteritems():
            print k, v
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
            print 'selecte node 1 = ', self.selected_node
            print 'selected node 2 = ', selected_node2
            if self.selected_node:
                if selected_node2 and selected_node2 != self.selected_node and not (
                    self.line_map.get((self.selected_node.id, selected_node2.id)) or
                    self.line_map.get((selected_node2.id, self.selected_node.id))
                ):
                    # draw line
                    new_line = Line(line_index_gen.next(), self.selected_node, selected_node2)
                    self.line_list.append(new_line)
                    self.line_map[self.selected_node.id, selected_node2.id] = new_line
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