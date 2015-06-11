from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QPen

from math import sqrt
from random import randint
CIRCLE_SIZE = 36
CIRCLE_R = CIRCLE_SIZE/2

class DrawableObject():
    
    def set_weight(self, weight):
        self.weight = weight

class Node(DrawableObject):
    def __init__(self, id, center_x, center_y):
        self.id = id
        self.x = center_x - CIRCLE_R
        self.y = center_y - CIRCLE_R
        self.center_x = center_x
        self.center_y = center_y
        self.weight = 1
        self.selected = False

    def __repr__(self):
        return 'Node %s' % self.id

    def is_selected(self, x1, y1):
        return (x1 < (self.center_x + CIRCLE_R) and x1 > (self.center_x - CIRCLE_R) and 
            y1 < (self.center_y + CIRCLE_R) and y1 > (self.center_y - CIRCLE_R))

    def set_weight(self, weight):
        self.weight = weight  

    def set_new_coordinate(self, new_x, new_y):
        self.center_x = new_x
        self.center_y = new_y
        self.x = new_x - CIRCLE_R
        self.y = new_y - CIRCLE_R

    def draw_itself(self, event, qp):
        circle_color = QColor(204, 0, 0) if self.selected else QColor(0, 0, 0)
        qp.setPen(QPen(circle_color, 3))
        qp.setBrush(QColor(255, 255, 255))
        qp.drawEllipse(self.x, self.y, CIRCLE_SIZE, CIRCLE_SIZE)
        # draw node id
        text = str(self.id)
        qp.setPen(QColor(102, 0, 0))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(self.x, self.y, text)  

        # draw node weight
        text = str(self.weight)
        qp.setPen(QColor(25, 0, 51))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(self.center_x-5, self.center_y+5, text)

class Line(DrawableObject):
    def __init__(self, id, from_node, to_node):
        self.id = id
        self.from_node = from_node
        self.to_node = to_node
        self.weight = 1
        self.selected = False

    def __repr__(self):
        return 'Node %s wght - %s' % (self.id, self.weight)

    def center_x(self):
        return (self.from_node.center_x + (self.to_node.center_x - self.from_node.center_x) / 2)

    def center_y(self):
        return (self.from_node.center_y + (self.to_node.center_y - self.from_node.center_y) / 2)

    def is_selected(self, x, y):
        return (x < (self.center_x() + CIRCLE_R) and x > (self.center_x() - CIRCLE_R) and 
            y < (self.center_y() + CIRCLE_R) and y > (self.center_y() - CIRCLE_R))

    def get_on_circle_point(self):
        x2 = self.from_node.center_x
        x1 = self.to_node.center_x
        y2 = self.from_node.center_y
        y1 = self.to_node.center_y
        l = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        xc = x1 - ((x1 - x2) * CIRCLE_R) / l 
        yc = y1 - ((y1 - y2) * CIRCLE_R) / l
        return xc, yc


    def draw_itself(self, event, qp, mode_type):
        line_color = QColor(153, 0, 0) if self.selected else QColor(0, 0, 0, 200)
        qp.setPen(QPen(line_color, 2))
        on_circle_point = self.get_on_circle_point()
        qp.drawLine(
            self.from_node.center_x, 
            self.from_node.center_y, 
            on_circle_point[0],
            on_circle_point[1],
        )
        if mode_type == 'task':
            # draw pointer
            qp.setPen(QPen(QColor(0, 0, 0), 12))
            qp.drawPoint(*on_circle_point)
        # draw weight
        text = str(self.weight)
        qp.setPen(QPen(QColor(25, 0, 51)))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(self.center_x()-2, self.center_y()+2, text)

