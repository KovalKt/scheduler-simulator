# -*- coding: utf-8
# 3 8 11; 1 5
import sys
import random
import pickle
from itertools import count
from PyQt4 import QtGui, QtCore

from Objects import *
from helpers import create_graph
from helpers import check_system_graph
from helpers import check_task_graph
from helpers import build_queue3, build_queue8, build_queue11
from helpers import generate_graph_hendler

node_index_gen = count()
task_line_index_gen = count()
sys_line_index_gen = count()
proc_index_gen = count()


class MainGui(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainGui, self).__init__()
        self.node_list = []
        self.task_line_list = []
        self.sys_line_list = []
        self.proc_list = []
        self.selected_node = None
        self.selected_line = None
        self.task_line_map = dict()
        self.sys_line_map = dict()
        self.mode_type = 'task'
        self.has_error = False
        self.queue3 = []
        self.queue8 = []
        self.w = None
        self.initUI()
        self.initMenu()
    
    def initUI(self):
        self.setGeometry(350, 150, 800, 550)
        self.setWindowTitle('My magic application')
        self.modeButton = QtGui.QPushButton(self.get_mode_button_text(), self)
        self.modeButton.resize(self.modeButton.sizeHint())
        self.connect(self.modeButton, QtCore.SIGNAL('clicked()'), self.mode_button_heandler)

        self.validateButton = QtGui.QPushButton('Validation', self)
        self.validateButton.resize(self.validateButton.sizeHint())
        self.validateButton.move(150, 0)
        self.connect(self.validateButton, QtCore.SIGNAL('clicked()'), self.validate)
        self.modeTypeLabel = QtGui.QLabel(self.get_mode_label_text(), self)
        self.modeTypeLabel.move(700, 0)

        self.buildQueueButton = QtGui.QPushButton('Build queue', self)
        self.buildQueueButton.resize(self.buildQueueButton.sizeHint())
        self.buildQueueButton.move(237, 0)
        self.connect(self.buildQueueButton, QtCore.SIGNAL('clicked()'), self.build_queue_hendler)

        self.buildGenerateButton = QtGui.QPushButton('Generate graph', self)
        self.buildGenerateButton.resize(self.buildQueueButton.sizeHint())
        self.buildGenerateButton.move(337, 0)
        self.connect(self.buildGenerateButton, QtCore.SIGNAL('clicked()'), self.generate_graph_hendler)

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
            return 'go to System mode'
        else:
            return 'go to Task mode'

    def get_mode_label_text(self):
        text = {
            'task': "Task graph",
            'system': "System graph",
        }
        return text[self.mode_type]

    def mode_button_heandler(self):
        if self.mode_type == 'task':
            self.mode_type = 'system'
        else:
            self.mode_type = 'task'
        lable = self.get_mode_button_text()
        self.modeButton.setText(lable)
        self.modeTypeLabel.setText(self.get_mode_label_text())
        if self.selected_node:
            self.selected_node.selected = False
            self.selected_node = None
        if self.selected_line:
            self.selected_line.selected = False
            self.selected_line = None

    def validate(self):
        # validate system graph
        system_graph = create_graph(self.proc_list, self.sys_line_list, 'system')
        error_1 = check_system_graph(system_graph)
        # validate task graph
        task_graph = create_graph(self.node_list, self.task_line_list, 'task')
        error_2 = check_task_graph(task_graph)
        if error_1 or error_2:
            self.has_error = True
            error_message = 'Validation failed!\n'
            error_message += 'Check task graph!' if error_2 else 'Check system graph!'
            # error_dialog = DialogWindow()
            # error_dialog.show_error_dialog(error_message)
        else:
            self.has_error = False
        return system_graph, task_graph

    def build_queue_hendler(self):
        if self.has_error:
            return
        system_graph, task_graph = self.validate()
        if self.has_error:
            return
        queue3 = build_queue3(task_graph)
        queue8 = build_queue8(task_graph)
        queue11 = build_queue11(task_graph)
        # print u"Algorithm №3"
        # print queue3
        # print u"Algorithm №8"
        # print queue8
        # print u"Algorithm №11"
        # print queue11
        queue_result = u"\nAlgorithm №3\n" + str(queue3)
        queue_result += u"\n\nAlgorithm №8\n" + str(queue8)
        queue_result += u"\n\nAlgorithm №11\n" + str(queue11)

        self.w = InfoWindow(queue_result, 'Queue build result')
        self.w.setGeometry(QtCore.QRect(200, 200, 400, 200))
        self.w.show()

    def generate_graph_hendler(self):
        generate_graph_hendler()
        

    def save_into_file(self):
        save_file_dialog = DialogWindow()
        file_name, ans = save_file_dialog.showDialog('Enter file name:')
        if ans:
            data = dict(
                node_list=self.node_list,
                proc_list=self.proc_list,
                task_line_list=self.task_line_list,
                sys_line_list=self.sys_line_list,
                node_last_index=node_index_gen.next(),
                proc_last_index=proc_index_gen.next(),
                task_line_last_index=task_line_index_gen.next(),
                sys_line_last_index=sys_line_index_gen.next(),
                task_line_map=self.task_line_map,
                sys_line_map=self.sys_line_map,
            )
            with open(file_name, 'w') as f:
                pickle.dump(data, f)
        print 'file was saved'

    def open_file(self):
        global node_index_gen, task_line_index_gen, sys_line_index_gen, proc_index_gen
        open_file_dialog = DialogWindow()
        file_name, ans = open_file_dialog.showDialog('Enter file name:')
        if ans:
            with open(file_name, 'r') as f:
                data = pickle.load(f)
                if data:
                    self.node_list = data['node_list']
                    self.proc_list = data['proc_list']
                    self.task_line_list = data['task_line_list']
                    self.sys_line_list = data['sys_line_list']
                    self.task_line_map = data['task_line_map']
                    self.sys_line_map = data['sys_line_map']
                    node_index_gen = count(data['node_last_index'])
                    proc_index_gen = count(data['proc_last_index'])
                    task_line_index_gen = count(data['task_line_last_index'])
                    sys_line_index_gen = count(data['sys_line_last_index'])

    def paintEvent(self, event):
        if self.has_error:
            p = self.palette()
            p.setColor(self.backgroundRole(), QColor(255, 153, 153, 150))
            self.setPalette(p)
        else:
            p = self.palette()
            p.setColor(self.backgroundRole(), QColor(204, 255, 204, 150))
            self.setPalette(p)
        qp = QtGui.QPainter()
        qp.begin(self)
        if len(self.node_list):
            self.drawObjects(event, qp)
        self.update()
        qp.end()

    def mousePressEvent(self, event):
        x = event.pos().x()  # - CIRCLE_SIZE/2
        y = event.pos().y()  # - CIRCLE_SIZE/2
        if self.mode_type == 'task':
            self.mouse_press_handler_task(x, y)
        else:
            self.mouse_press_handler_system(x, y)
    
    def mouse_press_handler_system(self, x, y):
        selected_obj = find_selected_odj(self.proc_list+self.sys_line_list, x, y)
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
                if selected_node2 and selected_node2 != self.selected_node and not (
                    self.sys_line_map.get((self.selected_node.id, selected_node2.id)) or
                    self.sys_line_map.get((selected_node2.id, self.selected_node.id))
                ):
                    # draw line
                    new_line = Line(sys_line_index_gen.next(), self.selected_node, selected_node2)
                    self.sys_line_list.append(new_line)
                    self.sys_line_map[self.selected_node.id, selected_node2.id] = new_line
                self.selected_node.selected = False
                self.selected_node = None 
            else:            
                if selected_node2:
                    self.selected_node = selected_node2
                    selected_node2.selected = True
                else:    
                    node_weight_dialog = DialogWindow()
                    weight, ans = node_weight_dialog.showDialog('Enter CPU weight:')
                    if ans:
                        new_node = Node(proc_index_gen.next(), x, y)
                        new_node.set_weight(weight)
                        self.proc_list.append(new_node)

    def mouse_press_handler_task(self, x, y):
        selected_obj = find_selected_odj(self.node_list+self.task_line_list, x, y)
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
            # print 'selecte node 1 = ', self.selected_node
            # print 'selected node 2 = ', selected_node2
            if self.selected_node:
                if selected_node2 and selected_node2 != self.selected_node and not (
                    self.task_line_map.get((self.selected_node.id, selected_node2.id)) or
                    self.task_line_map.get((selected_node2.id, self.selected_node.id))
                ):
                    # draw line
                    new_line = Line(task_line_index_gen.next(), self.selected_node, selected_node2)
                    self.task_line_list.append(new_line)
                    self.task_line_map[self.selected_node.id, selected_node2.id] = new_line
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
        if event.key() == QtCore.Qt.Key_Delete:
            if self.selected_line:
                if self.mode_type == 'task':
                    del self.task_line_map[self.selected_line.from_node.id, self.selected_line.to_node.id]
                    self.task_line_list.remove(self.selected_line)
                else:
                    del self.sys_line_map[self.selected_line.from_node.id, self.selected_line.to_node.id]
                    self.sys_line_list.remove(self.selected_line)
                self.selected_line = None
            if self.selected_node:
                if self.mode_type == 'task':
                    self.node_list.remove(self.selected_node)
                    for line in reversed(self.task_line_list):
                        if self.selected_node == line.from_node or self.selected_node == line.to_node:
                            self.task_line_list.remove(line)
                            del self.task_line_map[line.from_node.id, line.to_node.id]
                else:
                    self.proc_list.remove(self.selected_node)
                    for line in reversed(self.sys_line_list):
                        if self.selected_node == line.from_node or self.selected_node == line.to_node:
                            self.sys_line_list.remove(line)
                            del self.sys_line_map[line.from_node.id, line.to_node.id]
                self.selected_node = None

    
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

        if self.mode_type == 'task':
            for line in self.task_line_list:
                line.draw_itself(event, qp, self.mode_type)
            for node in self.node_list:
                node.draw_itself(event, qp)
        else:
            for line in self.sys_line_list:
                line.draw_itself(event, qp, self.mode_type)
            for proc in self.proc_list:
                proc.draw_itself(event, qp)


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

    # def show_error_dialog(self, message):
    #     lable = QtGui.QLabel(message, self)
    #     lable.setAlignment(QtCore.Qt.AlignHCenter)
    #     btnQuit = QtGui.QPushButton(u"Quit", self)
    #     btnQuit.setGeometry(150, 75, 200, 30)
    #     self.connect(btnQuit, QtCore.SIGNAL('clicked()'), quit)

class InfoWindow(QtGui.QWidget):

    def __init__(self, info_text, title):
        super(InfoWindow, self).__init__()

        self.initUI(info_text, title)

    def initUI(self, info_text, title):
        self.info = info_text
        self.setWindowTitle(title)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignHCenter, self.info)

class MainApp(QtGui.QApplication):
    def __init__(self, *args):
        QtGui.QApplication.__init__(self, *args)
        self.main = MainGui()
        self.connect(self, QtCore.SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()

    def byebye( self ):
        self.exit(0)

if __name__ == "__main__":
    app = MainApp(sys.argv)
    app.exec_()