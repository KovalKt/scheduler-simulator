from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QPen

from math import sqrt
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