class Gant_diagram():

    def __init__(self, tasks_queue, task_line_map):
        self.processors = {}
        self.free_proc = []
        self.current_time = 0
        self.next_task_end_time = 0
        self.tasks_queue = map(lambda x: x[0],tasks_queue)
        self.completed_tasks = {}
        self.ready_tasks = []
        self.task_line_map = task_line_map
        self.in_progress_tasks = []


    def prepare_data(self, proc_list):
        for proc in proc_list:
            self.processors[proc.id] = {'calc':[]}
            for n in range(int(proc.weight)):
                self.processors[proc.id]['link%s'%n] = []
        for k, v in self.processors.iteritems():
            print k, v
        self.free_proc = map(lambda x: x.id, sorted([p for p in proc_list], key=lambda x: int(x.weight)))
        # self.free_proc

    def first_assign_algorithm(self, task_graph, system_graph):
        print 'tasks_queue', self.tasks_queue
        print 'task_graph', task_graph
        from helpers import get_start_nodes, invert_graph
        self.ready_tasks = get_start_nodes(task_graph)
        print 'start_tasks', self.ready_tasks
        task_graph = invert_graph(task_graph)

        #assign start tasks
        self.next_task_end_time = int(self.ready_tasks[0].weight)
        for task in reversed(self.ready_tasks):
            proc_id = self.free_proc.pop()
            if int(task.weight) < self.next_task_end_time:
                self.next_task_end_time = int(task.weight)
            for t in range(int(task.weight)):
                self.processors[proc_id]['calc'].append(task)
            self.ready_tasks.remove(task)
            self.in_progress_tasks.append(task.id)
        print 'processors'
        for k, v in self.processors.iteritems():
            print k, v
        while len(self.completed_tasks) < len(self.tasks_queue):
            self.current_time = self.next_task_end_time
            print 'new current time', self.current_time
            for proc_id, time_lines in self.processors.iteritems():
                if (len(time_lines['calc']) == self.current_time or 
                    len(time_lines['calc']) > self.current_time and 
                    isinstance(time_lines['calc'], Node) and
                    time_lines['calc'][self.current_time-1] != time_lines['calc'][self.current_time]
                ):
                    compl_task = time_lines['calc'][self.current_time-1]
                    if isinstance(compl_task, int):
                        print '!!!!!!!!!!!compl_task is int', compl_task, time_lines['calc']
                        print '!!!!!!!!!current_time', self.current_time
                    self.completed_tasks[compl_task.id] = compl_task
                    self.in_progress_tasks.remove(compl_task.id)
                    self.free_proc.append(proc_id)
            print 'completed_tasks', self.completed_tasks
            print 'free_process', self.free_proc
            if len(self.completed_tasks) == len(self.tasks_queue):
                break
            self.update_ready_tasks(task_graph)
            # assign for random free proc
            proc_for_assign = self.free_proc[randint(0, len(self.free_proc)-1)]
            while self.ready_tasks:
                self.assign_to_proc(proc_for_assign, self.current_time, task_graph, system_graph)
                print 'processors after auto assign'
                for k, v in self.processors.iteritems():
                    print k, v
            self.find_next_task_end_time()
            # break

    def assign_to_proc(self, proc_for_assign, time, task_graph, system_graph):
        # if from_proc == proc_for_assign:
        #     self.
        print 'proc_for_assign', proc_for_assign
        proc_for_assign = filter(lambda x: x.id == proc_for_assign, system_graph)[0]
        task_to_assign = self.ready_tasks.pop()
        parents = task_graph[task_to_assign]
        print 'parents', parents
        for p in parents:
            for proc_id, time_lines in self.processors.iteritems():
                if p in time_lines['calc']:
                    parent_proc = filter(lambda x: x.id == proc_id, system_graph)[0]
            print task_to_assign,'parent_proc', parent_proc, proc_for_assign
            print '_______system graph_____', system_graph
            new_time = time
            if parent_proc == proc_for_assign:
                continue
                # self.assign_task_to_proc(task_to_assign, proc_for_assign, time)
            else:
                path = [item for item in dfs_paths(system_graph, parent_proc, proc_for_assign)]
                print '============', path, 'ppp', parent_proc, proc_for_assign
                path = sorted(path, key=lambda x: len(x))[0]
                if not path:
                    path = [item for item in dfs_paths(system_graph, proc_for_assign, parent_proc)]
                    path = sorted(path, key=lambda x: len(x))[0]
                print 'paths ', path
                # spikes
                if proc_for_assign == path[0]:
                    path.reverse()
                for indx, proc in enumerate(path):
                    if indx == 0:
                        new_time = self.assign_transmit_to_proc(task_to_assign, proc, new_time, p, 'send')
                        new_time -= 1
                    elif indx == len(path)-1:
                        new_time = self.assign_transmit_to_proc(task_to_assign, proc, new_time, p, 'recive')
                    else:
                        new_time -= 1
                        new_time = self.assign_transmit_to_proc(task_to_assign, proc, new_time, p, 'transfer')

                    # new_time -=1
                    # print "==__==__==__==", new_time
        self.assign_task_to_proc(task_to_assign, proc_for_assign, new_time)
        self.free_proc.remove(proc_for_assign.id)
        print 'clean free_proc', self.free_proc, proc_for_assign.id
        # break

    def assign_transmit_to_proc(self, task, proc_for_assign, time, parent_task, transmit_type, next_proc=None):
        
        while True:
            for line_name, time_line in self.processors[proc_for_assign.id].iteritems():
                if line_name == 'calc':
                    continue
                transmit = Transmit(parent_task, task, self.task_line_map, transmit_type)
                if len(time_line) == time:
                    for t in range(transmit.weight):
                        time_line.append(transmit)
                    return time+transmit.weight
                elif len(time_line) < time:
                    time_line += [0]*(time - len(time_line))
                    for t in range(transmit.weight):
                        time_line.append(transmit)
                    return time+transmit.weight
                elif len(time_line) > time:
                    # transmit_lengt = int(self.task_line_map[(parent_task.id, task.id)].weight)
                    if not any(time_line[time:time+transmit.weight]):
                        for t in range(transmit.weight):
                            time_line[time+t] = transmit
                        return time+transmit.weight
            time += 1

    def assign_task_to_proc(self, task, proc_for_assign, time):
        time_line = self.processors[proc_for_assign.id]['calc']
        # self.ready_tasks.remove(task)
        self.in_progress_tasks.append(task.id)
        while True:
            if len(time_line) == time:
                for t in range(int(task.weight)):
                    time_line.append(task)
                    return
            elif len(time_line) < time:
                time_line += [0]*(time - len(time_line))
                for t in range(int(task.weight)):
                    time_line.append(task)
                return
            elif len(time_line) > time:
                if not any(time_line[time:time+int(task.weight)]):
                    for t in range(int(task.weight)):
                        time_line[time+t] = task
                    return
                    #time+transmit.weight
            time += 1  

    def find_next_task_end_time(self):
        # next_time = self.current_time
        next_time = []
        for proc_id, time_lines in self.processors.iteritems():
            # p_next_time = next_time
            line = time_lines['calc']
            if not len(line):
                continue
            next_time.append(len(line))
            for i in range(len(line[self.current_time:-1])):
                if line[i] != line[i+1]:
                    next_time.append(self.current_time + i+1)
        print 'next_time ', next_time 
        self.next_task_end_time = min(filter(lambda x: x > self.current_time, next_time))


    def update_ready_tasks(self, task_graph):
        for task, dependance in task_graph.iteritems():
            if task.id not in self.completed_tasks and task.id not in self.in_progress_tasks and dependance:
                if all(map(lambda x: x.id in self.completed_tasks, dependance)):
                    print 'yahoo!!!', task, dependance
                    self.ready_tasks.append(task)

# def dfs_paths(graph, begin, goal, path = [], paths = []):
#     path.append(goal)
#     for related in graph[goal]:
#         if related == begin and len(path) > 2:
#             paths.append(list(path))
#         if related not in path:
#             paths = dfs_paths(graph, begin, related, path, paths)
#     path.pop()        
#     return paths

# def dfs_paths(graph, begin, current, path = [], paths = []):
#     print 'in dfs', begin, current
#     path.append(current)
#     for related in graph[current]:
#         if related == begin and len(path) > 2:
#             paths.append(list(path))
#         if related not in path:
#             paths = dfs_paths(graph, begin, related, path, paths)
#     path.pop()        
#     return paths

# def dfs_paths(graph, start, goal, path=None):
#     if path is None:
#         path = [start]
#     if start == goal:
#         yield path
#     for next in graph[start] - set(path):
#         yield dfs_paths(graph, next, goal, path + [next])

def dfs_paths(graph, start, end):
    todo = [[start, [start]]]
    while 0 < len(todo):
        (node, path) = todo.pop(0)
        for next_node in graph[node]:
            if next_node in path:
                continue
            elif next_node == end:
                yield path + [next_node]
            else:
                todo.append([next_node, path + [next_node]])

class Transmit():
    def __init__(self, from_task, to_task, task_line_map, _type):
        self.from_task = from_task
        self.to_task = to_task
        self.weight = int(task_line_map[(from_task.id, to_task.id)].weight)
        self.transmit_type = _type

    def __repr__(self):
        return "%s from t%s to t%s, time %s" % (self.transmit_type, self.from_task.id, self.to_task.id, self.weight)

